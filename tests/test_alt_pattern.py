import phonenumbers
import pytest

from phone_gen.alt_patterns import ALT_PATTERNS
from phone_gen import PhoneNumber


@pytest.mark.phonenumbers
@pytest.mark.parametrize('count', range(5))
@pytest.mark.parametrize('code, ref', [
    (key, value['ref']) for key, value in ALT_PATTERNS.items() if 'pattern' in value and 'ref' in value
])
def test_alt_pattern(code, ref, count):
    number = PhoneNumber(code).get_number()
    num_obj = phonenumbers.parse(number, code)
    assert phonenumbers.is_valid_number_for_region(num_obj, ref)


@pytest.mark.phonenumbers
@pytest.mark.parametrize('count', range(5))
@pytest.mark.parametrize('code, ref', [
    (key, value['ref']) for key, value in ALT_PATTERNS.items() if 'pattern' not in value and 'ref' in value
])
def test_ref(code, ref, count):
    number = PhoneNumber(code).get_number()
    num_obj = phonenumbers.parse(number, code)
    assert phonenumbers.is_valid_number_for_region(num_obj, ref)
