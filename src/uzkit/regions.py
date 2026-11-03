"""O'zbekiston viloyatlari va tarkibiy birliklari."""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional

__all__ = ["Region", "get_region", "list_regions"]


@dataclass(frozen=True)
class Region:
    name: str
    name_cyrillic: str
    capital: str
    capital_cyrillic: str
    plate_code: str


@lru_cache(maxsize=1)
def _regions() -> tuple[Region, ...]:
    path = Path(__file__).resolve().parent / "data" / "regions.json"
    with path.open(encoding="utf-8") as file:
        raw = json.load(file)
    return tuple(Region(**item) for item in raw)


def list_regions() -> list[Region]:
    return list(_regions())


def get_region(name: str) -> Optional[Region]:
    if not isinstance(name, str) or not name.strip():
        return None
    needle = name.casefold()
    for region in _regions():
        if region.name.casefold() == needle or region.name_cyrillic.casefold() == needle:
            return region
    return None
