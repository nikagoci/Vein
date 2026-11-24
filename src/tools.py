# --- HW2: Vigenere encrypt tool (owner: nikagoci) -------------------------
from pydantic import BaseModel, Field, ConfigDict

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def _validate_key(key: str) -> str:
    """Strip non-letters, lowercase; raise if nothing remains."""
    cleaned = "".join(c for c in key.lower() if c.isalpha())
    if not cleaned:
        raise ValueError("Key must contain at least one letter. Try 'lemon'.")
    return cleaned


class EncryptInput(BaseModel):
    """Input contract for the vigenere_encrypt tool.

    Least-privilege: read-only. No user, student or account field.
    """
    model_config = ConfigDict(extra="forbid")

    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Plaintext to encrypt. Letters are shifted; other "
                    "characters pass through unchanged.",
    )
    key: str = Field(
        ...,
        min_length=1,
        max_length=64,
        pattern=r"^[A-Za-z]+$",
        description="Cipher key, letters only (a-z, A-Z). Example: 'lemon'.",
    )


def vigenere_encrypt(text: str, key: str) -> str:
    """Encrypt text with a Vigenere key. Pure, read-only, idempotent-safe."""
    key = _validate_key(key)
    key_i = 0
    out = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            x = ord(ch) - base
            y = ord(key[key_i]) - ord("a")
            out.append(chr(base + (x + y) % 26))
            key_i = (key_i + 1) % len(key)
        else:
            out.append(ch)
    return "".join(out)


def _run_encrypt(args: dict) -> dict:
    """Adapter used by call_tool() / the golden tests. Validates, then runs."""
    payload = EncryptInput(**args)
    return {"ciphertext": vigenere_encrypt(payload.text, payload.key)}


TOOLS["vigenere_encrypt"] = {
    "schema": EncryptInput,
    "handler": _run_encrypt,
    "consequential": False,
}


@mcp.tool()
def vigenere_encrypt_tool(text: str, key: str) -> dict:
    """Encrypt text with a Vigenere cipher key.

    Read-only. Refuses empty text, non-letter keys, and any extra fields.
    """
    return _run_encrypt({"text": text, "key": key})
# --- end HW2 --------------------------------------------------------------