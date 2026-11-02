"""O'zbek tili uchun Lotin <-> Kirill transliteratsiyasi."""

from __future__ import annotations

OKINA = "\u02bb"  # ʻ  o‘ va g‘ dagi belgi
TUTUQ = "\u02bc"  # ʼ  tutuq belgisi (ma’no)

_APOSTROPHES = frozenset("'\u2019\u02bb\u2018`\u00b4\u02bc")
_LAT_VOWELS = frozenset("aeiou")
_CYR_VOWELS = frozenset("аеёиоуўэюяы")

_LAT2CYR = {
    "a": "а", "b": "б", "d": "д", "f": "ф", "g": "г", "h": "ҳ",
    "i": "и", "j": "ж", "k": "к", "l": "л", "m": "м", "n": "н",
    "o": "о", "p": "п", "q": "қ", "r": "р", "s": "с", "t": "т",
    "u": "у", "v": "в", "x": "х", "y": "й", "z": "з",
}
_Y_COMBOS = {"o": "ё", "u": "ю", "a": "я", "e": "е"}

_CYR2LAT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "ё": "yo",
    "ж": "j", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l",
    "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s",
    "т": "t", "у": "u", "ф": "f", "х": "x", "ц": "ts", "ч": "ch",
    "ш": "sh", "щ": "shch", "ъ": TUTUQ, "ы": "i", "ь": "", "э": "e",
    "ю": "yu", "я": "ya", "ў": "o" + OKINA, "қ": "q",
    "ғ": "g" + OKINA, "ҳ": "h",
}


def to_cyrillic(text: str) -> str:
    """Lotin yozuvidagi matnni Kirillga o'giradi.

    >>> to_cyrillic("O'zbekiston")
    'Ўзбекистон'
    """
    out: list[str] = []
    n = len(text)
    i = 0
    while i < n:
        ch = text[i]
        low = ch.lower()
        nxt = text[i + 1] if i + 1 < n else ""
        nlow = nxt.lower()
        prev = text[i - 1] if i > 0 else ""
        step = 1

        if low in ("o", "g") and nxt in _APOSTROPHES:
            res = "ў" if low == "o" else "ғ"
            step = 2
        elif low in ("s", "c") and nlow == "h":
            res = "ш" if low == "s" else "ч"
            step = 2
        elif low == "y" and nlow in _Y_COMBOS:
            res = _Y_COMBOS[nlow]
            step = 2
        elif low == "e":
            at_start = not prev.isalpha() or prev.lower() in _LAT_VOWELS
            res = "э" if at_start else "е"
        elif ch in _APOSTROPHES and prev.isalpha() and nxt.isalpha():
            res = "ъ"
        elif low in _LAT2CYR:
            res = _LAT2CYR[low]
        else:
            out.append(ch)
            i += 1
            continue

        out.append(res.upper() if ch.isupper() else res)
        i += step
    return "".join(out)


def _has_upper_neighbor(text: str, i: int) -> bool:
    before = i > 0 and text[i - 1].isupper()
    after = i + 1 < len(text) and text[i + 1].isupper()
    return before or after


def to_latin(text: str) -> str:
    """Kirill yozuvidagi matnni Lotinga o'giradi (2023 alifbosi).

    >>> to_latin("Ўзбекистон")
    'Oʻzbekiston'
    """
    out: list[str] = []
    for i, ch in enumerate(text):
        low = ch.lower()
        if low == "е":
            prev = text[i - 1].lower() if i > 0 else ""
            ye = not prev.isalpha() or prev in _CYR_VOWELS or prev in "ъь"
            res = "ye" if ye else "e"
        elif low in _CYR2LAT:
            res = _CYR2LAT[low]
        else:
            out.append(ch)
            continue

        if ch.isupper() and res:
            if len(res) > 1 and not _has_upper_neighbor(text, i):
                res = res.capitalize()
            else:
                res = res.upper()
        out.append(res)
    return "".join(out)