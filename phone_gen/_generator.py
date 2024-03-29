import random
import re
import string
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict, Final

from .alt_patterns import ALT_PATTERNS
from .country_name import COUNTRY_NAME
from .iso3 import ISO3
from .patterns import PATTERNS

SYSTEM_RANDOM = random.SystemRandom()
RANDINT = SYSTEM_RANDOM.randint
CHOICE = SYSTEM_RANDOM.choice
SAMPLE = SYSTEM_RANDOM.sample
SHUFFLE = SYSTEM_RANDOM.shuffle

BSLASH: Final[str] = "\\"
LBRACE: Final[str] = "{"
RBRACE: Final[str] = "}"
LSQB: Final[str] = "["
RSQB: Final[str] = "]"
LPAR: Final[str] = "("
RPAR: Final[str] = ")"
COLON: Final[str] = ":"
MINUS: Final[str] = "-"
VBAR: Final[str] = "|"

META_TOKENS: Tuple[str, ...] = (
    LSQB,
    RSQB,
    LBRACE,
    RBRACE,
    LPAR,
    RPAR,
    VBAR,
)

ALTERNATIVE_FILE: dict = {}


def clean_alt_patters() -> None:
    ALTERNATIVE_FILE.clear()


def load_alt_patters(patters: dict) -> None:
    clean_alt_patters()
    ALTERNATIVE_FILE.update(patters)


class NumberGeneratorException(Exception):
    """Base Exception"""


class NumberGeneratorSyntaxException(NumberGeneratorException):
    """Syntax Exception"""


class PhoneNumberNotFound(Exception):
    """Not found country"""


class StringNode(metaclass=ABCMeta):
    """The abstract class for all nodes"""

    @abstractmethod
    def render(self): ...  # pragma: no cover


@dataclass(frozen=True)
class Sequence:
    """Render a sequence of nodes from the template."""

    seq: List[StringNode]

    def render(self) -> str:
        return "".join(i.render() for i in self.seq)


@dataclass(frozen=True)
class SequenceOR(Sequence):
    def render(self):
        return self.seq[RANDINT(0, len(self.seq) - 1)].render()


@dataclass(repr=True)
class Literal(StringNode):
    chars: str

    def render(self) -> str:
        return self.chars


@dataclass(repr=True)
class CharacterSet(StringNode):
    chars: str
    start: int
    cnt: int

    def render(self) -> str:
        cnt = RANDINT(self.start, self.cnt) if self.start > -1 else self.cnt
        return "".join(self.chars[RANDINT(0, len(self.chars) - 1)] for _ in range(cnt))


class NumberGenerator:
    """
    Modified StringGenerator https://github.com/paul-wolf/strgen
    """

    _code = {"d": string.digits}

    def __init__(self, pattern: str):
        self._pattern = pattern
        self._index = -1
        self._seq = self._get_sequence()

    def _current(self) -> Optional[str]:
        return self._pattern[self._index] if self._index < len(self._pattern) else None

    def _next(self) -> Optional[str]:
        self._index += 1
        return self._current()

    def _lookahead(self) -> Optional[str]:
        return (
            self._pattern[self._index + 1]
            if self._index + 1 < len(self._pattern)
            else None
        )

    def _last(self) -> Optional[str]:
        return None if self._index == 0 else self._pattern[self._index - 1]

    def _get_quantifier(self) -> Tuple[int, int]:
        start = -1
        self._next()
        digits = "0"
        while True:
            d = self._next()
            if not d:
                raise NumberGeneratorException(
                    "Unexpected end of input getting quantifier"
                )
            if d in (COLON, MINUS):
                start = int(digits)
                digits = "0"
                continue
            if d == RBRACE:
                if self._last() in (COLON, MINUS):
                    raise NumberGeneratorSyntaxException(
                        "Quantifier range must be closed"
                    )
                break  # pragma: no cover
            if d.isnumeric():
                digits += d
            else:
                raise NumberGeneratorSyntaxException("Non-digit in count")
        return start, int(digits)

    @staticmethod
    def _get_character_range(first: str, last: str) -> str:
        chars = ""
        # support z-a as a range
        if not ord(first) < ord(last):
            first, last = last, first
        for c in range(ord(first), ord(last) + 1):
            chars += chr(c)
        return chars

    def _get_character_set(self) -> CharacterSet:
        chars = ""
        cnt = 1
        start = 0

        while True:
            char = self._next()
            if self._lookahead() == MINUS and not char == BSLASH:
                f = char
                self._next()  # skip hyphen
                char = self._next()  # get far range
                if not char or (char in META_TOKENS):
                    raise NumberGeneratorSyntaxException(
                        "unexpected end of class range"
                    )
                chars += self._get_character_range(f, char)
            elif char == BSLASH:
                if self._lookahead() in META_TOKENS:
                    char = self._next()
                    chars += char
                    continue
                elif self._lookahead() in self._code:
                    char = self._next()
                    chars += self._code[char]
            elif char and char not in META_TOKENS:
                chars += char
            if char == RSQB:
                if self._lookahead() == LBRACE:
                    start, cnt = self._get_quantifier()
                else:
                    start = -1
                    cnt = 1
                break
            if char and char in META_TOKENS and not self._last() == BSLASH:
                raise NumberGeneratorSyntaxException(
                    f"Un-escaped character in class definition: {char}"
                )
            if not char:
                break  # pragma: no cover
        return CharacterSet(chars=chars, start=start, cnt=cnt)

    def _get_literal(self) -> Literal:
        chars = ""
        char = self._current()
        while True:
            if char and char == BSLASH:
                char = self._next()
                if char:
                    chars += char
                continue
            elif not char or (char in META_TOKENS):
                break  # pragma: no cover
            else:
                chars += char
            if self._lookahead() and self._lookahead() in META_TOKENS:
                break
            char = self._next()
        return Literal(chars=chars)

    def _get_sequence(self, level: int = 0) -> Sequence:
        seq = []
        op = ""
        left_operand = None
        sequence_closed = False
        while True:
            char = self._next()
            if not char:
                break
            is_last_bslash = self._last() == BSLASH
            if char and char not in META_TOKENS:
                seq.append(self._get_literal())
            elif char == LSQB and not is_last_bslash:
                seq.append(self._get_character_set())
            elif char == LPAR and not is_last_bslash:
                seq.append(self._get_sequence(level + 1))
            elif char == RPAR and not is_last_bslash:
                # end of this sequence
                if level == 0:
                    # there should be no parens here
                    raise NumberGeneratorSyntaxException("Extra closing parenthesis")
                sequence_closed = True
                break
            elif char == VBAR and not is_last_bslash:
                op = char
            else:
                if char in META_TOKENS and not is_last_bslash:
                    raise NumberGeneratorSyntaxException(
                        f"Un-escaped special character: {char}"
                    )

            if op and not left_operand:
                if not seq:
                    raise NumberGeneratorSyntaxException(
                        f"Operator: {op} with no left operand"
                    )
                left_operand = seq.pop()
            elif op and len(seq) >= 1 and left_operand:
                right_operand = seq.pop()

                if op == VBAR:
                    seq.append(SequenceOR(seq=[left_operand, right_operand]))
                op = ""
                left_operand = None

        # check for syntax errors
        if op:
            raise NumberGeneratorSyntaxException(
                f"Operator: {op} with no right operand"
            )
        if level > 0 and not sequence_closed:
            raise NumberGeneratorSyntaxException("Missing closing parenthesis")
        return Sequence(seq=seq)

    def render(self) -> str:
        return self._seq.render()


class PhoneNumber:
    def __init__(self, value: str) -> None:
        code = self._preparation(value)
        self._country = self._find(code)
        if not self._country:
            raise PhoneNumberNotFound(f'Not found country "{value}"')

    def __str__(self):
        return f"<{type(self).__name__}({self.info()})>"

    def _find(self, value: str) -> Optional[Dict[str, str]]:
        if country := ALTERNATIVE_FILE.get(value) or PATTERNS["data"].get(value):
            return country
        if alt_country := ALT_PATTERNS.get(value):
            return (
                alt_country
                if "pattern" in alt_country
                else self._find(alt_country["ref"])
            )
        if country_name := COUNTRY_NAME.get(value):
            return self._find(country_name["code"])
        if ico3 := ISO3.get(value):
            return self._find(ico3["code"])
        return None

    @staticmethod
    def _preparation(value: str) -> str:
        return re.sub(r"\W", "", value).upper()

    @staticmethod
    def info() -> str:
        return PATTERNS["info"]

    def get_code(self) -> str:
        return self._country["code"]

    def get_number(self, full: bool = True) -> str:
        return self.get_national(full) if RANDINT(0, 1) else self.get_mobile(full)

    def get_mobile(self, full: bool = True) -> str:
        number = NumberGenerator(
            pattern=self._country.get("mobile", self._country["pattern"])
        ).render()
        return f"+{self._country['code']}{number}" if full else number

    def get_national(self, full: bool = True) -> str:
        number = NumberGenerator(pattern=self._country["pattern"]).render()
        # Could not find problem
        if (
            number.startswith("49") and self._country["code"] == "49"
        ):  # pragma: no cover
            return self.get_national(full)
        return f"+{self._country['code']}{number}" if full else number
