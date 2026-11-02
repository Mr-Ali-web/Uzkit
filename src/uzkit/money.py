"""So'm summalarini so'zga aylantirish va formatlash."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import Union

from uzkit.numbers import number_to_words
from uzkit.translit import OKINA

SOM = f"so{OKINA}m"
TIYIN = "tiyin"

Amount = Union[int, float, Decimal, str]


def _to_decimal(amount: Amount) -> Decimal:
    if isinstance(amount, bool) or not isinstance(amount, (int, float, Decimal, str)):
        raise TypeError(f"Unsupported amount type: {type(amount).__name__}")
    return Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def money_to_words(amount: Amount, *, with_tiyin: bool = True) -> str:
    """Summani so'm va tiyinda so'z bilan yozadi.

    >>> money_to_words(1250)
    'bir ming ikki yuz ellik soʻm'
    >>> money_to_words("1250.50")
    'bir ming ikki yuz ellik soʻm ellik tiyin'
    """
    value = _to_decimal(amount)
    sign = "minus " if value < 0 else ""
    value = abs(value)
    som = int(value)
    tiyin = int((value - som) * 100)
    parts = [number_to_words(som), SOM]
    if with_tiyin and tiyin:
        parts += [number_to_words(tiyin), TIYIN]
    return sign + " ".join(parts)


def format_money(amount: Amount) -> str:
    """Summani o'qishga qulay ko'rinishda yozadi.

    >>> format_money(1250000)
    '1 250 000 soʻm'
    """
    value = _to_decimal(amount)
    sign = "-" if value < 0 else ""
    value = abs(value)
    som = int(value)
    tiyin = int((value - som) * 100)
    text = f"{som:,}".replace(",", " ")
    if tiyin:
        text += f",{tiyin:02d}"
    return f"{sign}{text} {SOM}"