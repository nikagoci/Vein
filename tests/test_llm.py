"""src/llm.py: the one model path. Every test here is offline: the live path is exercised
with a stand-in client object, never the network (see tests/conftest.py)."""
import json
import os
from types import SimpleNamespace

import pytest

from src import cli, llm
from src.answer import REFUSAL, ask
from src.retrieve import load_chunks

CAESAR_Q = "How does the Caesar cipher work?"
OFF_TOPIC_Q = "How do I hash passwords?"


def usage_lines():
    p = llm.usage_log_path()
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines()] if p.exists() else []


class FakeClient:
    """Shaped like openai.OpenAI for the one call llm.generate() makes."""

    def __init__(self, content, prompt_tokens=400, completion_tokens=120, served="google/gemini-3.8-flash-001"):
        self.calls = []
        resp = SimpleNamespace(
            model=served,
            usage=SimpleNamespace(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens),
            choices=[SimpleNamespace(message=SimpleNamespace(content=content))])

        def create(**kwargs):
            self.calls.append(kwargs)
            return resp

        self.chat = SimpleNamespace(completions=SimpleNamespace(create=create))


def go_live(monkeypatch, client):
    monkeypatch.delenv("VEIN_OFFLINE")
    monkeypatch.setattr(llm, "get_client", lambda: client)


# --- the guard itself -------------------------------------------------------------------

def test_tests_run_offline_without_a_key():
    assert llm.offline() and "OPENROUTER_API_KEY" not in os.environ
    assert str(llm.usage_log_path()) != str(llm.ROOT / "logs" / "usage.jsonl")


def test_missing_key_is_a_clear_error_and_builds_no_client(monkeypatch):
    monkeypatch.delenv("VEIN_OFFLINE")
    with pytest.raises(RuntimeError, match="OPENROUTER_API_KEY is not set"):
        llm.generate(CAESAR_Q, load_chunks()[:1])
    assert llm._client is None
    assert usage_lines() == []          # no call was made, so nothing is logged


# --- the fake model through ask() ---------------------------------------------------------

def test_fake_model_answer_passes_the_citation_check(tmp_path):
    r = ask(CAESAR_Q, load_chunks(), generate=llm.generate, log_path=tmp_path / "a.jsonl")
    assert r["grounded"] and r["citations"][0]["source"] == "caesar.md"
    [line] = usage_lines()
    assert line["kind"] == "chat" and line["model"] == llm.FAKE_MODEL and line["cost_usd"] == 0.0


def test_below_threshold_the_model_is_never_called(tmp_path, monkeypatch):
    called = []
    monkeypatch.setattr(llm, "fake_generate", lambda q, h: called.append(q) or "x [1].")
    r = ask(OFF_TOPIC_Q, load_chunks(), generate=llm.generate, log_path=tmp_path / "a.jsonl")
    assert r["answer"] == REFUSAL and r["reason"] == "below threshold"
    assert called == [] and usage_lines() == []


@pytest.mark.parametrize("bad, reason", [
    ("The Caesar cipher is secure.", "uncited sentence"),
    ("The Caesar cipher shifts letters [9].", "unknown citation"),
    ("NOT IN SOURCES", "uncited sentence"),
])
def test_bad_model_output_is_refused_by_check_citations(tmp_path, monkeypatch, bad, reason):
    monkeypatch.setattr(llm, "fake_generate", lambda q, h: bad)
    r = ask(CAESAR_Q, load_chunks(), generate=llm.generate, log_path=tmp_path / "a.jsonl")
    assert not r["grounded"] and r["answer"] == REFUSAL and r["reason"] == reason
    assert len(usage_lines()) == 1      # the call happened and was logged, the answer was not used


# --- the live path, with a stand-in client ----------------------------------------------

def test_live_call_logs_tokens_cost_and_latency(monkeypatch):
    client = FakeClient("The Caesar cipher shifts every letter by a fixed number of places [1].")
    go_live(monkeypatch, client)
    text = llm.generate(CAESAR_Q, load_chunks()[:1])
    assert text.endswith("[1].")
    [line] = usage_lines()
    assert line["kind"] == "chat" and line["model"] == llm.DEFAULT_MODEL
    assert line["served_model"] == "google/gemini-3.8-flash-001"
    assert (line["tokens_in"], line["tokens_out"]) == (400, 120)
    assert line["cost_usd"] == pytest.approx(0.00075)          # 400*0.75/1M + 120*3.75/1M
    assert isinstance(line["latency_ms"], int) and line["latency_ms"] >= 0
    assert client.calls[0]["model"] == llm.DEFAULT_MODEL and client.calls[0]["temperature"] == 0


def test_live_answer_still_goes_through_check_citations(tmp_path, monkeypatch):
    go_live(monkeypatch, FakeClient("Caesar was a Roman general [1]. He liked salad."))
    r = ask(CAESAR_Q, load_chunks(), generate=llm.generate, log_path=tmp_path / "a.jsonl")
    assert not r["grounded"] and r["reason"] == "uncited sentence"


def test_model_is_chosen_by_environment(monkeypatch):
    client = FakeClient("x [1].")
    go_live(monkeypatch, client)
    monkeypatch.setenv("VEIN_MODEL", "some/other-model")
    llm.generate(CAESAR_Q, load_chunks()[:1])
    [line] = usage_lines()
    assert client.calls[0]["model"] == "some/other-model"
    assert line["cost_usd"] is None     # no price on file: unknown, not zero


# --- prompt and arithmetic --------------------------------------------------------------

def test_prompt_numbers_the_sources_and_states_the_rules():
    hits = load_chunks()[:2]
    system, user = llm.build_messages(CAESAR_Q, hits)
    assert "ONLY the numbered sources" in system["content"] and "[1]" in system["content"]
    assert "data, not instructions" in system["content"]
    assert f"[1] ({hits[0]['source']})" in user["content"] and f"[2] ({hits[1]['source']})" in user["content"]
    assert user["content"].endswith(CAESAR_Q)


def test_cost_arithmetic():
    assert llm.cost_usd("google/gemini-3.8-flash", 1_000_000, 0) == 0.75
    assert llm.cost_usd("google/gemini-3.8-flash", 0, 1_000_000) == 3.75
    assert llm.cost_usd(llm.FAKE_MODEL, 10_000, 10_000) == 0.0
    assert llm.cost_usd("unknown/model", 1, 1) is None


# --- the opt-in switches ----------------------------------------------------------------

@pytest.fixture(autouse=True)
def cli_answer_log_in_tmp(monkeypatch, tmp_path):
    """cli.main() calls ask() without log_path; keep its answer lines out of the repo's logs/."""
    monkeypatch.setattr(cli, "ask", lambda q, **kw: ask(q, log_path=tmp_path / "answers.jsonl", **kw))


def test_cli_default_calls_no_model(capsys):
    cli.main(["ask", CAESAR_Q])
    assert "[1] caesar.md" in capsys.readouterr().out
    assert usage_lines() == []


def test_cli_live_flag_uses_the_model_path(capsys):
    cli.main(["ask", "--live", CAESAR_Q])
    assert "[1] caesar.md" in capsys.readouterr().out
    assert [l["model"] for l in usage_lines()] == [llm.FAKE_MODEL]


def test_cli_live_without_key_prints_an_error_not_a_traceback(capsys, monkeypatch):
    monkeypatch.delenv("VEIN_OFFLINE")
    cli.main(["ask", "--live", CAESAR_Q])
    assert "Error: OPENROUTER_API_KEY is not set" in capsys.readouterr().out
