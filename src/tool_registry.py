"""The common tool registry used by local tests and the MCP server."""
from src.tools.vigenere_encrypt import encrypt_vigenere

TOOLS = {
    "encrypt_vigenere": encrypt_vigenere,
}


def call_tool(name: str, arguments: dict) -> dict:
    """Call a registered tool by name; unknown names fail safely."""
    if name not in TOOLS:
        raise ValueError(f"Unknown tool '{name}'. Check the available tool names and try again.")
    return TOOLS[name](arguments)
