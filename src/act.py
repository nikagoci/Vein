"""The function-calling door: the model asks for a tool, our code decides whether it runs.

call_tool() applies three gates, in order:
  1. offered?   the tool is in the set this caller was offered (doc_tools.tools_for)
  2. valid?     the arguments pass the tool's contract (src/contracts.py); otherwise nothing runs
  3. identity   who is calling comes from the app (`caller`), never from the arguments

It never raises for a bad call. Whatever happens becomes {ok, error, result} for the model to
read, and one line in logs/tools.jsonl. A real bug in a tool still crashes loudly.

The log line records the tool, the outcome, the latency, a hash of the caller and the SIZE of
the arguments, never their text: a question can contain anything a person typed.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from pydantic import ValidationError

from .doc_tools import Tool, ToolFailure

ROOT = Path(__file__).resolve().parent.parent


def tool_log_path() -> Path:
    return Path(os.environ.get("VEIN_TOOL_LOG", ROOT / "logs" / "tools.jsonl"))


def caller_key(caller: str) -> str:
    return hashlib.sha256(caller.encode("utf-8")).hexdigest()[:12]


def brief(e: ValidationError, tool: Tool) -> str:
    """A validation error the model can act on: which field, what was wrong, what to send."""
    parts = []
    for x in e.errors():
        field = ".".join(map(str, x["loc"])) or "arguments"
        parts.append(f"{field}: {x['msg']}")
    allowed = ", ".join(tool.args.model_fields)
    return f"invalid arguments: {'; '.join(parts)}. Send only: {allowed}, as described in the tool schema."


def call_tool(call: dict, allowed: dict[str, Tool], caller: str | None) -> dict:
    t0 = time.perf_counter()
    raw = call.get("arguments")
    raw = raw if isinstance(raw, str) else json.dumps(raw or {})
    tool = allowed.get(call["name"])
    if tool is None:                                                       # 1 · offered?
        offered = ", ".join(sorted(allowed)) or "none"
        return _log(call, raw, caller, t0, error=f"no tool named {call['name']!r} is available. "
                                                 f"Available tools: {offered}.")
    try:
        args = tool.args.model_validate_json(raw or "{}")                  # 2 · valid?
    except ValidationError as e:
        return _log(call, raw, caller, t0, error=brief(e, tool))
    try:
        out = tool.run(args, caller=caller) if tool.writes else tool.run(args)   # 3 · identity from us
    except ToolFailure as e:
        return _log(call, raw, caller, t0, error=str(e))
    return _log(call, raw, caller, t0, result=out.model_dump(mode="json"))


def _log(call: dict, raw: str, caller: str | None, t0: float,
         result: dict | None = None, error: str | None = None) -> dict:
    line = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "tool": call["name"], "ok": error is None, "error": error,
            "caller": caller_key(caller) if caller else None,
            "argument_chars": len(raw or ""),
            "latency_ms": int((time.perf_counter() - t0) * 1000)}
    path = tool_log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(line) + "\n")
    return {**line, "result": result}
