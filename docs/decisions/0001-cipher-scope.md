# 0001 — Cipher scope

- Status: accepted
- Date: 2026-10-20

## Decision
In scope: Vigenère, Rail Fence, Caesar.
Out of scope: atbash, ROT13, other ciphers.

## Why
Three ciphers cover substitution (Caesar), polyalphabetic (Vigenère) and transposition (Rail Fence) — enough to teach the core ideas, small enough to test thoroughly. 

## Consequences
src/ contains exactly three cipher modules. Design Review §1 cites pytest as the correctness evidence.
