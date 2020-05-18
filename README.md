# Phone Gen

[![Build Status](https://travis-ci.com/tolstislon/phone_gen.svg?branch=master)](https://travis-ci.com/tolstislon/phone_gen)
[![codecov](https://codecov.io/gh/tolstislon/phone-gen/branch/master/graph/badge.svg)](https://codecov.io/gh/tolstislon/phone-gen)


Phone number generator for [Google's libphonenumber library](https://github.com/google/libphonenumber)


Install
----

```bash
pip install phone-gen
```

Example
----
```python
from phone_gen import PhoneNumber

phone_number = PhoneNumber('GB')

# Get full phone number
number = phone_number.get_number()
print(number)  # +442908124840

# Get country code
country_code = phone_number.get_code()
print(country_code)  # 44

# Phone number without country code
number = phone_number.get_number(full=False)
print(number)  # 183782623
```


Contributing
----
Contributions are very welcome.