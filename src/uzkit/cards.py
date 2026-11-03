"""Bank karta raqamlarini aniqlash va tekshirish (Uzcard, Humo va xalqaro)."""

from __future__ import annotations

from typing import Optional

UZCARD = "Uzcard"
HUMO = "Humo"
VISA = "Visa"
MASTERCARD = "Mastercard"
UNIONPAY = "UnionPay"

_SEPARATORS = (" ", "-")


def normalize_card(number: str) -> Optional[str]:
    """Karta raqamidan bo'shliq va tirelarni olib tashlaydi.

    Faqat raqamlardan iborat satrni qaytaradi, aks holda ``None``.

    >>> normalize_card("8600 1234 5678 9012")
    '8600123456789012'
    """
    if not isinstance(number, str):
        return None
    digits = number
    for sep in _SEPARATORS:
        digits = digits.replace(sep, "")
    if not digits or not (digits.isascii() and digits.isdigit()):
        return None
    return digits


def luhn_check(digits: str) -> bool:
    """Luhn kontrol yig'indisini tekshiradi (``digits`` faqat raqamlar bo'lsin)."""
    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def card_type(number: str) -> Optional[str]:
    """Karta turini boshlang'ich raqamlari (BIN) bo'yicha aniqlaydi.

    ``"Uzcard"``, ``"Humo"``, ``"Visa"``, ``"Mastercard"``, ``"UnionPay"``
    yoki aniqlab bo'lmasa ``None``. Kontrol yig'indisi tekshirilmaydi,
    buning uchun :func:`is_valid_card` dan foydalaning.

    >>> card_type("8600 1234 5678 9012")
    'Uzcard'
    """
    digits = normalize_card(number)
    if digits is None:
        return None
    if digits[:4] in ("8600", "5614"):
        return UZCARD
    if digits[:4] == "9860":
        return HUMO
    if digits[:1] == "4":
        return VISA
    if len(digits) >= 2 and "51" <= digits[:2] <= "55":
        return MASTERCARD
    if len(digits) >= 4 and "2221" <= digits[:4] <= "2720":
        return MASTERCARD
    if digits[:2] == "62":
        return UNIONPAY
    return None


def is_valid_card(number: str) -> bool:
    """Karta raqami turi, uzunligi va Luhn yig'indisi bo'yicha to'g'rimi.

    Uzcard va Humo uchun uzunlik 16 ta raqam. Bu raqam haqiqatda mavjud
    yoki faol ekanini bildirmaydi, faqat formatini tekshiradi.
    """
    digits = normalize_card(number)
    if digits is None:
        return False
    kind = card_type(digits)
    if kind is None:
        return False
    if kind in (UZCARD, HUMO) and len(digits) != 16:
        return False
    if not 13 <= len(digits) <= 19:
        return False
    return luhn_check(digits)


def format_card(number: str) -> Optional[str]:
    """Raqamni 4 tadan guruhlab yozadi: ``8600 1234 5678 9012``."""
    digits = normalize_card(number)
    if digits is None:
        return None
    return " ".join(digits[i : i + 4] for i in range(0, len(digits), 4))


def mask_card(number: str) -> Optional[str]:
    """Raqamning o'rtasini yashiradi: ``8600 **** **** 9012``."""
    digits = normalize_card(number)
    if digits is None or len(digits) < 8:
        return None
    hidden = digits[:4] + "*" * (len(digits) - 8) + digits[-4:]
    return " ".join(hidden[i : i + 4] for i in range(0, len(hidden), 4))
