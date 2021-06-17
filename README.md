# Phone Gen

[![PyPI](https://img.shields.io/pypi/v/phone-gen?color=%2301a001&label=pypi&logo=version)](https://pypi.org/project/phone-gen/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/phone-gen.svg)](https://pypi.org/project/phone-gen/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/phone-gen)](https://pypi.org/project/phone-gen/)
[![Downloads](https://pepy.tech/badge/phone-gen)](https://pepy.tech/project/phone-gen)

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

phone_number = PhoneNumber("GB")  # ISO 3166-2
# or
phone_number = PhoneNumber("GBR")  # ISO 3166-3
# or
phone_number = PhoneNumber("Great Britain")  # Country name

# Get a phone number
number = phone_number.get_number()
print(number)  # +442908124840

# Get a country code
country_code = phone_number.get_code()
print(country_code)  # 44

# Get a phone number without a country code
number = phone_number.get_number(full=False)
print(number)  # 183782623

# Get a mobile phone number
number = phone_number.get_mobile()
print(number)  # +447911899521

# Get a national phone number
number = phone_number.get_national()
print(number)  # +442408055065
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
  country         Country code or country name. Example: "GB" or "GBR" or "Great Britain"

optional arguments:
  -h, --help      show this help message and exit
  -v, --version   show program's version number and exit
  -f, --not-full  Get a phone number without a country code
  -m, --mobile    Get mobile phone number
  -n, --national  Get national phone number
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
$ phone-gen -f DE
66999511

$ phone-gen -f Germany
877595

# Get mobile phone number
$ phone-gen -m DE
+491601376066

# Get national phone number
$ phone-gen -n DE
+4940381
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


