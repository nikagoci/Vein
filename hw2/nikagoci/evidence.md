# Evidence

## Golden test cases

Five cases in `evals/tools/nikagoci.yaml`, run by `tests/test_tool_golden.py`
through `call_tool()` (no model, no key) in the CI job required by the
branch rule. All five pass on `main`.

| #   | Test                                      | Input                                   | Expected result                     | Actual result                       | Status |
| --- | ----------------------------------------- | --------------------------------------- | ----------------------------------- | ----------------------------------- | ------ |
| 1   | Basic encryption with a valid key         | `text="attackatdawn"`, `key="lemon"`    | `{"ciphertext": "lxfopvefrnhr"}`    | `{"ciphertext": "lxfopvefrnhr"}`    | Pass   |
| 2   | Text with spaces and punctuation          | `text="Attack at dawn!"`, `key="lemon"` | `{"ciphertext": "Lxfopv ef rnhr!"}` | `{"ciphertext": "Lxfopv ef rnhr!"}` | Pass   |
| 3   | Uppercase key is normalized               | `text="hello"`, `key="LEMON"`           | `{"ciphertext": "sixzb"}`           | `{"ciphertext": "sixzb"}`           | Pass   |
| 4   | Empty key (bad input)                     | `text="hello"`, `key=""`                | `ToolInputError("invalid input")`   | `ToolInputError("invalid input")`   | Pass   |
| 5   | Adversarial: repeat call must be harmless | `text="hello"`, `key="lemon"`           | `{"ciphertext": "sixzb"}`           | `{"ciphertext": "sixzb"}`           | Pass   |

Local run:
$ python -m pytest tests/test_tool_golden.py -v
tests/test_tool_golden.py::test_tool_golden_cases PASSED
tests/test_tool_golden.py::test_tool_registry_rejects_unknown_tool PASSED
2 passed

## CI results

**Successful run **
Link: "https://github.com/nikagoci/Vein/actions/runs/45392505662/job/138439618697"

All checks passed — `tests / pytest (push)` succeeded in 12s, and the merge
button was enabled.

What I weakened: on the throwaway branch `hw2-red-nikagoci` I removed
`pattern=r"^[A-Za-z]+$"` from the `key` field in `EncryptInput`, pushed,
and opened a pull request. CI went red because the contract no longer
enforced the key format, and the merge button was blocked. I closed the
pull request without merging and deleted the branch.

## What I learned from the failed run

The red run proved the CI gate is real, not decorative: weakening the
contract on `key` turned the suite red and disabled the merge button, so a
bad contract cannot reach `main`. It also showed me that the schema and the
handler were doing overlapping work — with `pattern` removed, the bad-input
case still failed, but through the handler's `ToolInputError("invalid input")`
rather than the schema's `ValidationError`. That redundancy is intentional
(belt and suspenders), but the experiment made it visible: the schema is the
first line of defence, and the handler is the second. The lesson for the
write-up is that "the tests pass" is weaker evidence than "I broke the
contract and the tests caught it."
