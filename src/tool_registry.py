"""Tool registry for the Vigenere capstone.

Single source of truth: EncryptInput, run_encrypt, TOOLS, call_tool,
and ToolInputError all live here. src/tools.py re-exports from this file.
"""

from pydantic import BaseModel, Field, ConfigDict, ValidationError


class ToolInputError(Exception):
    """Raised when a tool's input contract rejects the arguments."""
    pass


ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def _validate_key(key: str) -> str:
    cleaned = "".join(c for c in key.lower() if c.isalpha())
    if not cleaned:
        raise ToolInputError("invalid input")
    return cleaned


class EncryptInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Plaintext to encrypt."
    )
    key: str = Field(
        ...,
        min_length=1,
        max_length=64,
        pattern=r"^[A-Za-z]+$",
        description="Cipher key. Example: lemon."
    )


def vigenere_encrypt(text: str, key: str) -> str:
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


def run_encrypt(args: dict) -> dict:
    try:
        payload = EncryptInput(**args)
    except ValidationError:
        raise ToolInputError("invalid input") from None
    return {
        "ciphertext": vigenere_encrypt(payload.text, payload.key)
    }


TOOLS = {
    "encrypt_vigenere": {
        "schema": EncryptInput,
        "handler": run_encrypt,
        "consequential": False,
    }
}


def call_tool(name: str, arguments: dict) -> dict:
    """Call a registered tool by name."""
    if name not in TOOLS:
        raise ValueError(
            f"Unknown tool '{name}'. Check the available tool names and try again."
        )

    tool = TOOLS[name]
    try:
        validated = tool["schema"](**arguments)
    except ValidationError:
        raise ToolInputError("invalid input") from None
    return tool["handler"](validated.model_dump())