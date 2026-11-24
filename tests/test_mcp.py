"""The MCP door (SDK 2, in-memory Client): same contract as the function-calling door,
read-only annotations, errors that reach the model as text. Plus a regression check that
Nika's encrypt_vigenere still works after the move to SDK 2."""
import asyncio

from mcp import Client

from src.doc_tools import DOC_TOOLS
from src.mcp_server import mcp


def run(coro):
    return asyncio.run(coro)


async def listed():
    async with Client(mcp) as c:
        return {t.name: t for t in (await c.list_tools()).tools}


async def call(name, args):
    async with Client(mcp) as c:
        return await c.call_tool(name, args)


def strip(schema):
    return {k: {kk: vv for kk, vv in v.items() if kk != "title"} for k, v in schema["properties"].items()}


def test_server_lists_both_hw2_tools():
    assert set(run(listed())) == {"ask_cipher_docs", "encrypt_vigenere"}


def test_both_doors_describe_ask_cipher_docs_identically():
    mcp_schema = run(listed())["ask_cipher_docs"].input_schema
    fc_schema = DOC_TOOLS["ask_cipher_docs"].schema()["function"]["parameters"]
    assert strip(mcp_schema) == strip(fc_schema)
    assert set(mcp_schema.get("required", [])) == set(fc_schema.get("required", []))
    assert run(listed())["ask_cipher_docs"].description == DOC_TOOLS["ask_cipher_docs"].schema()["function"]["description"]


def test_ask_cipher_docs_is_marked_read_only():
    a = run(listed())["ask_cipher_docs"].annotations
    assert a.read_only_hint is True and a.destructive_hint is False and a.open_world_hint is False


def test_answer_through_mcp():
    r = run(call("ask_cipher_docs", {"question": "How does the Caesar cipher work?"}))
    assert not r.is_error
    assert r.structured_content["grounded"] is True
    assert r.structured_content["citations"][0]["source"] == "caesar.md"


def test_refusal_through_mcp_is_a_result():
    r = run(call("ask_cipher_docs", {"question": "What is the best way to hash passwords?"}))
    assert not r.is_error and r.structured_content["grounded"] is False


def test_bad_arguments_are_rejected_through_mcp():
    r = run(call("ask_cipher_docs", {"question": "x" * 301}))
    assert r.is_error


def test_an_extra_argument_changes_nothing_through_mcp():
    """The SDK drops unknown arguments; the function-calling door refuses them. Either way the
    path never reaches the tool: the answer is the same as without it."""
    plain = run(call("ask_cipher_docs", {"question": "How does the Caesar cipher work?"}))
    smuggled = run(call("ask_cipher_docs", {"question": "How does the Caesar cipher work?",
                                            "corpus_path": "../../.env"}))
    assert smuggled.is_error or smuggled.structured_content == plain.structured_content


def test_nikas_encrypt_vigenere_still_works_after_sdk2_move():
    r = run(call("encrypt_vigenere", {"text": "attackatdawn", "key": "lemon"}))
    assert not r.is_error and r.structured_content == {"ciphertext": "lxfopvefrnhr"}
