"""O'zbekiston telefon raqamlari va avtomobil davlat raqamlarini tekshirish."""

from __future__ import annotations

import re
from typing import Any, Optional

__all__ = [
    "MOBILE_OPERATOR_CODES",
    "is_valid_phone",
    "is_valid_plate",
    "normalize_phone",
]

COUNTRY_CODE = "998"

#: Mobil operator kodlari (+998 XX ...).
MOBILE_OPERATOR_CODES = frozenset(
    {
        "20",  # Sardor Telecom / OQ
        "33",  # Humans
        "50",  # Ucell
        "55",  # Ucell; VoIP (Uztelecom), mobil emas
        "77",  # Uzmobile
        "88",  # Mobiuz / Humans
        "90",  # Beeline
        "91",  # Beeline
        "93",  # Ucell
        "94",  # Ucell
        "95",  # Uzmobile
        "97",  # Mobiuz
        "98",  # Mobiuz
        "99",  # Uzmobile
    }
)

# Raqamlar orasida ruxsat etilgan ajratuvchilar: bo'shliq, tire, nuqta, qavs.
_PHONE_SEPARATORS = re.compile(r"[\s\-.()]+")
_PHONE_BODY = re.compile(r"\+?[0-9]+", re.ASCII)

# 01 A 123 AA (jismoniy shaxs) va 01 123 AAA (yuridik shaxs)
_PLATE_PERSONAL = re.compile(r"(\d{2}) ?([A-Z]) ?(\d{3}) ?([A-Z]{2})", re.ASCII)
_PLATE_LEGAL = re.compile(r"(\d{2}) ?(\d{3}) ?([A-Z]{3})", re.ASCII)


def normalize_phone(phone: Any) -> Optional[str]:
    """Telefon raqamini ``+998XXXXXXXXX`` ko'rinishiga keltiradi.

    Qabul qilinadigan kiritishlar (bo'shliq, tire, nuqta va qavslar e'tiborga
    olinmaydi)::

        +998 90 123-45-67
        998901234567
        90 123 45 67        (milliy 9 xonali format)

    Raqam noto'g'ri bo'lsa (yoki ``str`` bo'lmasa) ``None`` qaytariladi.
    Faqat mobil operator kodlari (:data:`MOBILE_OPERATOR_CODES`) qabul qilinadi.
    """
    if not isinstance(phone, str):
        return None

    cleaned = _PHONE_SEPARATORS.sub("", phone)
    if not _PHONE_BODY.fullmatch(cleaned):
        return None

    digits = cleaned[1:] if cleaned.startswith("+") else cleaned

    if len(digits) == 12 and digits.startswith(COUNTRY_CODE):
        national = digits[len(COUNTRY_CODE):]
    elif len(digits) == 9 and not cleaned.startswith("+"):
        national = digits
    else:
        return None

    if national[:2] not in MOBILE_OPERATOR_CODES:
        return None

    return f"+{COUNTRY_CODE}{national}"


def is_valid_phone(phone: Any) -> bool:
    """Telefon raqami O'zbekiston mobil raqami ekanini tekshiradi.

    >>> is_valid_phone("+998 90 123 45 67")
    True
    >>> is_valid_phone("+998 10 123 45 67")
    False
    """
    return normalize_phone(phone) is not None


def is_valid_plate(plate: Any) -> bool:
    """Avtomobil davlat raqamini tekshiradi.

    Qo'llab-quvvatlanadigan formatlar::

        01 A 123 AA     (jismoniy shaxslar)
        01 123 AAA      (yuridik shaxslar)

    Bo'shliqlar ixtiyoriy (``01A123AA``), harflar katta-kichikligi farqlanmaydi.
    Viloyat kodi 00 dan farqli ikki xonali kod bo'lishi shart (01-99).
    """
    if not isinstance(plate, str):
        return False

    value = plate.strip().upper()
    match = _PLATE_PERSONAL.fullmatch(value) or _PLATE_LEGAL.fullmatch(value)
    if match is None:
        return False

    code = match.group(1)
    return code != "00" and code.isdigit() and len(code) == 2
