

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def validate_key(key):
    key = key.lower()
    cleaned = "".join(c for c in key if c.isalpha())
    if not cleaned:
        raise ValueError("Key must contain at least one letter")
    return cleaned


def encrypt(text, key):
    key = validate_key(key)
    key_i = 0
    out = ""
    for ch in text:
        if ch.islower():
            x = ALPHABET.find(ch)
            y = ALPHABET.find(key[key_i])
            out += ALPHABET[(x + y) % 26]
            key_i = (key_i + 1) % len(key)
        elif ch.isupper():
            x = ALPHABET.find(ch.lower())
            y = ALPHABET.find(key[key_i])
            out += ALPHABET[(x + y) % 26].upper()
            key_i = (key_i + 1) % len(key)
        else:
            out += ch
    return out


def decrypt(encrypted, key):
    key = validate_key(key)
    key_i = 0
    out = ""
    for ch in encrypted:
        if ch.islower():
            x = ALPHABET.find(ch)
            y = ALPHABET.find(key[key_i])
            out += ALPHABET[(x - y) % 26]
            key_i = (key_i + 1) % len(key)
        elif ch.isupper():
            x = ALPHABET.find(ch.lower())
            y = ALPHABET.find(key[key_i])
            out += ALPHABET[(x - y) % 26].upper()
            key_i = (key_i + 1) % len(key)
        else:
            out += ch
    return out


def main():
    text = input("Give the text: ")
    raw_key = input("Give the cipher key: ")
    try:
        enc = encrypt(text, raw_key)
        dec = decrypt(enc, raw_key)
    except ValueError as e:
        print(f"Error: {e}")
        return
    print("Encrypted:", enc)
    print("Decrypted:", dec)
    print("Round-trip:", "PASS" if dec == text else "FAIL")


if __name__ == "__main__":
    main()
