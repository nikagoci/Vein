# HW2 Tool Contract — `encrypt_vigenere`

## Purpose

Encrypt a supplied text using Vein's Vigenère cipher. This is an educational classical cipher, **not secure encryption**.

## Tool

- Name: `encrypt_vigenere`
- Implementation: [`src/tools/vigenere_encrypt.py`](../../src/tools/vigenere_encrypt.py)
- Cipher implementation: [`src/vigenere.py`](../../src/vigenere.py)
- Registry / local call door: [`src/tool_registry.py`](../../src/tool_registry.py)
- MCP server door: [`src/mcp_server.py`](../../src/mcp_server.py)

## Input contract

| Field  | Type and constraints                                     | Purpose         |
| ------ | -------------------------------------------------------- | --------------- |
| `text` | strict string, 1–10,000 characters                       | Text to encrypt |
| `key`  | strict string, 1–64 ASCII English letters (`A-Z`, `a-z`) | Vigenère key    |

Unknown fields are forbidden (`extra="forbid"`). No user, student, or account identity is accepted. There are no file, network, database, or external side effects.

## Output

A JSON object containing one field: `ciphertext` (string).

## Refusal and recovery

- Missing/empty/oversized text: asks for text between 1 and 10,000 characters.
- Invalid key: asks for 1–64 English letters and tells the caller to remove spaces, digits, and punctuation.
- Extra fields: refuses the unexpected argument and instructs the caller to send only `text` and `key`.

## Least privilege and autonomy

The tool computes ciphertext in memory and does not send, save, delete, or publish anything. No confirmation step is needed for this computation. The result must not be described as secure encryption.

## Limits

The Vigenère cipher is classical and can be broken; it must not be used to protect passwords, personal data, or real secrets.
