from mcp.server import MCPServer
from mcp.server.mcpserver.tools import Tool

mcp = MCPServer("Demo")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.resource("greeting://{name}")
def greeting(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

"""
To run the server from terminal-> 

uv run mcp run server.py --transport streamable-http

"""