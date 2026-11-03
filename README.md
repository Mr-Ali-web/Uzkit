[![tests](https://github.com/Mr-Ali-web/uzkit/actions/workflows/tests.yml/badge.svg)](https://github.com/Mr-Ali-web/uzkit/actions/workflows/tests.yml)

# uzkit

O'zbek tili va ma'lumotlari uchun yordamchi Python kutubxonasi.  
Small Python library for Uzbek language and data helpers.

## O'rnatish / Installation

```bash
pip install -e ".[dev]"
```

## Misollar / Examples

```python
from uzkit import to_cyrillic, to_latin, number_to_words, money_to_words, format_money, normalize_phone, is_valid_phone, is_valid_plate, ordinal

to_cyrillic("Salom, dunyo!")      # 'Салом, дунё!'
to_latin("Салом, дунё!")          # 'Salom, dunyo!'
number_to_words(1250)              # 'bir ming ikki yuz ellik'
money_to_words(1250)               # 'bir ming ikki yuz ellik soʻm'
format_money(1250000)              # '1 250 000 soʻm'
normalize_phone("+998 90 123 45 67")  # '+998901234567'
is_valid_phone("+998 90 123 45 67")   # True
is_valid_plate("01A123BC")         # True
ordinal(3)                         # 'uchinchi'
```

## Testlar / Tests

```bash
pytest
```

## Cheklovlar / Limitations

- Operator va viloyat kodlari rasmiy manbadan tekshirilmagan.
- Faqat mobil raqamlar qo'llab-quvvatlanadi.
- Viloyatlar ro'yxati Wikipedia/ISO 3166-2:UZ manbalariga asoslangan; rasmiy davlat manbasi bilan to'liq solishtirilmagan.

Operator and region codes are not verified against an official source. Only mobile phone numbers are supported.
Region list is based on Wikipedia/ISO 3166-2:UZ and has not been fully reconciled with official government sources.# Uzkit
