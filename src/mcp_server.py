"""Vein as an MCP server (MCP Python SDK 2.x, MCPServer). Install requirements.txt first.

Run over stdio (what Claude Code, Cursor and VS Code launch):
    python -m src.mcp_server
Connect it to Claude Code from the repo root:
    claude mcp add --transport stdio vein -- python -m src.mcp_server

Tools:
  * encrypt_vigenere  (owner: nikagoci, HW2)  contract and handler in src/tool_registry.py
  * ask_cipher_docs   (owner: Izmirku, HW2)   contract in src/contracts.py; it goes through the
                       same gates and log as the function-calling door (src/act.py)
"""
import json
from typing import Annotated

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import Field

from src import act, doc_tools
from src.contracts import AskCipherDocs, Question
from src.tool_registry import call_tool

mcp = MCPServer("Vein", instructions="Classical ciphers (educational, not secure) and answers "
                                     "from Vein's own cipher documents, with citations.")
READS = ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=True,
                        open_world_hint=False)


@mcp.tool(name="encrypt_vigenere")
def encrypt_vigenere_tool(
    text: Annotated[str, Field(min_length=1, max_length=10_000)],
    key: Annotated[str, Field(min_length=1, max_length=64, pattern=r"^[A-Za-z]+$")],
) -> dict[str, str]:
    """Encrypt text using the Vigenere cipher. Only English-letter keys are accepted."""
    return call_tool("encrypt_vigenere", {"text": text, "key": key})


@mcp.tool(name="ask_cipher_docs", annotations=READS, description=AskCipherDocs.__doc__)
def ask_cipher_docs_tool(question: Question) -> doc_tools.DocAnswer:
    # Identity: MCP hosts here are a single local user, so no caller is passed (the tool needs none).
    out = act.call_tool({"name": "ask_cipher_docs", "arguments": json.dumps({"question": question})},
                        doc_tools.tools_for(None), None)
    if not out["ok"]:
        raise ToolError(out["error"])
    return doc_tools.DocAnswer(**out["result"])


if __name__ == "__main__":
    mcp.run()
