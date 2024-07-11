import string
from dataclasses import dataclass, field
from itertools import chain
from random import choice, randint
from re import error, Pattern
from typing import Any, Dict, Callable, Sequence, Union

try:
    from re._parser import SubPattern
except ImportError:  # pragma: no cover
    from re import Pattern as SubPattern

try:
    import re._parser as parse
except ImportError:  # pragma: no cover
    import sre_parse as parse


class PatternError(Exception):
    """Not found country"""


_CATEGORIES: Dict[str, Callable[[], str]] = {
    "category_digit": lambda: string.digits,
    "category_not_digit": lambda: string.ascii_letters + string.punctuation,
    "category_space": lambda: string.whitespace,
    "category_not_space": lambda: string.printable.strip(),
    "category_word": lambda: string.ascii_letters + string.digits + "_",
    "category_not_word": lambda: "".join(set(string.printable).difference(string.ascii_letters + string.digits + "_")),
}


@dataclass
class RegEx:
    pattern: Union[Pattern, str]
    _cache: Dict[str, Any] = field(default_factory=dict, init=False, repr=False)
    _cases: Dict[str, Callable[[Any], Any]] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self):
        self._cases = {
            parse.LITERAL: lambda x: chr(x),
            parse.NOT_LITERAL: lambda x: choice(string.printable.replace(chr(x), "")),
            parse.AT: lambda x: "",
            parse.IN: lambda x: self._in(x),
            parse.ANY: lambda x: choice(string.printable.replace("\n", "")),
            parse.RANGE: lambda x: [chr(i) for i in range(x[0], x[1] + 1)],
            parse.CATEGORY: lambda x: _CATEGORIES[x](),
            parse.BRANCH: lambda x: "".join(self._state(i) for i in choice(x[1])),
            parse.SUBPATTERN: lambda x: self._group(x),
            parse.ASSERT: lambda x: "".join(self._state(i) for i in x[1]),
            parse.ASSERT_NOT: lambda x: "",
            parse.GROUPREF: lambda x: self._cache[x],
            parse.MIN_REPEAT: lambda x: self._repeat(*x),
            parse.MAX_REPEAT: lambda x: self._repeat(*x),
            parse.NEGATE: lambda x: [False],
        }

    def _repeat(self, start_range: int, end_range: int, value: str) -> str:
        times = randint(start_range, min((end_range, 100)))
        return "".join("".join(self._state(i) for i in value) for _ in range(times))

    def _group(self, value: Sequence[Any]) -> str:
        result = "".join(self._state(i) for i in value[-1])
        if value[0]:
            self._cache[value[0]] = result
        return result

    def _in(self, value: Any) -> Any:
        candidates = list(chain(*(self._state(i) for i in value)))
        if candidates[0] is False:
            candidates = list(set(string.printable).difference(candidates[1:]))
        return choice(candidates)

    def _state(self, state: Any) -> Any:
        opcode, value = state
        if opcode == parse.CATEGORY:
            value = value.name.lower()
        return self._cases[opcode](value)

    def _get_string(self, parsed: SubPattern) -> str:
        return "".join(self._state(state) for state in parsed)

    def generate(self) -> str:
        try:
            parsed = parse.parse(self.pattern.pattern if isinstance(self.pattern, Pattern) else self.pattern)
        except error:
            raise PatternError(f"Invalid regex: {self.pattern!r}")
        result = self._get_string(parsed)
        self._cache.clear()
        return result
