# HW2 · Tool contract · `ask_cipher_docs` · Izmirku

Vein's grounded Q&A (`ask()` in [`src/answer.py`](../../src/answer.py)) wrapped as a tool a model can call, through function calling and through MCP. The answer still comes only from `data/corpus/`, every sentence must cite a source, and the tool refuses when retrieval is too weak.

**In one sentence, for the model** (the docstring of [`AskCipherDocs`](../../src/contracts.py)): Answer a question about the Caesar, Vigenere or Rail Fence ciphers using only Vein's own documents, with numbered citations. Refuses when the documents do not cover the question. Reads only; changes nothing.

| | |
|---|---|
| **Effect** | reads |
| **Undo** | nothing to undo: it changes nothing |
| **Idempotent?** | yes: the same question gives the same result (`test_same_question_same_result`) |
| **Offered to** | every caller, visitor or signed in: it only reads public cipher notes (`tools_for()` in [`src/doc_tools.py`](../../src/doc_tools.py)) |
| **Identity from** | not needed. There is no identity field; the function-calling door takes the caller from the app (`call_tool(..., caller)`), never from the arguments |
| **Touches** | the four files in `data/corpus/` (read) and the answer log `ask()` already writes. No path, file name, k, threshold or model can be chosen by the caller |
| **Must never** | answer from anything except `data/corpus/`, or return an answer that failed `check_citations()` |
| **Read or consequential?** | read. It cannot book, send, pay, publish or delete, so a loop may call it without a person's yes |

**Inputs.** `extra="forbid"`: any other argument is refused.

| Argument | Type | Constraint | Description the model reads |
|---|---|---|---|
| `question` | string | 3 to 300 characters, pattern `^[^\x00-\x1f\x7f]+$` (no control characters) | The question, in plain words. Example: How does the Caesar cipher work? |

**Result** ([`DocAnswer`](../../src/doc_tools.py)): `answer` (string), `citations` (list of `{n, source}`), `grounded` (bool), `reason` (`ok`, `below threshold`, `uncited sentence`, `unknown citation`). A refusal is a normal result with `grounded: false`, not an error, so the model tells the person the notes do not cover it instead of retrying.

**Expected failures** (in `{ok: false, error}` from [`call_tool()`](../../src/act.py), or `ToolError` through MCP):

| When | Message the model reads |
|---|---|
| question too short, too long, wrong type, has a newline | `invalid arguments: question: <what is wrong>. Send only: question, as described in the tool schema.` |
| an extra argument (`corpus_path`, `k`, `user_id`...) | `invalid arguments: <field>: Extra inputs are not permitted. Send only: question, ...` |
| a tool that was not offered | `no tool named '<name>' is available. Available tools: ask_cipher_docs.` |
| the server runs with the live model but has no key | `The answer model is not available on this server right now. Try again later, or answer without this tool.` |

**Tests and golden cases.**

| Case | Expect | Where |
|---|---|---|
| a valid call | runs, cites `caesar.md` | `tests/test_ask_tool.py::test_valid_call_runs_and_cites_corpus_files`, golden n1, n2 |
| a question the notes do not cover | result with `grounded: false` | golden n3 |
| invalid arguments | refused before the tool runs | `test_invalid_arguments_never_reach_the_tool` (8 variants), golden b1 |
| not offered to this caller | refused, nothing runs | `test_tool_not_offered_never_runs` |
| identity in the arguments | refused | `test_identity_is_not_an_argument` |
| adversarial: "ignore the corpus" injection | still refused below the threshold | golden a1, `test_injection_gets_a_refusal_or_only_corpus_sentences` |
| adversarial: `corpus_path: "../../.env"` | refused | golden a2 |
| both doors describe it the same way | identical schema | `tests/test_mcp.py` |

Golden file: [`evals/tools/Izmirku.yaml`](../../evals/tools/Izmirku.yaml), run in CI by [`tests/test_tool_golden_template.py`](../../tests/test_tool_golden_template.py).

**Log line.** One line per call in `logs/tools.jsonl`: time, tool, ok, error, a hash of the caller (or null), the number of characters in the arguments, latency. It deliberately leaves out the question text, because a person can type anything into it (`test_one_log_line_per_call_without_the_question_text`).

**Limits.** Retrieval is keyword-based: a typo or a synonym can lower the score and cause a refusal (decision 0002). Extra words in a question lower the score too, which is why most injected instructions end in a refusal.
