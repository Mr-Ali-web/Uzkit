# uzkit

O'zbekiston uchun kichik yordamchi vositalar to'plami. Hozircha:

- telefon raqamini tekshirish va normallashtirish (`+998` format);
- avtomobil davlat raqamini tekshirish.

Tashqi kutubxonalarga bog'liq emas.

## O'rnatish

```bash
pip install -e ".[dev]"
```

## Foydalanish

```python
from uzkit import is_valid_phone, normalize_phone, is_valid_plate

is_valid_phone("+998 90 123 45 67")      # True
is_valid_phone("+998 10 123 45 67")      # False (noma'lum operator kodi)
normalize_phone("(90) 123-45-67")        # "+998901234567"
normalize_phone("salom")                 # None

is_valid_plate("01 A 123 AA")            # True
is_valid_plate("01 123 AAA")             # True
is_valid_plate("99 A 123 AA")            # False (noma'lum viloyat kodi)
```

### Telefon

Qabul qilinadigan ko'rinishlar: `+998901234567`, `998901234567`, `901234567`
(bo'shliq, tire, nuqta va qavslar e'tiborga olinmaydi). Faqat mobil operator
kodlari qabul qilinadi: `20, 33, 50, 55, 77, 88, 90, 91, 93, 94, 95, 97, 98, 99`.
Ro'yxat `uzkit.validators.MOBILE_OPERATOR_CODES` ichida.

### Davlat raqami

| Format        | Misol         |
|---------------|---------------|
| `01 A 123 AA` | `01 A 123 AA` |
| `01 123 AAA`  | `01 123 AAA`  |

Bo'shliqlar ixtiyoriy (`01A123AA`), harflar katta-kichikligi farqlanmaydi,
faqat lotin harflari. Viloyat kodlari: `01, 10, 20, 25, 30, 40, 50, 60, 70, 75,
80, 85, 90, 95`.

## Testlar

```bash
pytest
```

## Litsenziya

[MIT](LICENSE)
