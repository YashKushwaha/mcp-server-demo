import sqlite3
import aiosqlite

from mcp.server.mcpserver import MCPServer

# Create an MCP server
mcp = MCPServer("sqlite-Demo")

DB_PATH = "test.db"

@mcp.tool()
async def read_query(query: str):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(query) as cursor:
            rows = await cursor.fetchall()
            return rows

@mcp.tool()
async def write_query(query: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(query)
        await db.commit()
        return "OK"

@mcp.tool()
async def list_tables():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ) as cursor:
            return await cursor.fetchall()

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8001,
    )