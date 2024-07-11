import re
import string
import sys
from dataclasses import dataclass, field
from itertools import chain
from random import choice, randint
from typing import Any, Dict, Callable, Sequence, Union, Final

try:
    import re._parser as parse
except ImportError:  # pragma: no cover
    import sre_parse as parse

kwargs = {"eq": True}
if sys.version_info >= (3, 11):
    kwargs.update({"slots": True})


class PatternError(Exception):
    """Not found country"""


_CATEGORIES: Final[Dict[int, str]] = {
    parse.CATEGORY_DIGIT: string.digits,
    parse.CATEGORY_NOT_DIGIT: string.ascii_letters + string.punctuation,
    parse.CATEGORY_SPACE: string.whitespace,
    parse.CATEGORY_NOT_SPACE: string.printable.strip(),
    parse.CATEGORY_WORD: string.ascii_letters + string.digits + "_",
    parse.CATEGORY_NOT_WORD: "".join(set(string.printable).difference(string.ascii_letters + string.digits + "_")),
}

_CASE: Final[Dict[int, Callable[[Any, Any], Any]]] = {
    parse.LITERAL: lambda p, x: chr(x),
    parse.NOT_LITERAL: lambda s, x: choice(string.printable.replace(chr(x), "")),
    parse.AT: lambda p, x: "",
    parse.IN: lambda p, x: p.in_state(x),
    parse.ANY: lambda p, x: choice(string.printable.replace("\n", "")),
    parse.RANGE: lambda p, x: [chr(i) for i in range(x[0], x[1] + 1)],
    parse.CATEGORY: lambda p, x: _CATEGORIES[x],
    parse.BRANCH: lambda p, x: "".join(p.state(i) for i in choice(x[1])),
    parse.SUBPATTERN: lambda p, x: p.group(x),
    parse.ASSERT: lambda p, x: "".join(p.state(i) for i in x[1]),
    parse.ASSERT_NOT: lambda p, x: "",
    parse.GROUPREF: lambda p, x: p.cache[x],
    parse.MIN_REPEAT: lambda p, x: p.repeat(*x),
    parse.MAX_REPEAT: lambda p, x: p.repeat(*x),
    parse.NEGATE: lambda p, x: [False],
}


@dataclass(**kwargs)
class _Parser:
    cache: Dict[str, Any] = field(default_factory=dict, init=False, repr=False)

    def repeat(self, start_range: int, end_range: int, value: str) -> str:
        times = randint(start_range, min((end_range, 100)))
        return "".join("".join(self.state(i) for i in value) for _ in range(times))

    def group(self, value: Sequence[Any]) -> str:
        result = "".join(self.state(i) for i in value[-1])
        if value[0]:
            self.cache[value[0]] = result
        return result

    def in_state(self, value: Any) -> Any:
        candidates = list(chain(*(self.state(i) for i in value)))
        if candidates[0] is False:
            candidates = list(set(string.printable).difference(candidates[1:]))
        return choice(candidates)

    def state(self, state: Any) -> Any:
        opcode, value = state
        return _CASE[opcode](self, value)

    def value(self, pattern: re.Pattern) -> str:
        parsed = parse.parse(pattern.pattern)
        result = "".join(self.state(state) for state in parsed)
        self.cache.clear()
        return result


@dataclass(**kwargs)
class RegEx:
    pattern: Union[re.Pattern, str] = field(init=True, repr=True)
    _parser: _Parser = field(default_factory=_Parser, init=False, repr=False)

    def __post_init__(self):
        try:
            self.pattern = re.compile(self.pattern)
        except re.error as e:
            raise PatternError(f"Invalid pattern: {self.pattern!r}") from e

    def generate(self) -> str:
        return self._parser.value(self.pattern)
