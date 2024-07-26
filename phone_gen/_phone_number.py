import random
from dataclasses import dataclass, field
from re import sub
from typing import Dict, Optional

from string_gen import StringGen

from .alt_patterns import ALT_PATTERNS
from .country_name import COUNTRY_NAME
from .iso3 import ISO3
from .patterns import PATTERNS

ALTERNATIVE_FILE: dict = {}


def clean_alt_patters() -> None:
    ALTERNATIVE_FILE.clear()


def load_alt_patters(patters: dict) -> None:
    clean_alt_patters()
    ALTERNATIVE_FILE.update(patters)


class PhoneNumberNotFound(Exception):
    """Not found country"""


@dataclass
class PhoneNumber:
    code: str
    _country: Optional[Dict[str, str]] = field(default=None, init=False, repr=False)

    def __str__(self):
        return f"<{type(self).__name__}({self.info()})>"

    def __post_init__(self):
        self.code = sub(r"\W", "", self.code).upper()
        if (country := self._find(self.code)) is None:
            raise PhoneNumberNotFound(f'Not found country "{self.code}"')
        self._country = country

    def _find(self, value: str) -> Optional[Dict[str, str]]:
        if country := ALTERNATIVE_FILE.get(value) or PATTERNS["data"].get(value):
            return country
        if alt_country := ALT_PATTERNS.get(value):
            return alt_country if "pattern" in alt_country else self._find(alt_country["ref"])
        if country_name := COUNTRY_NAME.get(value):
            return self._find(country_name["code"])
        if ico3 := ISO3.get(value):
            return self._find(ico3["code"])
        return None

    @staticmethod
    def info() -> str:
        return PATTERNS["info"]

    def get_code(self) -> str:
        return self._country["code"]

    def get_number(self, full: bool = True) -> str:
        return self.get_national(full) if random.randint(0, 1) else self.get_mobile(full)

    def get_mobile(self, full: bool = True) -> str:
        number = StringGen(self._country.get("mobile", self._country["pattern"])).render()
        return f"+{self._country['code']}{number}" if full else number

    def get_national(self, full: bool = True) -> str:
        number = StringGen(self._country["pattern"]).render()
        # Could not find problem
        if number.startswith("49") and self._country["code"] == "49":  # pragma: no cover
            return self.get_national(full)
        return f"+{self._country['code']}{number}" if full else number
