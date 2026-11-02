import pytest

from uzkit.validators import (
    MOBILE_OPERATOR_CODES,
    PLATE_REGION_CODES,
    is_valid_phone,
    is_valid_plate,
    normalize_phone,
)


# ---------------------------------------------------------------- telefon
@pytest.mark.parametrize(
    "value",
    [
        "+998901234567",
        "+998 90 123 45 67",
        "+998 (90) 123-45-67",
        "998901234567",
        "901234567",
        "90 123 45 67",
        "+998.91.123.45.67",
        "  +998931234567  ",
    ],
)
def test_valid_phone_formats(value):
    assert is_valid_phone(value) is True


@pytest.mark.parametrize("code", sorted(MOBILE_OPERATOR_CODES))
def test_every_operator_code_is_accepted(code):
    assert is_valid_phone(f"+998{code}1234567")


@pytest.mark.parametrize("code", ["90", "91", "93", "94", "95", "97", "99", "33", "88"])
def test_required_operator_codes_present(code):
    assert code in MOBILE_OPERATOR_CODES


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
        "+99890123456",  # juda qisqa
        "+9989012345678",  # juda uzun
        "+998 10 123 45 67",  # noma'lum operator kodi
        "+998 00 123 45 67",
        "+7 901 234 56 78",  # boshqa davlat
        "+901234567",  # 9 xonali, lekin '+' bilan
        "90123456",  # 8 xonali
        "+998 90 123 45 6a",
        "++998901234567",
        "+99890+1234567",
        "abcdefghijkl",
        "+٩٩٨٩٠١٢٣٤٥٦٧",  # arab-hind raqamlari
    ],
)
def test_invalid_phone(value):
    assert is_valid_phone(value) is False


@pytest.mark.parametrize("value", [None, 998901234567, 90.1, [], b"+998901234567"])
def test_non_string_phone(value):
    assert is_valid_phone(value) is False
    assert normalize_phone(value) is None


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("+998 90 123-45-67", "+998901234567"),
        ("998901234567", "+998901234567"),
        ("90 123 45 67", "+998901234567"),
        ("(93) 765-43-21", "+998937654321"),
        ("+998-33-111-22-33", "+998331112233"),
    ],
)
def test_normalize_phone(raw, expected):
    assert normalize_phone(raw) == expected


def test_normalize_phone_invalid_returns_none():
    assert normalize_phone("+998 10 123 45 67") is None
    assert normalize_phone("hello") is None


def test_normalize_is_idempotent():
    once = normalize_phone("90 123 45 67")
    assert normalize_phone(once) == once


# ----------------------------------------------------------- davlat raqami
@pytest.mark.parametrize(
    "value",
    [
        "01 A 123 AA",
        "01 123 AAA",
        "01A123AA",
        "01123AAA",
        "01 a 123 aa",
        "  30 B 456 CD  ",
        "95 Z 999 ZZ",
        "80 777 XYZ",
        "10 A 001 BC",
    ],
)
def test_valid_plate(value):
    assert is_valid_plate(value) is True


@pytest.mark.parametrize("code", sorted(PLATE_REGION_CODES))
def test_every_region_code_is_accepted(code):
    assert is_valid_plate(f"{code} A 123 AA")
    assert is_valid_plate(f"{code} 123 AAA")


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
        "00 A 123 AA",  # noma'lum viloyat kodi
        "99 123 AAA",
        "02 A 123 AA",
        "1 A 123 AA",  # viloyat kodi bitta raqam
        "001 A 123 AA",
        "01 AA 123 AA",
        "01 A 12 AA",
        "01 A 1234 AA",
        "01 A 123 A",
        "01 A 123 AAA",  # ikki format aralashgan
        "01 12 AAA",
        "01 1234 AAA",
        "01 123 AA",
        "01 123 AAAA",
        "01 1 123 AA",
        "A 01 123 AA",
        "01-A-123-AA",
        "01  A 123 AA",  # ikkita bo'shliq
        "01 А 123 АА",  # kirill harflari
    ],
)
def test_invalid_plate(value):
    assert is_valid_plate(value) is False


@pytest.mark.parametrize("value", [None, 123, [], b"01 A 123 AA"])
def test_non_string_plate(value):
    assert is_valid_plate(value) is False
