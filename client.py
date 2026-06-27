import sys

from mcp.client.streamable_http import streamable_http_client
from mcp import ClientSession
from langchain_openai import ChatOpenAI

from setup_telemetry import run_telemetry_setup

run_telemetry_setup()

from openinference.instrumentation.langchain import LangChainInstrumentor
LangChainInstrumentor().instrument()

from contextlib import asynccontextmanager
from langchain.agents import create_agent
from rich import print
import asyncio

from mcp.server.mcpserver import MCPServer

async def load_mcp_tools_manually(session: ClientSession):
    """Manually load tools from MCP server"""
    
    # Get all available tools from the server
    response = await session.list_tools()
    
    tools = []
    for tool in response.tools:
        tools.append({
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema if hasattr(tool, 'inputSchema') else {}
        })
    
    return tools

@asynccontextmanager
async def get_mcp_session():
    async with streamable_http_client("http://localhost:8010/mcp") as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            #tools = await load_mcp_tools(session)
            yield session

system_prompt = """You are a personal assistant with access to external tools.

        Use available tools whenever they help fulfill the user's request more accurately or persist information beyond the current conversation.

        Do not claim to have performed an action unless you have successfully used the appropriate tool.

        Prefer tool results over assumptions.

        Respond naturally and concisely.

        If the user asks you to save or remember something, infer the note content when it is reasonably clear.

        Only ask follow-up questions if essential information is missing.

        For example:

        User: "Remember I have a dentist appointment this weekend."

        → Save "Dentist appointment this weekend."

        Do not ask for confirmation unless the request is ambiguous.

    """.replace('\t', ' ')

from langchain.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from mcp.types import CallToolResult
from langchain_core.messages.tool import (
        ToolCall,
        ToolMessage)

async def main():
    async with get_mcp_session() as session:
        tools = await load_mcp_tools_manually(session)
        print("Available tools:", [t["name"] for t in tools])
        model_wo_tools = ChatOpenAI(model = "gpt-5-nano")
        model = model_wo_tools.bind_tools(tools)
        system_msg = SystemMessage(system_prompt)
        #user_query = "I am planning to go to the dentist this weekend, can you save a note for me ?"
        user_query = 'What is the current time ?'
        human_msg = HumanMessage(user_query)
        messages = [system_msg, human_msg]

        response: AIMessage = await model.ainvoke(messages) 
        print('response')
        print(response)
        messages.append(response)

        tool_calls: list[ToolCall]   = response.tool_calls
        if tool_calls:
            for tool_call in tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                print('Tool call: ', tool_name)
                tool_result: CallToolResult = await session.call_tool(name = tool_name, arguments=tool_args)
                tool_message = \
                    ToolMessage(
                        content=str(tool_result.content),
                        artifact=tool_result,
                        tool_call_id=tool_call['id'],
                    )
                messages.append(tool_message)

            final_response: AIMessage = await model.ainvoke(messages) 
            print('final_response')
            print(final_response)


if __name__ == '__main__':
    asyncio.run(main())