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
import random

class PhoneNumber:
    def _init_(self, country):
        self.country = country
        self.country_code = self.get_country_code(country)
        self.number_length = self.get_number_length(country)

    def get_country_code(self, country):
        # A dictionary mapping country names/ISO codes to their respective country codes
        country_codes = {
            "US": "1",
            "USA": "!",
            "UNiTED STATE": "1",
            # Add more countries as needed
        }
        return country_codes.get(country, None)

    def get_number_length(self, country):
        # A dictionary mapping country names/ISO codes to their respective phone number lengths
        number_lengths = {
            "US": 10,
            "USA": 10,
            "united state": 10,
            # Add more countries as needed
        }
        return number_lengths.get(country, None)

    def get_number(self, full=True):
        if full:
            return f"+{self.country_code}{self.generate_random_number()}"
        return self.generate_random_number()

    def get_mobile(self):
        return f"+{self.country_code}{self.generate_random_mobile_number()}"

    def get_national(self):
        return f"+{self.country_code}{self.generate_random_number()}"

    def generate_random_number(self):
        return ''.join(random.choices('0123456789', k=self.number_length))

    def generate_random_mobile_number(self):
        # Assuming mobile numbers start with '7' in the US
        return '7' + ''.join(random.choices('0123456789', k=self.number_length - 1))

# Example usage
if _name_ == "_main_":
    phone_number = PhoneNumber("US")
    print(phone_number.get_number())  # e.g., +14234945549
    print(phone_number.get_code())     # 1
    print(phone_number.get_number(full=False))  # e.g., 183782623
    print(phone_number.get_mobile())   # e.g., +15597046914

##### pytest fixture

```python
import pytest
from phone_gen import PhoneNumber

@pytest.fixture
def phone_number():
    """Fixture to generate phone numbers based on country code."""
    return lambda code: PhoneNumber(code).get_number()

def test_one(phone_number):
    number = phone_number("DE")
    # Add assertions or further testing logic here
    ...
```

import argparse

def main():
    parser = argparse.ArgumentParser(
        description="International phone number generation"
    )

    # Positional argument for country
    parser.add_argument(
        'country',
        nargs='+',  # Allows multiple country codes/names
        help='Country code or country name (e.g., "US", "USA", "United state")'
    )

    # Optional arguments
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.0',  # Replace with actual version
        help="Show program's version number and exit"
    )
    parser.add_argument(
        '-f', '--not-full',
        action='store_true',
        help='Get a phone number without a country code'
    )
    parser.add_argument(
        '-m', '--mobile',
        action='store_true',
        help='Get mobile phone number'
    )
    parser.add_argument(
        '-n', '--national',
        action='store_true',
        help='Get national phone number'
    )

    # Parse the arguments
    args = parser.parse_args()

    # Here you would implement the logic to generate the phone numbers
    # based on the parsed arguments.
    # For example:
    print(f"Generating phone numbers for: {args.country}")
    if args.not_full:
        print("Generating phone numbers without country code.")
    if args.mobile:
        print("Generating mobile phone numbers.")
    if args.national:
        print("Generating national phone numbers.")

if _name_ == "_main_":
    main()
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

* python 3.12
* pipenv 2023.11.15+

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
3. Run black
    ```bash
    pipenv run black
   ```
4. Run flake8
    ```bash
    pipenv run flake
   ```
5. Run the tests
    ```bash
    pipenv run tests
   ```
