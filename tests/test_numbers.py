import pytest

from uzkit import number_to_words, ordinal
from uzkit.translit import OKINA

O = OKINA

CARDINALS = [
    (0, "nol"),
    (1, "bir"),
    (7, "yetti"),
    (10, f"o{O}n"),
    (14, f"o{O}n to{O}rt"),
    (20, "yigirma"),
    (40, "qirq"),
    (80, "sakson"),
    (90, f"to{O}qson"),
    (100, "bir yuz"),
    (101, "bir yuz bir"),
    (1000, "bir ming"),
    (1250, "bir ming ikki yuz ellik"),
    (2024, f"ikki ming yigirma to{O}rt"),
    (1_000_000, "bir million"),
    (1_000_001, "bir million bir"),
    (1_000_000_000, "bir milliard"),
    (
        12_345_678,
        f"o{O}n ikki million uch yuz qirq besh ming olti yuz yetmish sakkiz",
    ),
]


@pytest.mark.parametrize("n,words", CARDINALS)
def test_number_to_words(n, words):
    assert number_to_words(n) == words


@pytest.mark.parametrize("n", [1, 5, 99, 1000, 123456])
def test_negative(n):
    assert number_to_words(-n) == "minus " + number_to_words(n)


ORDINALS = [
    (1, "birinchi"),
    (2, "ikkinchi"),
    (3, "uchinchi"),
    (4, f"to{O}rtinchi"),
    (5, "beshinchi"),
    (6, "oltinchi"),
    (7, "yettinchi"),
    (8, "sakkizinchi"),
    (9, f"to{O}qqizinchi"),
    (10, f"o{O}ninchi"),
    (20, "yigirmanchi"),
    (40, "qirqinchi"),
]


@pytest.mark.parametrize("n,words", ORDINALS)
def test_ordinal(n, words):
    assert ordinal(n) == words