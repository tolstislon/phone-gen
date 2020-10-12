# Phone Gen

[![PyPI](https://img.shields.io/pypi/v/phone-gen?color=%2301a001&label=pypi&logo=version)](https://pypi.org/project/phone-gen/)
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

phone_number = PhoneNumber("GB") # ISO 3166-2
# or
phone_number = PhoneNumber("GBR") # ISO 3166-3
# or
phone_number = PhoneNumber("Great Britain") # Country name

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
usage: phone-gen [-h] [-v] [-n] country [country ...]

International phone number generation

positional arguments:
  country         Country code or country name. Example: "GB" or "Great Britain"

optional arguments:
  -h, --help      show this help message and exit
  -v, --version   show program's version number and exit
  -n, --not-full  Get a phone number without a country code
```

Example
```bash
# Get a phone number

$ phone-gen DE
+49791774007056

$ phone-gen DEU
+499968635

$ phone-gen Germany
+49960335800


# Get a phone number without a country code
$ phone-gen DE -n
66999511

$ phone-gen Germany -n
877595
```

Resources
----
* [Google's libphonenumber](https://github.com/google/libphonenumber)
* Modified [strgen](https://github.com/paul-wolf/strgen) library


Contributing
----
Contributions are very welcome.


##### How to build a version with libphonenumber below v8.12.3
Need Python 3.6 or more.
1. `git pull https://github.com/tolstislon/phone-gen.git`
2. `cd phone-gen`
3. `pip install requests`
4. `python dev_tools/patterns_generator.py -t {Desired Tag}`
5. `python setup.py install`


Changelog
----
* **1.3.8** Updating patterns to libphonenumber v8.12.11
* **1.3.7** Updating patterns to libphonenumber v8.12.10
* **1.3.6** Updating patterns to libphonenumber v8.12.9
* **1.3.5** Updating patterns to libphonenumber v8.12.8
* **1.3.4** Updating patterns to libphonenumber v8.12.7
* **1.3.3** Updating patterns to libphonenumber v8.12.6
* **1.3.2** Fix `MI` invalid pattern
* **1.3.1** Updating patterns to libphonenumber v8.12.5
* **1.3.0** Added the ability to build a module with old versions of libphonenumber
* **1.2.0** Added phone number generation by `country name` and `ISO 3166-3`
* **1.1.1** Updating patterns to libphonenumber v8.12.4
* **1.1.0** Added cli
* **1.0.0** The first stable release