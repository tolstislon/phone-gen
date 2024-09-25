import pytest

from phone_gen.country_name import COUNTRY_NAME
from phone_gen.iso3 import ISO3
from phone_gen.patterns import PATTERNS


@pytest.mark.parametrize("country", PATTERNS["data"].keys())
def test_ico3(country: str):
    assert [i for i in ISO3.values() if i["code"] == country]


@pytest.mark.parametrize("country", PATTERNS["data"].keys())
def test_country_name(country: str):
    assert [i for i in COUNTRY_NAME.values() if i["code"] == country]
