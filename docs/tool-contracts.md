# Tool contracts · Vein

Every rule in a contract exists in code. One section per tool; the full one-page contract is in each owner's HW2 folder.

## `ask_cipher_docs` (reads)

Answers a question about the three ciphers from `data/corpus/` only, with citations, or refuses. One argument, `question` (3 to 300 characters, no control characters), `extra="forbid"`. Offered to every caller; no identity. Contract: [`src/contracts.py`](../src/contracts.py) · tool: [`src/doc_tools.py`](../src/doc_tools.py) · gates and log: [`src/act.py`](../src/act.py) · MCP: [`src/mcp_server.py`](../src/mcp_server.py). Full contract: [`hw2/Izmirku/contract.md`](../hw2/Izmirku/contract.md).

## `encrypt_vigenere` (computes, changes nothing)

Contract and handler: [`src/tool_registry.py`](../src/tool_registry.py). Full contract: [`hw2/nikagoci/contract.md`](../hw2/nikagoci/contract.md).

## HW2 owners

| Member | GitHub | Function wrapped | Golden cases |
|---|---|---|---|
| Nika Gotsiridze | @nikagoci | `encrypt_vigenere` | `evals/tools/nikagoci.yaml` |
| Saba Abesadze | @Izmirku | `ask_cipher_docs` (grounded `ask()`) | `evals/tools/Izmirku.yaml` |
