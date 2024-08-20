import re
from typing import Any, Callable, Sequence, TypeVar
from xdsl.parser import Input, Span
from xdsl.utils.lexer import Position

from xuiua.ast import (
    Comment,
    Item,
    Items,
    Number,
    Spaces,
    Word,
    WordsItem,
    Array,
    Spanned,
)

T = TypeVar("T")


class ParseError(Exception):
    position: Position
    message: str

    def __init__(self, position: Position, message: str) -> None:
        self.position = position
        self.message = message
        super().__init__(f"ParseError at {self.position}: {self.message}")


NEWLINE = re.compile(r"\n")
NOT_NEWLINE = re.compile(r"[^\n]")
SPACES = re.compile(r"\s")
NUMBER = re.compile(r"\d+(\.\d+)?")


class Parser:
    input: Input
    pos: int

    def __init__(self, input: Input | str, pos: int = 0):
        if isinstance(input, str):
            input = Input(input, "<unknown>")
        self.input = input
        self.pos = pos

    @property
    def remaining(self) -> str:
        return self.input.content[self.pos :]

    # Base parsing functions

    def parse_optional_chars(self, chars: str):
        if self.input.content.startswith(chars, self.pos):
            self.pos += len(chars)
            return chars

    def parse_optional_pattern(self, pattern: re.Pattern[str]):
        if (match := pattern.match(self.input.content, self.pos)) is not None:
            self.pos = match.regs[0][1]
            return self.input.content[match.pos : self.pos]

    # Helpers

    def parse_many(self, element: Callable[["Parser"], T | None]) -> tuple[T, ...]:
        if (first := element(self)) is None:
            return ()
        res = [first]
        while (el := element(self)) is not None:
            res.append(el)
        return tuple(res)

    def parse_many_separated(
        self,
        element: Callable[["Parser"], T | None],
        separator: Callable[["Parser"], Any | None],
    ) -> tuple[T, ...]:
        if (first := element(self)) is None:
            return ()
        res = [first]
        while separator(self) is not None:
            el = self.expect("element", element)
            res.append(el)
        return tuple(res)

    def parse_optional_list(
        self,
        el: Callable[["Parser"], T | None],
        separator: Callable[["Parser"], Any | None],
        end: Callable[["Parser"], Any | None],
    ) -> list[T] | None:
        if end(self) is not None:
            return []
        if (first := el(self)) is None:
            return None
        res = [first]
        while end(self) is None:
            self.expect("separator", separator)
            element = self.expect("element", el)
            res.append(element)
        return res

    def expect(self, message: str, parse: Callable[["Parser"], T | None]) -> T:
        if (parsed := parse(self)) is None:
            raise ParseError(self.pos, message)
        return parsed

    def parse_one_of(
        self, parsers: Sequence[Callable[["Parser"], T | None]]
    ) -> T | None:
        for parser in parsers:
            if (parsed := parser(self)) is not None:
                return parsed

    def spanned(self, parser: Callable[["Parser"], T | None]) -> Spanned[T] | None:
        start = self.pos
        if (res := parser(self)) is not None:
            span = Span(start, self.pos, self.input)
            return Spanned(res, span)

    # Words

    def parse_optional_number(self) -> Number | None:
        if (str_val := self.parse_optional_pattern(NUMBER)) is not None:
            float_val = float(str_val)
            return Number(str_val, float_val)

    def parse_optional_array(self) -> Array | None:
        if self.parse_optional_chars("[") is None:
            return None

        # TODO: signature
        lines = self.parse_word_lines()
        # TODO: boxed (ragged) array
        self.expect("close array", lambda parser: parser.parse_optional_chars("]"))

        return Array(None, lines, False, True)

    def parse_optional_comment(self) -> Comment | None:
        if self.parse_optional_chars("#") is None:
            return None

        value = self.expect(
            "comment", lambda parser: parser.parse_optional_pattern(NOT_NEWLINE)
        )
        return Comment(value)

    def parse_optional_spaces(self) -> Spaces | None:
        if self.parse_optional_pattern(SPACES) is not None:
            return Spaces()

    def parse_optional_word(self) -> Spanned[Word] | None:
        return self.spanned(lambda parser: parser.parse_one_of(WORD_PARSERS))

    def parse_word_line(self) -> tuple[Spanned[Word], ...]:
        """
        Parses consecutive words, delimited by newlines.
        Stops whenever it encounters a newline.
        """
        lines = self.parse_many(Parser.parse_optional_word)
        return lines

    def parse_word_lines(self) -> tuple[tuple[Spanned[Word], ...], ...]:
        lines = self.parse_many_separated(
            Parser.parse_word_line,
            lambda parser: parser.parse_optional_pattern(NEWLINE),
        )
        return lines

    # Items

    def parse_words_item(self) -> WordsItem:
        lines = self.parse_word_lines()
        return WordsItem(lines)

    def parse_optional_item(self) -> Item | None:
        if self.remaining:
            return self.parse_words_item()

    def parse_items(self) -> Items:
        items = self.parse_many(Parser.parse_optional_item)
        return Items(items)


WORD_PARSERS = (
    Parser.parse_optional_number,
    Parser.parse_optional_spaces,
    Parser.parse_optional_array,
    Parser.parse_optional_comment,
)
