import json
import re
import time
from pathlib import Path

from .retrieve import ROOT, load_chunks, retrieve

THRESHOLD = 0.3
REFUSAL = "I can't answer that from my sources."


def check_citations(answer, n_sources):
    """Every sentence must cite [n]; every n must be a retrieved source."""
    sentences = [s for s in re.split(r"(?<=\.)\s+", answer.strip()) if s]
    if not sentences:
        return False, "empty answer"
    for s in sentences:
        cited = [int(n) for n in re.findall(r"\[(\d+)\]", s)]
        if not cited:
            return False, "uncited sentence"
        if any(n < 1 or n > n_sources for n in cited):
            return False, "unknown citation"
    return True, ""


def _extractive(question, hits):
    parts = []
    for i, h in enumerate(hits, 1):
        for s in re.split(r"(?<=\.)\s+", h["text"]):
            parts.append(f"{s.rstrip('.')} [{i}].")
    return " ".join(parts)


def _log(path, question, grounded, reason, top_score, model):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    line = {"ts": time.time(), "question": question, "grounded": grounded,
            "reason": reason, "top_score": round(top_score, 3), "model": model}
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(line) + "\n")


def ask(question, chunks=None, k=2, generate=None, log_path=None, threshold=None):
    """Answer from the corpus, or refuse. `generate(question, hits) -> str` is
    an optional model hook; without it the answer is extracted from the
    sources and no model is called."""
    log_path = log_path or ROOT / "logs" / "usage.jsonl"
    chunks = chunks if chunks is not None else load_chunks()
    hits = retrieve(question, chunks, k)
    top = hits[0]["score"] if hits else 0.0

    def refuse(reason):
        _log(log_path, question, False, reason, top, "none" if generate is None else "hook")
        return {"answer": REFUSAL, "citations": [], "grounded": False, "reason": reason}

    hits = [h for h in hits if h["score"] >= (THRESHOLD if threshold is None else threshold)]
    if not hits:
        return refuse("below threshold")
    text = generate(question, hits) if generate else _extractive(question, hits)
    ok, why = check_citations(text, len(hits))
    if not ok:
        return refuse(why)
    _log(log_path, question, True, "ok", top, "none" if generate is None else "hook")
    return {"answer": text, "grounded": True, "reason": "ok",
            "citations": [{"n": i, "source": h["source"]} for i, h in enumerate(hits, 1)]}
