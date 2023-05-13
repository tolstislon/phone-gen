# Phone Gen

[![PyPI](https://img.shields.io/pypi/v/phone-gen?color=%2301a001&label=pypi&logo=version)](https://pypi.org/project/phone-gen/)
[![Downloads](https://pepy.tech/badge/phone-gen)](https://pepy.tech/project/phone-gen)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/phone-gen.svg)](https://pypi.org/project/phone-gen/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/phone-gen)](https://github.com/tolstislon/phone-gen)  

[![Code style: black](https://github.com/tolstislon/phone-gen/workflows/tests/badge.svg)](https://github.com/tolstislon/phone-gen/actions/workflows/python-package.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

International phone number generation

**This module was created exclusively for generating test data**


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

Changelog
----

* [Releases](https://github.com/tolstislon/phone-gen/releases)

Contributing
----

#### Contributions are very welcome.

You might want to:

* Fix spelling errors
* Improve documentation
* Add tests for untested code
* Add new features
* Fix bugs

#### Getting started

* python 3.11
* pipenv 2022.12.19+

1. Clone the repository
    ```bash
    git clone https://github.com/tolstislon/phone-gen.git
    cd phone-gen
   ```
2. Install dev dependencies
    ```bash
    pipenv install --dev
    pipenv shell
   ```
3. Run the linters
    ```bash
    black phone_gen/ 
    flake8 phone_gen/
   ```
4. Run the tests
    ```bash
    pytest tests/
   ```
