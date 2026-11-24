import argparse

from . import caesar, llm, rail_fence, vigenere
from .answer import ask


def main(argv=None):
    ap = argparse.ArgumentParser(prog="vein", description="Classical ciphers + grounded Q&A (educational only)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("encrypt", "decrypt"):
        p = sub.add_parser(name)
        p.add_argument("cipher", choices=["caesar", "vigenere", "rail"])
        p.add_argument("text")
        p.add_argument("key")
    q = sub.add_parser("ask")
    q.add_argument("question")
    q.add_argument("--live", action="store_true",
                   help="write the answer with the model in src/llm.py (needs OPENROUTER_API_KEY); "
                        "default: extract sentences from the sources, no model")
    a = ap.parse_args(argv)

    try:
        if a.cmd == "ask":
            r = ask(a.question, generate=llm.generate if a.live else None)
            print(r["answer"])
            for c in r["citations"]:
                print(f"  [{c['n']}] {c['source']}")
            return
        enc = a.cmd == "encrypt"
        if a.cipher == "caesar":
            f = caesar.encrypt if enc else caesar.decrypt
            print(f(a.text, int(a.key)))
        elif a.cipher == "vigenere":
            print((vigenere.encrypt if enc else vigenere.decrypt)(a.text, a.key))
        else:
            print((rail_fence.encrypt_rail if enc else rail_fence.decrypt_rail)(a.text, int(a.key)))
    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
