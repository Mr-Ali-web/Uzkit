from decimal import Decimal

import pytest

from uzkit import format_money, money_to_words
from uzkit.translit import OKINA

SOM = f"so{OKINA}m"


@pytest.mark.parametrize("amount,expected", [
    (0, f"nol {SOM}"),
    (1250, f"bir ming ikki yuz ellik {SOM}"),
    ("1250.50", f"bir ming ikki yuz ellik {SOM} ellik tiyin"),
    (Decimal("0.05"), f"nol {SOM} besh tiyin"),
    (-100, f"minus bir yuz {SOM}"),
    (1_000_000, f"bir million {SOM}"),
])
def test_money_to_words(amount, expected):
    assert money_to_words(amount) == expected


def test_without_tiyin():
    assert money_to_words(10.75, with_tiyin=False) == f"o{OKINA}n {SOM}"


def test_float_precision():
    assert money_to_words(0.1 + 0.2) == f"nol {SOM} o{OKINA}ttiz tiyin"


@pytest.mark.parametrize("bad", [None, True, [1], {}])
def test_bad_type(bad):
    with pytest.raises(TypeError):
        money_to_words(bad)


@pytest.mark.parametrize("amount,expected", [
    (1250000, f"1 250 000 {SOM}"),
    (999, f"999 {SOM}"),
    ("1500.5", f"1 500,50 {SOM}"),
    (-2000, f"-2 000 {SOM}"),
])
def test_format_money(amount, expected):
    assert format_money(amount) == expected
    