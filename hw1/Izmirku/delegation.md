# Delegation Log — HW1

## What I handed to AI

**Prompt 1 (spec):**
> "I have a working Vigenère cipher in Python. I want to turn it into a
> small CLI feature for a homework assignment. The feature should take
> text and a key, encrypt, decrypt with the same key, and print PASS/FAIL
> on the round-trip. Write a one-page spec with problem, users, success
> criteria, context list, acceptance criteria, and napkin math."

**Prompt 2 (code refactor):**
> "Here is my original Viegener cipher.py. Refactor it minimally so that:
> (1) validate_key is called inside encrypt and decrypt instead of at
> module level; (2) the CLI is wrapped in main() guarded by
> `if __name__ == '__main__':`; (3) invalid keys produce a clean error
> instead of a traceback; (4) add a `Round-trip: PASS/FAIL` print.
> Keep the cipher math unchanged."



## What came back wrong (or needed fixing)

1. The first refactor kept `validate_key` at module level, so an
   invalid key still crashed at import. I asked for validation to move
   inside `encrypt`/`decrypt` and to be wrapped in `try/except` in
   `main()`. GQ3 catches this.
2. The agent initially suggested using `enumerate` and a dict to look
   up indices. I kept my original `alphabet.find()` loops to preserve
   my own code style — the point is a minimal refactor, not a rewrite.

## How I caught it

- Read the agent's output line-by-line against `spec.md` acceptance
  criteria.
- Ran all three golden questions manually and pasted real output into
  `golden.md`.
- Compared the refactored cipher output against my original script on
  the same inputs — cipher math is identical.

## What I'd delegate differently next time

- Write the acceptance criteria before asking the agent to write
  code. The first draft drifted because the contract wasn't pinned.
- Ask for the diff, not a full rewrite, so changes stay reviewable.
