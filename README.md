# Phone Gen

[![PyPI](https://img.shields.io/pypi/v/phone-gen?color=%2301a001&label=version&logo=version)](https://pypi.org/project/phone-gen/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/phone-gen.svg)](https://pypi.org/project/phone-gen/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/phone-gen)](https://pypi.org/project/phone-gen/)
[![Downloads](https://pepy.tech/badge/phone-gen)](https://pepy.tech/project/phone-gen)
[![Build Status](https://travis-ci.com/tolstislon/phone-gen.svg?branch=master)](https://travis-ci.com/tolstislon/phone-gen)
[![codecov](https://codecov.io/gh/tolstislon/phone-gen/branch/master/graph/badge.svg)](https://codecov.io/gh/tolstislon/phone-gen)

International phone number generation

This module was created exclusively for generating test data


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

phone_number = PhoneNumber("GB")

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
    number = phone_number("DE")
    ...
```

Using the CLI
----
```bash
usage: phone-gen [-h] [-v] [-n] country

International phone number generation

positional arguments:
  country        Country code example: GB

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
  -n, --not-full  Get a phone number without a country code

```

Example
```bash
# Get a phone number
$ phone-gen GB
+44199561679

# Get a phone number without a country code
$ phone-gen GB -n
199561343
```

Resources
----
* [Google's libphonenumber](https://github.com/google/libphonenumber)
* Modified [strgen](https://github.com/paul-wolf/strgen) library


Contributing
----
Contributions are very welcome.


Changelog
----
* **1.1.1** Updating patterns to libphonenumber v8.12.4
* **1.1.0** Added cli
* **1.0.0** The first stable release