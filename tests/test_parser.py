from typing import Any

from xdsl.parser import Span
from xuiua.ast import Array, Number, Spaces, Spanned, WordsItem
from xuiua.parser import Parser


def test_parse_number():
    parser = Parser(" 1.1", pos=1)

    assert parser.parse_optional_number() == Number("1.1", 1.1)


def test_parse_array():
    parser = Parser(" [1.0 2.3]", pos=1)

    def s(start: int, end: int, value: Any) -> Spanned[Any]:
        span = Span(start, end, parser.input)
        return Spanned(value, span)

    def n(f: str) -> Number:
        return Number(f, float(f))

    assert parser.parse_optional_array() == Array(
        None,
        (
            (
                s(2, 5, n("1.0")),
                s(5, 6, Spaces()),
                s(6, 9, n("2.3")),
            ),
        ),
        False,
        True,
    )


def test_parse_items():
    parser = Parser(" [1.0 2.3] [5 6]", pos=1)

    def s(start: int, end: int, value: Any) -> Spanned[Any]:
        span = Span(start, end, parser.input)
        return Spanned(value, span)

    def n(f: str) -> Number:
        return Number(f, float(f))

    assert parser.parse_items() == (
        WordsItem(
            (
                (
                    s(
                        1,
                        10,
                        Array(
                            None,
                            (
                                (
                                    s(2, 5, n("1.0")),
                                    s(5, 6, Spaces()),
                                    s(6, 9, n("2.3")),
                                ),
                            ),
                            False,
                            True,
                        ),
                    ),
                    s(10, 11, Spaces()),
                    s(
                        11,
                        16,
                        Array(
                            None,
                            (
                                (
                                    s(12, 13, n("5")),
                                    s(13, 14, Spaces()),
                                    s(14, 15, n("6")),
                                ),
                            ),
                            False,
                            True,
                        ),
                    ),
                ),
            ),
        ),
    )