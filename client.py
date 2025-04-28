from mcp.client.http import http_client
from mcp import ClientSession
import asyncio

async def main():
    async with http_client("http://127.0.0.1:6277") as transport:
        async with ClientSession(transport) as client:
            result = await client.call("add", a=5, b=7)
            print(result)

            greeting = await client.get("greeting://John")
            print(greeting)

asyncio.run(main())
