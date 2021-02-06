import random

import phonenumbers
import pytest

from phone_gen import PhoneNumber, PhoneNumberNotFound
from phone_gen.patterns import PATTERNS


@pytest.mark.phonenumbers
@pytest.mark.parametrize('count', range(15))
@pytest.mark.parametrize('country', PATTERNS['data'].keys())
def test_patterns(country, count):
    phone_number = PhoneNumber(country)
    number = phone_number.get_number()
    num_obj = phonenumbers.parse(number, country)
    assert phonenumbers.is_valid_number_for_region(num_obj, country)


@pytest.mark.phonenumbers
@pytest.mark.parametrize('count', range(15))
@pytest.mark.parametrize('country', PATTERNS['data'].keys())
def test_national(country, count):
    phone_number = PhoneNumber(country)
    number = phone_number.get_national()
    num_obj = phonenumbers.parse(number, country)
    assert phonenumbers.is_valid_number_for_region(num_obj, country)


@pytest.mark.phonenumbers
@pytest.mark.parametrize('count', range(15))
@pytest.mark.parametrize('country', PATTERNS['data'].keys())
def test_mobile(country, count):
    phone_number = PhoneNumber(country)
    number = phone_number.get_mobile()
    num_obj = phonenumbers.parse(number, country)
    assert phonenumbers.is_valid_number_for_region(num_obj, country)


def test_info():
    phone_number = PhoneNumber('gb')
    assert phone_number.info().startswith('libphonenumber')


def test_get_code():
    country = random.choice(tuple(PATTERNS['data'].keys()))
    phone_number = PhoneNumber(country)
    assert phone_number.get_code() == PATTERNS['data'][country]['code']


def test_invalid_country():
    with pytest.raises(PhoneNumberNotFound):
        PhoneNumber('qwe')


def test_str_method():
    phone_number = PhoneNumber('GB')
    assert str(phone_number).startswith('<PhoneNumber(libphonenumber')
