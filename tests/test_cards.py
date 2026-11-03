import pytest

from uzkit.cards import (
    HUMO, MASTERCARD, UNIONPAY, UZCARD, VISA,
    card_type, format_card, is_valid_card, luhn_check, mask_card, normalize_card,
)

# Luhn bo'yicha to'g'ri, sun'iy (haqiqiy emas) raqamlar
UZ = "8600000000000007"
UZ_NFC = "5614000000000007"
HM = "9860000000000000"
HM_PUBLIC_TEST = "9860090101312172"
UZ_PUBLIC_TEST = "8600140407389072"
VS = "4111111111111111"
MC = "5555555555554444"
MC2 = "2221000000000009"
UP = "6200000000000005"


@pytest.mark.parametrize("number,expected", [
    (UZ, UZCARD), (UZ_NFC, UZCARD), (HM, HUMO),
    (VS, VISA), (MC, MASTERCARD), (MC2, MASTERCARD), (UP, UNIONPAY),
    ("8600 0000 0000 0007", UZCARD),
    ("9860-0000-0000-0000", HUMO),
    ("5100", MASTERCARD), ("2720", MASTERCARD),
    ("5600000000000000", None), ("2220000000000000", None),
    ("2721000000000000", None), ("1234567890123456", None),
    ("86", None), ("", None), ("abcd", None),
])
def test_card_type(number, expected):
    assert card_type(number) == expected


@pytest.mark.parametrize("bad", [None, 8600000000000007, [], b"8600"])
def test_non_string(bad):
    assert card_type(bad) is None
    assert is_valid_card(bad) is False
    assert normalize_card(bad) is None


@pytest.mark.parametrize("good", [
    UZ, UZ_NFC, HM, HM_PUBLIC_TEST, UZ_PUBLIC_TEST, VS, MC, MC2, UP,
    "8600 1404 0738 9072", "9860-0901-0131-2172",
])
def test_valid(good):
    assert is_valid_card(good) is True


@pytest.mark.parametrize("bad", [
    "8600000000000008",       # Luhn xato
    "860000000000007",        # Uzcard 15 xonali
    "86000000000000070",      # Uzcard 17 xonali
    "9860 0000 0000",         # qisqa
    "1234567890123452",       # noma'lum tur
    "8600 0000 0000 000X",    # harf
    "٨٦٠٠٠٠٠٠٠٠٠٠٠٠٠٠٧",    # arab-hind raqamlari
    "", " ",
])
def test_invalid(bad):
    assert is_valid_card(bad) is False


def test_luhn_check():
    assert luhn_check("79927398713") is True
    assert luhn_check("79927398710") is False


def test_format_and_mask():
    assert format_card(UZ) == "8600 0000 0000 0007"
    assert format_card("8600-0000 0000-0007") == "8600 0000 0000 0007"
    assert mask_card(UZ) == "8600 **** **** 0007"
    assert mask_card("9860 0901 0131 2172") == "9860 **** **** 2172"
    assert format_card("x") is None
    assert mask_card("1234") is None
