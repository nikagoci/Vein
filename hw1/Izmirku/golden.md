# Golden Questions — Vigenère Round-Trip CLI

## GQ1 — Round-trip with space
- Input: text = `hello world`, key = `key`
- Expected: encrypt shifts letters, space passes through, decrypt returns
  `hello world`, CLI prints `Round-trip: PASS`.
- Actual:
  ```
  Give the text: hello world
  Give the cipher key: key
  Encrypted: rijvs uyvjn
  Decrypted: hello world
  Round-trip: PASS
  ```
- Result: PASS

## GQ2 — Case preservation
- Input: text = `ABC`, key = `key`
- Expected: ciphertext is uppercase, round-trip returns `ABC`,
  CLI prints `Round-trip: PASS`.
- Actual:
  ```
  Give the text: ABC
  Give the cipher key: key
  Encrypted: KFA
  Decrypted: ABC
  Round-trip: PASS
  ```
- Result: PASS

## GQ3 — Invalid key (no letters)
- Input: text = `hello`, key = `123`
- Expected: program prints a clear error, no ciphertext printed.
- Actual:
  ```
  Give the text: hello
  Give the cipher key: 123
  Error: Key must contain at least one letter
  ```
- Result: PASS

## Notes on failures
No failures. GQ1 confirms the key stays aligned across non-letter
characters (the space); GQ2 confirms case is preserved; GQ3 confirms
invalid keys fail cleanly instead of raising an uncaught ValueError.


