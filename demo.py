"""Interactive tour of every Vein feature.  Run:  python demo.py"""
import json
import subprocess
import sys

from src import caesar, rail_fence, vigenere
from src.answer import ask
from src.retrieve import ROOT

MENU = """
=== Vein: classical ciphers + grounded Q&A (educational only) ===
 1  Caesar          encrypt / decrypt
 2  Vigenere        encrypt / decrypt
 3  Rail Fence      encrypt / decrypt
 4  Caesar brute force (try all 25 shifts)
 5  Ask a question  (answers from data/corpus with citations, or refuses)
 6  Run unit tests
 7  Run golden set  (writes a result file in evals/results/)
 8  Show usage log  (last 10 lines)
 9  Quit
"""


def direction():
    while True:
        d = input("  (e)ncrypt or (d)ecrypt? ").strip().lower()
        if d in ("e", "d"):
            return d == "e"


def cipher_menu(name):
    text = input("  Text: ")
    key = input("  Key: ")
    enc = direction()
    try:
        if name == "caesar":
            f = caesar.encrypt if enc else caesar.decrypt
            out = f(text, int(key))
        elif name == "vigenere":
            out = (vigenere.encrypt if enc else vigenere.decrypt)(text, key)
        else:
            out = (rail_fence.encrypt_rail if enc else rail_fence.decrypt_rail)(text, int(key))
        print("  ->", out)
    except ValueError as e:
        print("  Error:", e)


def brute():
    text = input("  Ciphertext: ")
    for s, p in caesar.brute_force(text).items():
        print(f"  shift {s:2}: {p}")


def ask_loop():
    print("  Try: 'How does the Caesar cipher work?'  or an off-topic one. Empty line to go back.")
    while True:
        q = input("  Question: ").strip()
        if not q:
            return
        r = ask(q)
        print("  ", r["answer"])
        for c in r["citations"]:
            print(f"    [{c['n']}] {c['source']}")
        print(f"   grounded={r['grounded']}  reason={r['reason']}")


def run(cmd):
    subprocess.run([sys.executable, *cmd], cwd=ROOT)


def show_log():
    p = ROOT / "logs" / "usage.jsonl"
    if not p.exists():
        print("  No log yet. Ask a question first (option 5).")
        return
    for line in p.read_text(encoding="utf-8").splitlines()[-10:]:
        d = json.loads(line)
        print(f"  grounded={d['grounded']!s:5} score={d['top_score']:<5} {d['reason']:<16} {d['question']}")


ACTIONS = {
    "1": lambda: cipher_menu("caesar"),
    "2": lambda: cipher_menu("vigenere"),
    "3": lambda: cipher_menu("rail"),
    "4": brute,
    "5": ask_loop,
    "6": lambda: run(["-m", "pytest", "-q"]),
    "7": lambda: run(["evals/run_golden.py"]),
    "8": show_log,
}


def main():
    while True:
        print(MENU)
        choice = input("Choose 1-9: ").strip()
        if choice == "9":
            return
        action = ACTIONS.get(choice)
        if action:
            action()
        else:
            print("  Pick a number from 1 to 9.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print()
