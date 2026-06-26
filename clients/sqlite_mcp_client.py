import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def main():
    async with streamable_http_client("http://127.0.0.1:8001/mcp") as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()

            print("Creating table...")
            await session.call_tool("write_query", {
                "query": """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER
                )
                """
            })

            print("Inserting data...")
            await session.call_tool("write_query", {
                "query": "INSERT INTO users (name, age) VALUES ('Alice', 25)"
            })

            await session.call_tool("write_query", {
                "query": "INSERT INTO users (name, age) VALUES ('Bob', 30)"
            })

            print("Reading data...")
            result = await session.call_tool("read_query", {
                "query": "SELECT * FROM users"
            })
            print(result)

            print("Tables:")
            tables = await session.call_tool("list_tables", {})
            print(tables)

asyncio.run(main())