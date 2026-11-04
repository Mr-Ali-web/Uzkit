[![tests](https://github.com/Mr-Ali-web/uzkit/actions/workflows/tests.yml/badge.svg)](https://github.com/Mr-Ali-web/uzkit/actions/workflows/tests.yml)

# uzkit

[![PyPI](https://img.shields.io/pypi/v/uzkit)](https://pypi.org/project/uzkit/)

O'zbek tili va ma'lumotlari uchun yordamchi Python kutubxonasi.  
Small Python library for Uzbek language and data helpers.

## O'rnatish / Installation

```bash
pip install uzkit
```

## Rivojlantirish / Development

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
card_type("8600 0000 0000 0007")      # 'Uzcard'
is_valid_card("8600 0000 0000 0007")  # True
format_card("9860 0901 0131 2172")    # '9860 0901 0131 2172'
mask_card("9860 0901 0131 2172")      # '9860 **** **** 2172'
```

## Testlar / Tests

```bash
pytest
```

## Cheklovlar / Limitations

- Telefon kodlari Wikipedia va operator sahifalariga asoslangan, regulyatorning rasmiy hujjati bilan tekshirilmagan.
- Faqat mobil raqamlar qo'llab-quvvatlanadi.
- Viloyatlar ro'yxati Wikipedia/ISO 3166-2:UZ manbalariga asoslangan; rasmiy davlat manbasi bilan to'liq solishtirilmagan.

Operator and region codes are not verified against an official source. Only mobile phone numbers are supported.
Region list is based on Wikipedia/ISO 3166-2:UZ and has not been fully reconciled with official government sources.# Uzkit

- Kartalar BIN prefiksi bo'yicha aniqlanadi (Uzcard 8600 va 5614, Humo 9860, shuningdek Visa, Mastercard, UnionPay).
- `is_valid_card` faqat format va Luhn yig'indisini tekshiradi, karta mavjudligini yoki faolligini emas.
- Humo uchun Luhn qoidasi rasmiy manbada tasdiqlanmagan, faqat ommaviy test kartasi bilan sinalgan.
- Kutubxona hech qanday karta raqamini saqlamaydi yoki yubormaydi.
