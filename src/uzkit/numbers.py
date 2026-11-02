"""Sonlarni o'zbekcha so'zlar bilan yozish (0 dan 10**12 gacha)."""

from __future__ import annotations

from typing import List

from uzkit.translit import OKINA

__all__ = ["MAX_NUMBER", "number_to_words", "ordinal"]

#: Qo'llab-quvvatlanadigan eng katta son (modul bo'yicha).
MAX_NUMBER = 10**12

_ONES = (
    "",
    "bir",
    "ikki",
    "uch",
    f"to{OKINA}rt",
    "besh",
    "olti",
    "yetti",
    "sakkiz",
    f"to{OKINA}qqiz",
)

_TENS = (
    "",
    f"o{OKINA}n",
    "yigirma",
    f"o{OKINA}ttiz",
    "qirq",
    "ellik",
    "oltmish",
    "yetmish",
    "sakson",
    f"to{OKINA}qson",
)

_SCALES = (
    (10**12, "trillion"),
    (10**9, "milliard"),
    (10**6, "million"),
    (10**3, "ming"),
)

_VOWELS = frozenset("aeiou")


def _validate(n: object) -> None:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, not {type(n).__name__}")
    if abs(n) > MAX_NUMBER:
        raise ValueError(f"n must be within [-{MAX_NUMBER}, {MAX_NUMBER}], got {n}")


def _below_thousand(n: int) -> List[str]:
    """1..999 oralig'idagi sonni so'zlar ro'yxati sifatida qaytaradi."""
    words: List[str] = []
    hundreds, rest = divmod(n, 100)
    if hundreds:
        words += [_ONES[hundreds], "yuz"]
    tens, ones = divmod(rest, 10)
    if tens:
        words.append(_TENS[tens])
    if ones:
        words.append(_ONES[ones])
    return words


def number_to_words(n: int) -> str:
    """Butun sonni o'zbekcha so'zlar bilan yozadi.

    >>> number_to_words(1250)
    'bir ming ikki yuz ellik'
    >>> number_to_words(0)
    'nol'
    >>> number_to_words(-5)
    'minus besh'

    Oraliq: ``-10**12 <= n <= 10**12``. Manfiy sonlar ``minus`` bilan
    boshlanadi. ``yuz`` va ``ming`` oldidan ``bir`` doim yoziladi
    (``100`` -> ``bir yuz``).

    ``oʻ`` va ``gʻ`` dagi belgi :data:`uzkit.translit.OKINA` (U+02BB).

    ``int`` bo'lmagan (``bool`` ham) kiritish uchun ``TypeError``, oraliqdan
    tashqari son uchun ``ValueError`` ko'taradi.
    """
    _validate(n)
    if n == 0:
        return "nol"

    words: List[str] = ["minus"] if n < 0 else []
    remainder = abs(n)
    for value, name in _SCALES:
        count, remainder = divmod(remainder, value)
        if count:
            words += _below_thousand(count) + [name]
    words += _below_thousand(remainder)
    return " ".join(words)


def ordinal(n: int) -> str:
    """Tartib sonni yozadi: oxirgi so'zga ``-inchi`` yoki ``-nchi`` qo'shiladi.

    >>> ordinal(3)
    'uchinchi'
    >>> ordinal(2)
    'ikkinchi'
    >>> ordinal(1250)
    'bir ming ikki yuz ellikinchi'

    Oxirgi so'z unli bilan tugasa ``-nchi``, undosh bilan tugasa ``-inchi``
    qo'shiladi. Oraliq: ``0 <= n <= 10**12``.

    ``int`` bo'lmagan kiritish uchun ``TypeError``, manfiy yoki oraliqdan
    tashqari son uchun ``ValueError`` ko'taradi.
    """
    _validate(n)
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    words = number_to_words(n)
    suffix = "nchi" if words[-1] in _VOWELS else "inchi"
    return words + suffix
