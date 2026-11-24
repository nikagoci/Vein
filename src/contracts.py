"""Tool contracts: what each tool accepts, as types the code checks.

Single source of truth for the inputs of the tools in src/doc_tools.py. Both doors read it:
  * function calling: Tool.schema() in src/doc_tools.py is built from these classes
  * MCP: src/mcp_server.py uses the same type aliases in its signatures
tests/test_mcp.py fails if the two doors ever describe a tool differently.

Rules for every contract here:
  * extra="ignore": an argument we did not ask for is refused, never silently ignored
  * every string is bounded and has a pattern
  * nothing names WHO is calling, and nothing lets the model choose a file, a path, k,
    the refusal threshold or the model. Those are decided by the server, not the caller.

(Nika's encrypt_vigenere keeps its own contract in src/tool_registry.py.)
"""
from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

# 3 to 300 characters, no control characters (newlines, tabs, NUL...). Long enough for any
# real question about the ciphers, too short to smuggle a page of instructions.
Question = Annotated[str, Field(
    min_length=3, pattern=r"^[^\x00-\x1f\x7f]+$",
    description="The question, in plain words, 3 to 300 characters. Example: How does the Caesar cipher work?")]


class Contract(BaseModel):
    model_config = ConfigDict(extra="ignore")


class AskCipherDocs(Contract):
    """Answer a question about the Caesar, Vigenere or Rail Fence ciphers using only Vein's own documents, with numbered citations. Refuses when the documents do not cover the question. Reads only; changes nothing."""
    question: Question
