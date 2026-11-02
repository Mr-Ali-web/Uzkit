import pytest

from uzkit.translit import OKINA, TUTUQ, to_cyrillic, to_latin

PAIRS = [
    ("Toshkent", "Тошкент"),
    (f"O{OKINA}zbekiston", "Ўзбекистон"),
    (f"G{OKINA}ijduvon", "Ғиждувон"),
    (f"Qo{OKINA}qon", "Қўқон"),
    ("yaxshi", "яхши"),
    ("shahar", "шаҳар"),
    ("chiroyli", "чиройли"),
    ("yoz", "ёз"),
    ("Yevropa", "Европа"),
    ("Elektr", "Электр"),
    ("aeroport", "аэропорт"),
    ("SHAHAR", "ШАҲАР"),
    ("YOSH", "ЁШ"),
    ("Shahar", "Шаҳар"),
    (f"ma{TUTUQ}no", "маъно"),
    ("", ""),
    ("123, 45!", "123, 45!"),
]


@pytest.mark.parametrize("latin,cyrillic", PAIRS)
def test_to_cyrillic(latin, cyrillic):
    assert to_cyrillic(latin) == cyrillic


@pytest.mark.parametrize("latin,cyrillic", PAIRS)
def test_to_latin(latin, cyrillic):
    assert to_latin(cyrillic) == latin


@pytest.mark.parametrize("apos", ["'", "’", "ʻ", "‘", "`"])
def test_apostrophe_variants(apos):
    assert to_cyrillic(f"o{apos}zbek") == "ўзбек"
    assert to_cyrillic(f"ma{apos}no") == "маъно"


def test_quotes_at_word_edges_untouched():
    assert to_cyrillic("'salom'") == "'салом'"