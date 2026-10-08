"""Vigenere cipher with round-trip self-check.

Original cipher logic by me. Refactored so encrypt() and decrypt()
are pure functions, the CLI is wrapped in main(), and the program
prints an explicit PASS/FAIL on the round-trip.
"""

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def validate_key(key: str) -> str:
    key = key.lower()
    cleaned = "".join(c for c in key if c.isalpha())
    if not cleaned:
        raise ValueError("Key must contain at least one letter")
    return cleaned


def encrypt(text: str, key: str) -> str:
    key = validate_key(key)
    key_i = 0
    encrypted = ""
    for ch in text:
        if ch.islower():
            ch_lower = ch
            if ch_lower in ALPHABET:
                x = ALPHABET.find(ch_lower)
                y = ALPHABET.find(key[key_i])
                hold = ALPHABET[(x + y) % 26]
                encrypted = encrypted + hold
                key_i = (key_i + 1) % len(key)
        elif ch.isupper():
            ch_upper = ch.lower()
            if ch_upper in ALPHABET:
                x = ALPHABET.find(ch_upper)
                y = ALPHABET.find(key[key_i])
                hold = ALPHABET[(x + y) % 26]
                encrypted = encrypted + hold.upper()
                key_i = (key_i + 1) % len(key)
        else:
            encrypted += ch
    return encrypted


def decrypt(encrypted: str, key: str) -> str:
    key = validate_key(key)
    key_i = 0
    decrypted = ""
    for ch in encrypted:
        if ch.islower():
            ch_lower = ch
            if ch_lower in ALPHABET:
                x = ALPHABET.find(ch_lower)
                y = ALPHABET.find(key[key_i])
                hold = ALPHABET[(x - y) % 26]
                decrypted = decrypted + hold
                key_i = (key_i + 1) % len(key)
        elif ch.isupper():
            ch_upper = ch.lower()
            if ch_upper in ALPHABET:
                x = ALPHABET.find(ch_upper)
                y = ALPHABET.find(key[key_i])
                hold = ALPHABET[(x - y) % 26]
                decrypted = decrypted + hold.upper()
                key_i = (key_i + 1) % len(key)
        else:
            decrypted += ch
    return decrypted


def main() -> None:
    text = input("Give the text: ")
    raw_key = input("Give the cipher key: ")
    try:
        encrypted = encrypt(text, raw_key)
        decrypted = decrypt(encrypted, raw_key)
    except ValueError as e:
        print(f"Error: {e}")
        return

    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)
    print("Round-trip:", "PASS" if decrypted == text else "FAIL")


if __name__ == "__main__":
    main()
