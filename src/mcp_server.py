"""MCP entry point. Install requirements.txt before running this module."""
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from src.tool_registry import call_tool

mcp = FastMCP("Vein")


@mcp.tool(name="encrypt_vigenere")
def encrypt_vigenere_tool(
    text: Annotated[str, Field(min_length=1, max_length=10_000)],
    key: Annotated[str, Field(min_length=1, max_length=64, pattern=r"^[A-Za-z]+$")],
) -> dict[str, str]:
    """Encrypt text using the Vigenere cipher. Only English-letter keys are accepted."""
    return call_tool("encrypt_vigenere", {"text": text, "key": key})


if __name__ == "__main__":
    mcp.run()
