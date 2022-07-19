import random

import phonenumbers
import pytest

from phone_gen import load_alt_patters, clean_alt_patters, PhoneNumber
from phone_gen.patterns import PATTERNS


@pytest.fixture(params=random.sample(tuple(PATTERNS['data'].keys()), 20))
def load_fixture(request):
    load_alt_patters({
        request.param: {
            "code": "0",
            "pattern": "([2]{7})",
            "mobile": "([1]{9})"
        }
    })
    yield request.param
    clean_alt_patters()


@pytest.mark.phonenumbers
def test_load_alt_patterns(load_fixture):
    phone_number = PhoneNumber(load_fixture)
    assert phone_number.get_national() == '+0{}'.format('2' * 7)
    assert phone_number.get_mobile() == '+0{}'.format('1' * 9)
    clean_alt_patters()
    phone_number = PhoneNumber(load_fixture)
    num_obj = phonenumbers.parse(phone_number.get_national(), load_fixture)
    assert phonenumbers.is_valid_number_for_region(num_obj, load_fixture)
    num_obj = phonenumbers.parse(phone_number.get_mobile(), load_fixture)
    assert phonenumbers.is_valid_number_for_region(num_obj, load_fixture)
