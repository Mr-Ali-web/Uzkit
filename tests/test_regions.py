import pytest

from uzkit.regions import Region, get_region, list_regions


def test_list_regions_count():
    assert len(list_regions()) == 14


def test_list_regions_returns_region_objects():
    assert all(isinstance(region, Region) for region in list_regions())


def test_get_region_by_latin_name():
    region = get_region("Toshkent viloyati")
    assert region is not None
    assert region.capital == "Nurafshon"


def test_get_region_by_cyrillic_name():
    region = get_region("Тошкент вилояти")
    assert region is not None
    assert region.name == "Toshkent viloyati"


def test_get_region_case_insensitive():
    assert get_region("toshkent viloyati") == get_region("TOSHKENT VILOYATI")


def test_get_region_unknown_returns_none():
    assert get_region("Mars") is None


def test_get_region_empty_returns_none():
    assert get_region("") is None
    assert get_region("   ") is None


def test_get_region_non_string_returns_none():
    assert get_region(None) is None
    assert get_region(123) is None


def test_all_capitals_present():
    for region in list_regions():
        assert region.capital
        assert region.capital_cyrillic


def test_plate_codes_match_validator_ranges():
    codes = {region.plate_code for region in list_regions()}
    assert codes == {"01", "10", "20", "25", "30", "40", "50", "60", "70", "75", "80", "85", "90", "95"}


def test_unique_region_names():
    names = [region.name for region in list_regions()]
    assert len(names) == len(set(names))


def test_unique_cyrillic_names():
    names = [region.name_cyrillic for region in list_regions()]
    assert len(names) == len(set(names))


def test_qoraqalpogiston():
    region = get_region("Qoraqalpog'iston Respublikasi")
    assert region is not None
    assert region.capital == "Nukus"


def test_toshkent_shahri():
    region = get_region("Toshkent shahri")
    assert region is not None
    assert region.plate_code == "01"


def test_get_region_by_capital_not_required():
    assert get_region("Nukus") is None


def test_immutable_region():
    region = get_region("Xorazm viloyati")
    with pytest.raises(Exception):
        region.name = "changed"


def test_region_code_mapping():
    assert get_region("Qashqadaryo viloyati").plate_code == "70"
    assert get_region("Surxondaryo viloyati").plate_code == "75"
    assert get_region("Buxoro viloyati").plate_code == "80"
    assert get_region("Navoiy viloyati").plate_code == "85"
