"""Runs every tool golden file in evals/tools/*.yaml that uses the course template format,
through the real gates. No model, no key. From Lab-5/templates/test_tool_golden.py, with the
two imports changed for Vein (src.doc_tools instead of src.tools).

Each case calls call_tool() exactly as a model's request would: the tool must be offered to
the caller, the arguments must pass the contract, and identity comes from `caller`, never the
arguments. It lives in tests/, so CI runs it, and a failing case blocks the merge.

nikagoci.yaml predates the template and is run by its owner's own test file. It is listed
here by name so no file in evals/tools/ can be skipped silently.
"""
import json
from pathlib import Path

import pytest
import yaml

from src.act import call_tool
from src.doc_tools import tools_for

ROOT = Path(__file__).resolve().parents[1]
LEGACY = {"nikagoci.yaml": "tests/test_tool_golden.py"}   # file -> the test that runs it
ALL_FILES = sorted((ROOT / "evals" / "tools").glob("*.yaml"))
FILES = [f for f in ALL_FILES if f.name not in LEGACY]
CASES = [(f.stem, case) for f in FILES for case in yaml.safe_load(f.read_text(encoding="utf-8"))["cases"]]


def subset(expected: dict, actual) -> bool:
    """Every key in `expected` is in `actual` with the same value. Lists and nested dicts compare whole."""
    return isinstance(actual, dict) and all(k in actual and actual[k] == v for k, v in expected.items())


@pytest.mark.parametrize("owner, case", CASES, ids=[f"{o}:{c['id']}" for o, c in CASES])
def test_tool_golden_case(owner, case):
    call = {"id": case["id"], "name": case["tool"], "arguments": json.dumps(case["arguments"])}
    out = call_tool(call, tools_for(case.get("caller")), case.get("caller"))
    if case["expect"] == "ok":
        assert out["ok"], f"{owner}:{case['id']} should succeed but was refused: {out['error']}"
        assert subset(case.get("result_has", {}), out["result"]), f"result was {out['result']}"
    else:
        assert not out["ok"], f"{owner}:{case['id']} should be refused but ran: {out['result']}"
        for phrase in case.get("error_has", []):
            assert str(phrase).lower() in out["error"].lower(), f"error was: {out['error']}"


def test_every_file_has_five_cases_including_one_adversarial():
    assert FILES, "no template-format golden files found in evals/tools/"
    for f in FILES:
        cases = yaml.safe_load(f.read_text(encoding="utf-8"))["cases"]
        types = [c["type"] for c in cases]
        assert len(cases) >= 5, f"{f.name}: {len(cases)} cases, HW2 needs 5"
        assert "adversarial" in types and "bad-input" in types, f"{f.name}: needs a bad-input and an adversarial case"
        assert all(c.get("why") for c in cases), f"{f.name}: every case needs a one-line why"


def test_no_golden_file_is_skipped_silently():
    for name, runner in LEGACY.items():
        assert (ROOT / "evals" / "tools" / name).exists(), f"{name} is listed as legacy but missing"
        assert (ROOT / runner).exists(), f"{name} is meant to be run by {runner}, which is missing"
    assert {f.name for f in ALL_FILES} == {f.name for f in FILES} | set(LEGACY)
