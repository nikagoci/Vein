import json
import sys
import time
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.answer import ask  # noqa: E402
from src.retrieve import ROOT  # noqa: E402


def main():
    th = float(sys.argv[1]) if len(sys.argv) > 1 else None
    results = []
    for g in yaml.safe_load(open(ROOT / "evals" / "golden.yaml", encoding="utf-8")):
        r = ask(g["question"], log_path=ROOT / "logs" / "golden.jsonl", threshold=th)
        if g["expect"] == "refuse":
            ok = not r["grounded"]
        else:
            ok = (r["grounded"]
                  and any(c["source"] == g["must_cite"] for c in r["citations"])
                  and g["must_mention"].lower() in r["answer"].lower())
        results.append({"id": g["id"], "pass": ok, "answer": r["answer"], "reason": r["reason"]})
        print(g["id"], "PASS" if ok else "FAIL", "-", g["question"])
    rate = sum(x["pass"] for x in results) / len(results)
    out = ROOT / "evals" / "results" / f"{time.strftime('%Y-%m-%d-%H%M')}-k2-t{th if th is not None else 0.3}.json"
    out.write_text(json.dumps({"pass_rate": rate, "results": results}, indent=2), encoding="utf-8")
    print(f"pass rate {rate:.2f} -> {out}")


if __name__ == "__main__":
    main()
