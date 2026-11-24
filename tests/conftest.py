import pytest

from src import llm


@pytest.fixture(autouse=True)
def no_real_model(monkeypatch, tmp_path):
    """Tests never call a real model and never write to the repo's logs/.

    VEIN_OFFLINE=1 routes llm.generate() to the fake model, the key is removed so a real
    client cannot be built even if a developer has one exported, and usage lines go to a
    temporary file."""
    monkeypatch.setenv("VEIN_OFFLINE", "1")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.setenv("VEIN_USAGE_LOG", str(tmp_path / "usage.jsonl"))
    monkeypatch.setenv("VEIN_TOOL_LOG", str(tmp_path / "tools.jsonl"))       # src/act.py
    monkeypatch.setenv("VEIN_ANSWER_LOG", str(tmp_path / "answers.jsonl"))   # src/doc_tools.py
    monkeypatch.delenv("VEIN_LIVE", raising=False)
    monkeypatch.setattr(llm, "_client", None)
