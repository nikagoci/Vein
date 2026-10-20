# Delegation Log

## 2026-10-20 · Refactoring cipher scripts
**What I delegated:** I asked an AI agent to refactor my raw cipher scripts (which used module-level `input()` and `print()`) into pure functions wrapped in a `main()` block, and to generate a `pytest` test suite for known-answer and round-trip verification.
**Rung:** 3. The agent wrote the code; I reviewed the result.
**What came back wrong:** The refactor looked clean but had gaps against my own spec. Rail Fence marked empty cells with `"*"`, so any text containing `*` could not round-trip. Rail Fence accepted `key = 0` (crash) and any non-integer key. Caesar accepted a non-integer shift. Nothing in the three ciphers could meet AC2 ("wrong-key decrypt returns an explicit value, never silent garbage"), because classical ciphers cannot detect a wrong key.
**How I caught it:** I compared each module against `docs/spec.md` acceptance criterion by criterion, then reviewed the code for edge cases (special characters, key 0, key longer than the text).
**What I changed:** Rail Fence now places characters by index (no sentinel) and rejects keys below 1; Caesar rejects non-integer shifts; AC2 was reworded to "invalid keys raise `ValueError`" and the wrong-key limit is documented in `data/corpus/limits.md`. New tests cover `*` in the input, bad keys and keys larger than the text.

## 2026-10-20 · Grounded Q&A layer (retrieval, citations, refusal, logging)
**What I delegated:** I asked an AI agent to build the planned AC3 and AC4 features on top of the ciphers: a small corpus, retrieval with scores, a reply `{answer, citations, grounded}`, a citation check, refusal before any model call, one log line per answer or refusal, a golden set with a runner, and offline tests.
**Rung:** 3. The agent wrote the code; I reviewed the diff and ran the tests and the golden set myself before merging.
**What came back wrong:**
- The first golden run passed only 3/5. "How does the Caesar cipher work?" was refused because the word "work" was not in the corpus and counted against the match score.
- At the starting threshold of 0.5, "Why is Vigenere harder to break than Caesar?" was also refused (score 0.35).
- Paths were relative to the current directory, so running from another folder failed to find the corpus and results.
- Tests wrote a stray log file into the repo.
- The extractive answer to the Caesar question also included a Vigenère sentence, because both documents mention Caesar.
**How I caught it:** the golden set run (failures printed per question), then running tests and the runner from different folders, and reading the answers rather than only the pass flags.
**What I changed:** added "work" to the stopword list; lowered the threshold to 0.3 after comparing runs, recorded in `docs/decisions/0002-threshold.md` (4/5 at 0.5, 5/5 at 0.3, refusal case scores 0.19); anchored all paths to the repo root; moved test logs to a temporary folder. The extra Vigenère sentence is a known limit of keyword retrieval, listed in the Design Review risks.
**Still open:** no real model is connected, so token counts and cost are not yet measured.
