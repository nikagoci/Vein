# HW1 Spec — Vigenère Round-Trip CLI

## Problem
I have a working Vigenère cipher in Python, but the original script
runs at import time, has no clean error handling for bad keys, and
never proves that encryption and decryption are exact inverses. A
reader has to trust the code without evidence. This feature wraps the
cipher in a small CLI that demonstrates the inverse property on real
inputs and fails cleanly on bad input.

## Users
- Me, verifying my own cipher implementation.
- A grader or teammate who wants to confirm the cipher works without
  reading the source.

## Success Criteria
1. Given text and a key, the CLI encrypts the text and prints the result.
2. It decrypts the ciphertext with the same key and prints the result.
3. It prints `Round-trip: PASS` if decrypted == original, else `FAIL`.
4. An invalid key (empty, or no letters) prints a clear error and exits
   without a traceback.

## Context List
- Python 3 standard library only. No pip installs.
- No files read or written; I/O via stdin/stdout.
- Alphabet a–z, modulo 26 arithmetic.
- Non-letter characters pass through unchanged and do NOT advance the
  key index.
- Case (upper/lower) preserved on both encrypt and decrypt.

## Acceptance Criteria
- Given text `hello world` and key `key`,
  when the CLI runs, then it prints `Round-trip: PASS`.
- Given text `ABC` and key `key`,
  when the CLI runs, then ciphertext is uppercase and case is preserved
  through the round-trip, and it prints `Round-trip: PASS`.
- Given key `123` (no letters),
  when the CLI runs, then it prints
  `Error: Key must contain at least one letter` and no ciphertext.

## Napkin Math
- 26 symbols in the alphabet.
- O(n) runtime in input length; n up to ~10^4 chars for a paragraph.
- No memory concerns beyond two copies of the input string.
