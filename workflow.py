import asyncio
import os
from contextlib import asynccontextmanager
#from requests import session
from rich import print
from mcp import ClientSession, Resource, Tool
from mcp.client.streamable_http import streamable_http_client
from mcp.client.stdio import stdio_client, StdioServerParameters

from mcp.types import CallToolResult


@asynccontextmanager
async def get_github_session_context():
    server_params = StdioServerParameters(
                        command="podman",
                        args=["run","--rm","-i","-e","GITHUB_PERSONAL_ACCESS_TOKEN","ghcr.io/github/github-mcp-server",],
                        env={"GITHUB_PERSONAL_ACCESS_TOKEN": os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"],},
                    )

    async with stdio_client(server_params) as (read_stream, write_stream):

        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            yield session

GOAL_TO_TOOL = {
    "whoami": "get_me",
    "repos": "search_repositories",
    "branches": "list_branches",
    "issues": "list_issues",
}

async def get_tool_maping(session):
    tool_map = {}
    tools = await session.list_tools()
    #resources = await session.list_resources()
    #prompts = await session.list_prompts()
    for tool in tools.tools:
        tool_map[tool.name] = tool

    return tool_map

async def main():
    # goal = input("Enter Input: ")
    
    # tool = GOAL_TO_TOOL[goal]
    
    # async with get_github_session_context() as session:
    #     tool_map = await get_tool_maping(session)
    #     result = await session.call_tool(tool, {})
    #     print(result)
    async with get_github_session_context() as session:
        tool = 'list_branches'
        result: CallToolResult = await session.call_tool(tool, {'owner': 'YashKushwaha', 'repo': 'mcp-server-demo'})
        print(result.model_dump())

if __name__=='__main__':
    asyncio.run(main())