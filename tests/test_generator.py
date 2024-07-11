import re

import pytest

from phone_gen._generator import RegEx, PatternError

REGEX = (
    r"\d{5}",
    r"#[a-fA-F0-9]{3,6}",
    r"[a-z0-9._%+-]+[a-z]@[a-z][a-z0-9-]+\.[a-z]{2,4}",
    r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)",
    r"^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])"
    r"[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$",
    r"^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$",
    r"[-a-zA-Z0-9@:%_\+.~#?&\/=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&\/=]*)?",
    r"^https?:\/\/[a-z0-9]{1,}\.[a-z]{2,3}$",
    r"^([A-Z][a-z]{1,15}\n){4,}[^\s]\w{1,15}\n\W{3}$",
)


@pytest.mark.parametrize("regex", REGEX)
def test_string(regex):
    value = RegEx(regex).generate()
    assert re.match(regex, value)


@pytest.mark.parametrize("regex", REGEX)
def test_pattern(regex):
    pattern = re.compile(regex)
    value = RegEx(regex).generate()
    assert pattern.match(value)


def test_error():
    with pytest.raises(PatternError):
        RegEx(".**").generate()
