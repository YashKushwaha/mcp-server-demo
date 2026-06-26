## From https://github.com/modelcontextprotocol/python-sdk/blob/v2.0.0a2/examples/snippets/clients/streamable_basic.py
import asyncio

#from requests import session
from rich import print
from mcp import ClientSession, Resource, Tool
from mcp.client.streamable_http import streamable_http_client
from mcp.client.stdio import stdio_client, StdioServerParameters

from mcp.types import (
    BlobResourceContents,
    BlobResourceContents,
    ListToolsResult,
    ListResourcesResult,
    ListPromptsResult,
    CallToolResult,
    ReadResourceResult,
    GetPromptResult,
    ListResourceTemplatesResult,
    TextResourceContents,
    TextResourceContents
)


import os
async def test_fastmcp_quickstart(url):
    async with streamable_http_client(
        url
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


async def test_mcpserver(url):

    
    async with streamable_http_client(url) as (read_stream, write_stream):

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
            print(templates.resource_templates)

            print("\n=== PROMPTS ===")
            prompts: ListPromptsResult = await session.list_prompts()
            for p in prompts.prompts:
                print("-", p.name)

async def test_github_mcp_server():
    server_params = StdioServerParameters(
        command="podman",
        args=[
            "run",
            "--rm",
            "-i",
            "-e",
            "GITHUB_PERSONAL_ACCESS_TOKEN",
            "ghcr.io/github/github-mcp-server",
        ],
        env={
            "GITHUB_PERSONAL_ACCESS_TOKEN": os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"],
        },
    )

    async with stdio_client(server_params) as (read_stream, write_stream):

        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            print("\n=== TOOLS ===")
            tools: ListToolsResult = await session.list_tools()
            tools_list : list[Tool] = tools.tools
            for t in tools_list:
                print("-", t.name)
                #print(t.description)
                #print(t.input_schema)
                #print('\n')

            #return
            print("\n=== RESOURCES ===")
            resources: ListResourcesResult = await session.list_resources()
            resource_list: list[Resource] = resources.resources
            for r in resource_list:
                print("-", r.uri, r.mime_type)
                out: ReadResourceResult = await session.read_resource(r.uri)
                contents: list[TextResourceContents | BlobResourceContents] = out.contents

                to_write = '\n'.join([str(c.text) for c in contents])
                with open(f"resource_{r.uri.replace('/', '_')}.html", "w") as f:
                    f.write(to_write)
            return 
            print("\n=== RESOURCE TEMPLATES ===")
            templates: ListResourceTemplatesResult = await session.list_resource_templates()
            for t in templates.resource_templates:
                print("-", t.name, ' => ',t.description)

            print("\n=== PROMPTS ===")
            prompts: ListPromptsResult = await session.list_prompts()
            for p in prompts.prompts:
                print("-", p.name)

if __name__ == "__main__":

    url = "http://localhost:8000/mcp"

    #url = "http://localhost:8001/mcp"

    asyncio.run(test_github_mcp_server()) 
    #asyncio.run(test_mcpserver(url)) 