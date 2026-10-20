

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def encrypt(text, shift):
    if not isinstance(shift, int):
        raise ValueError("Shift must be an integer")
    shift %= 26
    out = ""
    for ch in text:
        if ch.islower():
            out += ALPHABET[(ALPHABET.index(ch) + shift) % 26]
        elif ch.isupper():
            out += ALPHABET[(ALPHABET.index(ch.lower()) + shift) % 26].upper()
        else:
            out += ch
    return out


def decrypt(encrypted, shift):
    return encrypt(encrypted, -shift)


def brute_force(cipher):
    return {s: decrypt(cipher, s) for s in range(1, 26)}


def main():
    text = input("Give your text: ")
    while True:
        try:
            shift = int(input("Give shift value: "))
            break
        except ValueError:
            print("not a valid shift value")
    enc = encrypt(text, shift)
    print("Encrypted:", enc)
    print("Decrypted:", decrypt(enc, shift))
    print("---BRUTEFORCE_RESULTS---")
    for s, p in brute_force(enc).items():
        print("Shift:", s, "decrypted", p)


if __name__ == "__main__":
    main()
