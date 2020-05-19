import os
import random

import phonenumbers
import pytest

from phone_gen.patterns import PATTERNS


@pytest.mark.parametrize('country', random.sample(tuple(PATTERNS['data'].keys()), 20))
def test_get_country(capfd, country):
    os.system('phone-gen {}'.format(country))
    captured = capfd.readouterr()
    num_obg = phonenumbers.parse(captured.out, country)
    assert phonenumbers.is_valid_number_for_region(num_obg, country)


@pytest.mark.parametrize('country', random.sample(tuple(PATTERNS['data'].keys()), 20))
def test_get_without_country_code(capfd, country):
    os.system('phone-gen {} -n'.format(country))
    captured = capfd.readouterr()
    code = PATTERNS['data'][country]['code']
    num_obg = phonenumbers.parse('{}{}'.format(code, captured.out), country)
    assert phonenumbers.is_valid_number_for_region(num_obg, country)


def test_invalid_country(capfd):
    os.system('phone-gen qwe')
    captured = capfd.readouterr()
    assert captured.out.strip() == 'Error: Not found country qwe'
