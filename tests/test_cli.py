import os
import random

import phonenumbers
import pytest

from phone_gen.patterns import PATTERNS


@pytest.mark.phonenumbers
@pytest.mark.parametrize("country", random.sample(tuple(PATTERNS["data"].keys()), 20))
@pytest.mark.parametrize("arg", ("", "-n ", "-m "))
def test_get_country(capfd: pytest.CaptureFixture, country: str, arg: str):
    os.system(f"phone-gen {arg}{country}")
    captured = capfd.readouterr()
    num_obg = phonenumbers.parse(captured.out, country)
    assert phonenumbers.is_valid_number_for_region(num_obg, country)


@pytest.mark.phonenumbers
@pytest.mark.parametrize("country", random.sample(tuple(PATTERNS["data"].keys()), 20))
@pytest.mark.parametrize("arg", ("", "n", "m"))
def test_get_without_country_code(capfd: pytest.CaptureFixture, country: str, arg: str):
    os.system(f"phone-gen -f{arg} {country}")
    captured = capfd.readouterr()
    code = PATTERNS["data"][country]["code"]
    num_obg = phonenumbers.parse(f"{code}{captured.out}", country)
    assert phonenumbers.is_valid_number_for_region(num_obg, country)


def test_invalid_country(capfd: pytest.CaptureFixture):
    os.system("phone-gen qwe")
    captured = capfd.readouterr()
    assert captured.out.strip() == 'Error: Not found country "QWE"'


@pytest.mark.phonenumbers
@pytest.mark.parametrize(
    "country_name, code", (("Germany", "DE"), ("Panama", "PA"), ("Turkey", "TR"), ("France", "FR"))
)
@pytest.mark.parametrize("arg", ("", "-n ", "-m "))
def test_find_country_name(capfd: pytest.CaptureFixture, country_name: str, code: str, arg: str):
    os.system(f"phone-gen {arg}{country_name}")
    captured = capfd.readouterr()
    num_obg = phonenumbers.parse(captured.out, code)
    assert phonenumbers.is_valid_number_for_region(num_obg, code)


@pytest.mark.phonenumbers
@pytest.mark.parametrize("iso, code", (("VNM", "VN"), ("SLE", "SL"), ("MCO", "MC")))
@pytest.mark.parametrize("arg", ("", "-n ", "-m "))
def test_find_iso3(capfd: pytest.CaptureFixture, iso: str, code: str, arg: str):
    os.system(f"phone-gen {arg}{iso}")
    captured = capfd.readouterr()
    num_obg = phonenumbers.parse(captured.out, code)
    assert phonenumbers.is_valid_number_for_region(num_obg, code)
