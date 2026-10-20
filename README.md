# Vein

Three classical ciphers (Caesar, Vigenère, Rail Fence) plus a small grounded Q&A layer. Educational only, not secure.

    pip install pytest pyyaml
    python -m pytest -q                       # 30 tests, all offline
    python evals/run_golden.py                # golden set -> evals/results/
    python -m src.cli encrypt vigenere "attack at dawn" lemon
    python -m src.cli ask "How does the Caesar cipher work?"

Layout: `src/` (ciphers, `retrieve.py`, `answer.py`, `cli.py`) · `data/corpus/` (4 documents) · `tests/` · `evals/` · `docs/decisions/` · `logs/usage.jsonl` (one line per answer or refusal).

Grounding rules: refuse before any model call when no chunk scores above the threshold; every sentence must cite a retrieved `[n]`, otherwise the answer is refused. Answers are extracted from the sources by default; pass `generate=` to `ask()` to plug in a model, and its output goes through the same citation check.

Known limits: wrong-key decryption cannot be detected (see `data/corpus/limits.md`); retrieval is keyword-based, so synonyms are missed; the 0.3 threshold is tuned on five questions (see `docs/decisions/0002-threshold.md`).
