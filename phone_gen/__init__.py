"""
International phone number generation

This module was created exclusively for generating test data

Support ISO 3166-2, ISO 3166-3 and Country Name
----
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
----

Resources:
    * libphonenumber https://github.com/google/libphonenumber
    * Modified strgen https://github.com/paul-wolf/strgen
"""

from ._generator import PhoneNumber, PhoneNumberNotFound, load_alt_patters

try:
    from .__version__ import version as __version__
except ImportError:  # pragma: no cover
    __version__ = "unknown"

__all__ = ["PhoneNumber", "__version__", "PhoneNumberNotFound", "load_alt_patters"]
