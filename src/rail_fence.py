def _check_key(key):
    if not isinstance(key, int) or key < 1:
        raise ValueError("Key must be an integer >= 1")


def _order(n, key):
    """Indices of the text in the order they are read off the rails."""
    rows = [[] for _ in range(key)]
    row, d = 0, 1
    for i in range(n):
        rows[row].append(i)
        if key > 1:
            if row == key - 1:
                d = -1
            elif row == 0:
                d = 1
            row += d
    return [i for r in rows for i in r]


def encrypt_rail(text, key):
    _check_key(key)
    return "".join(text[i] for i in _order(len(text), key))


def decrypt_rail(cipher, key):
    _check_key(key)
    out = [""] * len(cipher)
    for ch, i in zip(cipher, _order(len(cipher), key)):
        out[i] = ch
    return "".join(out)
