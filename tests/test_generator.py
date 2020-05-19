import re

import pytest

from phone_gen._generator import NumberGenerator, NumberGeneratorException, NumberGeneratorSyntaxException


def test_one():
    data = NumberGenerator(r'[9-0][\d]{4}').render()
    assert re.match(r'\d{5}', data)


def test_two():
    NumberGenerator(r'[0-9][\d\{]').render()


SYNTAX_ERROR_PATTERN = (
    r'[136-9]\d{7}',
    r'[136-9][\d{7}',
    r'[136-9]\d]{7}',
    r'[136-9][\d]{7,8}',
    r'[136-9][\d]{7:}',
    r'(4[\d]{8})|([1-9][\d]{7}',
    r'(4[\d]{8})|[1-9][\d]{7})',
    r'(4[\d]{8})|',
    r'|([1-9][\d]{7})',
    r'(4[\d]{8})|([1-][\d]{7})'
)


@pytest.mark.parametrize('pattern', SYNTAX_ERROR_PATTERN)
def test_syntax_error(pattern):
    with pytest.raises(NumberGeneratorSyntaxException):
        NumberGenerator(pattern).render()


@pytest.mark.parametrize('pattern', (r'[0-9][\d]{',))
def test_base_error(pattern):
    with pytest.raises(NumberGeneratorException):
        NumberGenerator(pattern).render()
