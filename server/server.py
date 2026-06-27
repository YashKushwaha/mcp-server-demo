"""
FastMCP quickstart example.

Run from the repository root:
    uv run examples/snippets/servers/fastmcp_quickstart.py
"""

from mcp.server.mcpserver import MCPServer, Context
import random
from datetime import datetime

# Create an MCP server
mcp = MCPServer("Demo")

@mcp.tool()
def echo(text: str) -> str:
    """Echoes the input text"""
    return text

@mcp.tool()
def reverse(text: str) -> str:
    """Returns the input text but reversed"""
    return text[::-1]

@mcp.tool()
def random_number() -> int:
    """Returns a random number between 1 to 10"""
    return random.randint(1, 10)

@mcp.tool()
def current_time() -> str:
    """Return the current time in the format YYYY-MM-DD HH:MM:SS.mmmmmm"""
    return datetime.now().isoformat()

@mcp.tool()
def save_note(text: str) -> str:
    """Save incoming text into note book"""
    with open("notes.txt", "a") as f:
        f.write(text + "\n")
    return f"saved into notebook text: {text}"

@mcp.tool()
def read_notebook() -> str:
    """Returns the entire content of notebook"""
    with open("notes.txt", "r") as f:
        notes = f.read()
    return notes


# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8010,
    )