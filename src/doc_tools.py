"""Read-only tools over Vein's documents, and the registry the model is offered.

ask_cipher_docs wraps the grounded ask() from src/answer.py, unchanged: the refusal before
any model call below the threshold and check_citations() still decide every answer. The tool
only adds a contract in front of it (src/contracts.py).

What the tool touches: the files in data/corpus/ (read), plus the answer log ask() already
writes. It takes no path, no k, no threshold and no model from the caller.
Which answerer is used is server configuration, never an argument:
    default        sentences extracted from the sources, no model
    VEIN_LIVE=1    the model in src/llm.py (needs OPENROUTER_API_KEY)
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable

from pydantic import BaseModel

from . import llm
from .answer import ask
from .contracts import AskCipherDocs


class ToolFailure(Exception):
    """An expected failure. The message is written for the model: what happened, what to do."""


class Citation(BaseModel):
    n: int
    source: str


class DocAnswer(BaseModel):
    answer: str
    citations: list[Citation]
    grounded: bool
    reason: str


@dataclass(frozen=True)
class Tool:
    name: str
    args: type[BaseModel]
    run: Callable[[BaseModel], BaseModel]
    writes: bool = False

    def schema(self) -> dict:
        """The function-calling schema the model sees. Same class the call is validated with."""
        return {"type": "function",
                "function": {"name": self.name, "description": self.args.__doc__,
                             "parameters": self.args.model_json_schema()}}


def ask_cipher_docs(args: AskCipherDocs) -> DocAnswer:
    generate = llm.generate if os.environ.get("VEIN_LIVE") == "1" else None
    try:
        r = ask(args.question, generate=generate, log_path=os.environ.get("VEIN_ANSWER_LOG"))
    except RuntimeError:
        # llm.get_client() without a key. Say what to do; do not echo internals.
        raise ToolFailure("The answer model is not available on this server right now. "
                          "Try again later, or answer without this tool.") from None
    # A refusal is a valid result (grounded=false), not an error: the model should tell the
    # person the documents do not cover it, not retry with different wording to force an answer.
    return DocAnswer(answer=r["answer"], grounded=r["grounded"], reason=r["reason"],
                     citations=[Citation(**c) for c in r["citations"]])


DOC_TOOLS: dict[str, Tool] = {
    "ask_cipher_docs": Tool("ask_cipher_docs", AskCipherDocs, ask_cipher_docs, writes=False),
}


def tools_for(caller: str | None) -> dict[str, Tool]:
    """What this caller is offered. Read-only tools go to everyone, signed in or not;
    a tool that writes would only be offered to a signed-in caller. Nothing here writes."""
    return {name: t for name, t in DOC_TOOLS.items() if caller or not t.writes}
