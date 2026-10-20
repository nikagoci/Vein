# 0002 — Retrieval threshold 0.3

- Status: accepted · Date: 2026-10-20

## Decision
Refusal threshold 0.3 (was 0.5).

## Why
Golden run at 0.5: 4/5 (see `evals/results/*-t0.5.json`); at 0.3: 5/5. g3 ("Why is Vigenere harder to break than Caesar?") scored 0.35 because "harder" is not in the corpus. The off-topic question (g5, password hashing) scores 0.19, so 0.3 still refuses it. Margin is thin; a larger corpus and golden set are needed before trusting it.
