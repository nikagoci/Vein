# 0003 — One model path, opt-in

- Status: accepted · Date: 2026-11-24

## Decision
Every model call goes through `src/llm.py`, plugged into the existing `generate=` hook of `ask()`. The default answer path stays extractive (no model). The model is used only when asked for: `python -m src.cli ask --live "..."`, `VEIN_LIVE=1 python demo.py`, `python evals/run_golden.py --live`.

## Why
- The grounding safeguards stay exactly as they are: below the 0.3 threshold no model is called (`test_below_threshold_the_model_is_never_called`), and every model answer goes through `check_citations()` and is refused if it fails (`test_bad_model_output_is_refused_by_check_citations`, `test_live_answer_still_goes_through_check_citations`).
- The default stays free, deterministic and runnable without a key, so the committed golden results (decision 0002) stay reproducible and CI needs no secret.
- One usage line per model call in `logs/usage.jsonl` (`kind: "chat"`, model, tokens in/out, `cost_usd`, `latency_ms`) is the evidence for the Design Review token budget.

## Consequences
- Tests never call a real model: `tests/conftest.py` sets `VEIN_OFFLINE=1` (a fake model) and removes `OPENROUTER_API_KEY` for every test.
- `logs/usage.jsonl` now holds two kinds of line: answer lines (no `kind` field, written by `answer.py`) and model-call lines (`kind: "chat"`). `demo.py` option 8 shows both.
- Prices in `PRICES` are copied from the course reference (13 October 2026) and must be re-checked before costs are reported. A model with no price logs `cost_usd: null`, not 0.
- Live golden results are written with a `-live` suffix and `"mode": "live"`, so they are never confused with extractive runs.
