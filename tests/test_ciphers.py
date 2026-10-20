import pytest

from src import caesar, rail_fence, vigenere


def test_caesar_known():
    assert caesar.encrypt("abc XYZ!", 3) == "def ABC!"
    assert caesar.decrypt("def", 3) == "abc"


def test_caesar_brute_force_contains_plaintext():
    assert caesar.brute_force(caesar.encrypt("hello", 7))[7] == "hello"


def test_caesar_rejects_non_int():
    with pytest.raises(ValueError):
        caesar.encrypt("a", "3")


def test_vigenere_known():
    assert vigenere.encrypt("attackatdawn", "lemon") == "lxfopvefrnhr"
    assert vigenere.decrypt("lxfopvefrnhr", "lemon") == "attackatdawn"


def test_vigenere_empty_key():
    with pytest.raises(ValueError):
        vigenere.encrypt("hi", "123")


def test_rail_known():
    assert rail_fence.encrypt_rail("WEAREDISCOVEREDFLEEATONCE", 3) == "WECRLTEERDSOEEFEAOCAIVDEN"


@pytest.mark.parametrize("text", ["hello*world", "a", "", "x" * 40])
@pytest.mark.parametrize("key", [1, 2, 5, 100])
def test_rail_round_trip(text, key):
    assert rail_fence.decrypt_rail(rail_fence.encrypt_rail(text, key), key) == text


@pytest.mark.parametrize("key", [0, -1, "2"])
def test_rail_bad_key(key):
    with pytest.raises(ValueError):
        rail_fence.encrypt_rail("abc", key)
