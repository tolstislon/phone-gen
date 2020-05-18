import phonenumbers
import pytest
import random
from phone_gen import PhoneNumber
from phone_gen.patterns import PATTERNS
from phone_gen.generator import NumberGeneratorException


@pytest.mark.parametrize('count', range(15))
@pytest.mark.parametrize('country', PATTERNS['data'].keys())
def test_patterns(country, count):
    number = PhoneNumber(country).get_number()
    num_obj = phonenumbers.parse(number, country)
    assert phonenumbers.is_valid_number_for_region(num_obj, country)


def test_info():
    phone_number = PhoneNumber('gb')
    assert phone_number.info.startswith('libphonenumber')


def test_get_code():
    country = random.choice(tuple(PATTERNS['data'].keys()))
    phone_number = PhoneNumber(country)
    assert phone_number.get_code() == PATTERNS['data'][country]['code']


def test_invalid_country():
    with pytest.raises(NumberGeneratorException):
        PhoneNumber('qwe')
