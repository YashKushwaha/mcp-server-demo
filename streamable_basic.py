## From https://github.com/modelcontextprotocol/python-sdk/blob/v2.0.0a2/examples/snippets/clients/streamable_basic.py
import asyncio

#from requests import session

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from mcp.types import (
    ListToolsResult,
    ListResourcesResult,
    ListPromptsResult,
    CallToolResult,
    ReadResourceResult,
    GetPromptResult,
)


async def main():
    async with streamable_http_client(
        "http://localhost:8000/mcp"
    ) as (read_stream, write_stream):

        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            print("\n=== TOOLS ===")
            tools: ListToolsResult = await session.list_tools()
            for t in tools.tools:
                print("-", t.name)

            print("\n=== RESOURCES ===")
            resources: ListResourcesResult = await session.list_resources()
            for r in resources.resources:
                print("-", r.uri)

            templates: ListResourceTemplatesResult = await session.list_resource_templates()
            print(dir(templates))
            print(templates.resource_templates)

            print("\n=== PROMPTS ===")
            prompts: ListPromptsResult = await session.list_prompts()
            for p in prompts.prompts:
                print("-", p.name)

            print("\n=== TOOL CALL ===")
            result: CallToolResult = await session.call_tool(
                "add",
                {"a": 10, "b": 32},
            )
            print(result)

            print("\n=== RESOURCE ===")
            greeting: ReadResourceResult = await session.read_resource(
                "greeting://Alice"
            )
            print(greeting)

            print("\n=== PROMPT ===")
            prompt: GetPromptResult = await session.get_prompt(
                "greet_user",
                {
                    "name": "Alice",
                    "style": "casual",
                },
            )
            print(prompt)


asyncio.run(main())