# Pattern Journal · Izmirku · Weeks 5 to 7

*Written up on 24 November 2026 from my notes. I used Claude to turn my short notes into these entries; the points are mine.*

## Week 5 (19–25 Oct 2026) · Tool Contract

**Where I used it:** my HW2 tool `ask_cipher_docs`. It only accepts one thing, a question between 3 and 300 characters. Anything else, like a file path, `k`, the threshold or a user id, gets refused.

**What I noticed:** if the AI calling the tool could pick the file, it might read unrelated files or even malicious data. So the tool decides what it reads, not the model.

**Do differently:** turn on branch protection on `main` from the start, so a pull request with failing tests can't be merged.

## Week 6 (26 Oct – 1 Nov 2026) · Session State

**Where I used it:** my tool remembers nothing between questions, every call starts fresh. The tool log (`logs/tools.jsonl`) only stores how long the question was, not the words.

**What I noticed:** the older `ask()` still writes the full question text into `logs/usage.jsonl`.

**Do differently:** store less there. Somebody could accidentally type sensitive data into a question, and we don't want that kept in a log.

## Week 7 (2–8 Nov 2026) · Supervised Autonomy Loop

**Where I used it:** `ask_cipher_docs` only reads the notes, so an AI can call it without asking me first. Reading doesn't change anything.

**The action that must wait for a yes:** encrypting a file. Writing needs a yes, because on its own the AI could encrypt the wrong file.
