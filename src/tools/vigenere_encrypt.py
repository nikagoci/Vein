"""Validated, least-privilege Vigenere encryption tool."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from src.vigenere import encrypt


class EncryptVigenereInput(BaseModel):
    """Only the plaintext and an English-letter key are accepted."""

    model_config = ConfigDict(extra="forbid", strict=True)

    text: str = Field(min_length=1, max_length=10_000)
    key: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z]+$")


class ToolInputError(ValueError):
    """Safe, actionable input error returned to the calling model."""


def encrypt_vigenere(arguments: dict) -> dict[str, str]:
    """Encrypt text with the Vigenere cipher and return the ciphertext."""
    try:
        data = EncryptVigenereInput.model_validate(arguments)
    except ValidationError as exc:
        errors = exc.errors()
        if any(error["type"] == "extra_forbidden" for error in errors):
            raise ToolInputError(
                "Unexpected argument. Send only 'text' and 'key'; do not include user or account identifiers."
            ) from None
        if any(error["loc"] == ("key",) for error in errors):
            raise ToolInputError(
                "Invalid key. Use 1–64 English letters (A–Z) only; remove spaces, digits, and punctuation."
            ) from None
        if any(error["loc"] == ("text",) for error in errors):
            raise ToolInputError(
                "Invalid text. Provide 1–10,000 characters, then try again."
            ) from None
        raise ToolInputError("Invalid input. Check 'text' and 'key' and try again.") from None

    try:
        ciphertext = encrypt(data.text, data.key)
    except ValueError:
        # Do not expose internal exceptions or implementation details.
        raise ToolInputError("Encryption failed. Check that the key contains English letters and try again.") from None

    return {"ciphertext": ciphertext}
