from pathlib import Path

import pytest
import yaml

from src.tool_registry import call_tool
from src.tools import ToolInputError


GOLDEN_FILE = Path(__file__).resolve().parents[1] / "evals" / "tools" / "nikagoci.yaml"


def test_tool_golden_cases():
    data = yaml.safe_load(GOLDEN_FILE.read_text(encoding="utf-8"))
    assert data["tool"] == "encrypt_vigenere"
    assert len(data["cases"]) == 5

    for case in data["cases"]:
        if "expect_error" in case:
            with pytest.raises(ToolInputError, match="^" + __import__("re").escape(case["expect_error"]) + "$"):
                call_tool(data["tool"], case["arguments"])
        else:
            assert call_tool(data["tool"], case["arguments"]) == case["expect"], case["name"]


def test_tool_registry_rejects_unknown_tool():
    with pytest.raises(ValueError, match="Unknown tool"):
        call_tool("delete_everything", {})
