"""uzkit - O'zbekiston uchun kichik yordamchi vositalar to'plami."""

from uzkit.validators import is_valid_phone, is_valid_plate, normalize_phone

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "is_valid_phone",
    "is_valid_plate",
    "normalize_phone",
]
