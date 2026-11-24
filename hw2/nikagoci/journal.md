# Pattern Journal — Nika Gotsiridze

## Week 5 — Tool Contract
- **Pattern:** Tool Contract.
- **Where I used it:** In my Vein HW2 tool, `encrypt_vigenere`, I kept the inputs limited to `text` and `key`. The contract also rejects extra fields, and one of the golden tests checks that a `user_id` field is refused.
- **What I learned:** A tool should only accept the information it actually needs. If the model sends extra information, the tool should not just ignore it; it should reject it and explain what to send instead.

## Week 6 — Session State
- **Pattern:** Session State.
- **Where I used it:** The Week 6 slides made me think about what our encryption tool actually needs to remember. For the current Vigenère tool, it does not need session memory: each call receives the text and key, encrypts the text, and returns the result. We do not need to keep the key or plaintext after the call.
- **What I learned:** Memory is something the application has to design, not something the model automatically has. If a product does store information, it should be clear who can access it, how long it stays, and how it can be deleted. For our current tool, not storing anything is simpler and safer.

## Week 7 — Supervised Autonomy Loop
- **Pattern:** Supervised Autonomy Loop.
- **Where I used it:** In `encrypt_vigenere`, the model can request encryption, but the code still checks the arguments before doing it. The golden tests check normal input, an invalid key, and an unexpected identity field, so the model cannot bypass the input rules just by sending different arguments.
- **One product action that must wait for a yes:** If we add an option to save encrypted text to a file, especially if it replaces an existing file, the app should ask the user to confirm before saving or overwriting it. Returning ciphertext in the current tool does not need that confirmation because it does not change or send anything outside the tool.
