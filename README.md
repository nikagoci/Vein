# Vein

Three classical ciphers (Caesar, Vigenère, Rail Fence) plus a small grounded Q&A layer. Educational only, not secure.

    pip install -r requirements.txt
    python -m pytest -q                       # 47 tests, all offline, no model, no key
    python evals/run_golden.py                # golden set -> evals/results/
    python -m src.cli encrypt vigenere "attack at dawn" lemon
    python -m src.cli ask "How does the Caesar cipher work?"

    # with a real model (OpenRouter); the key lives in your shell, never in a file
    export OPENROUTER_API_KEY=...             # optional: VEIN_MODEL=<openrouter model id>
    python -m src.cli ask --live "How does the Caesar cipher work?"
    python evals/run_golden.py --live         # writes ...-live.json, "mode": "live"

Layout: `src/` (ciphers, `retrieve.py`, `answer.py`, `llm.py`, `cli.py`) · `data/corpus/` (4 documents) · `tests/` · `evals/` · `docs/decisions/` · `logs/usage.jsonl` (one line per answer or refusal, and one `kind: "chat"` line per model call with tokens, cost and latency).

Grounding rules: refuse before any model call when no chunk scores above the threshold; every sentence must cite a retrieved `[n]`, otherwise the answer is refused. Answers are extracted from the sources by default; `--live` (or `generate=llm.generate` in `ask()`) uses the model in `src/llm.py`, and its output goes through the same citation check (`docs/decisions/0003-model-path-opt-in.md`).

Known limits: wrong-key decryption cannot be detected (see `data/corpus/limits.md`); retrieval is keyword-based, so synonyms are missed; the 0.3 threshold is tuned on five questions (see `docs/decisions/0002-threshold.md`).
