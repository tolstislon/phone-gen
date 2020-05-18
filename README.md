# Phone Gen

[![Build Status](https://travis-ci.com/tolstislon/phone_gen.svg?branch=master)](https://travis-ci.com/tolstislon/phone_gen)
[![codecov](https://codecov.io/gh/tolstislon/phone-gen/branch/master/graph/badge.svg)](https://codecov.io/gh/tolstislon/phone-gen)
[![PyPI](https://img.shields.io/pypi/v/phone-gen?color=%2301a001&label=version&logo=version)](https://pypi.org/project/phone-gen/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/phone-gen.svg)](https://pypi.org/project/phone-gen/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/phone-gen)](https://pypi.org/project/phone-gen/)

Phone number generator for [Google's libphonenumber library](https://github.com/google/libphonenumber)

This module was created exclusively for generating test data, when it is necessary to enter phone numbers in fields that are validated by the `libphonenumber` library or its ports.


Installation
----
Install using pip with
```bash
pip install phone-gen
```

Example
----
```python
from phone_gen import PhoneNumber

phone_number = PhoneNumber('GB')

# Get a phone number
number = phone_number.get_number()
print(number)  # +442908124840

# Get a country code
country_code = phone_number.get_code()
print(country_code)  # 44

# Get a phone number without a country code
number = phone_number.get_number(full=False)
print(number)  # 183782623
```

##### pytest fixture
```python
import pytest
from phone_gen import PhoneNumber


@pytest.fixture
def phone_number():
    def wrap(code):
        return PhoneNumber(code).get_number()

    yield wrap


def test_one(phone_number):
    number = phone_number('DE')
    ...
```

Resources
----
* [libphonenumber](https://github.com/google/libphonenumber)
* Modified [strgen](https://github.com/paul-wolf/strgen) library


Contributing
----
Contributions are very welcome.