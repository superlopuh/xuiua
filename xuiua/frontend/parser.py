import re
from typing import Any, Callable, Sequence, TypeVar
from xdsl.parser import Input, Span
from xdsl.utils.lexer import Position

from xuiua.frontend.ast import (
    BindingItem,
    Comment,
    Func,
    Item,
    Items,
    Modified,
    Number,
    Primitive,
    PrimitiveClass,
    PrimitiveSpelling,
    Spaces,
    Word,
    WordsItem,
    Array,
    Spanned,
)

T = TypeVar("T")


SKIP_COMMENT = True


class ParseError(Exception):
    position: Position
    message: str

    def __init__(self, position: Position, message: str) -> None:
        self.position = position
        self.message = message
        super().__init__(f"ParseError at {self.position}: {self.message}")


NEWLINE = re.compile(r"\n")
NOT_NEWLINE = re.compile(r"[^\n]*")
SPACES = re.compile(r"[^\S\n]")
NUMBER = re.compile(r"\d+(\.\d+)?")
PRIMITIVE = re.compile("|".join(re.escape(p.value) for p in PrimitiveSpelling))
IDENTIFIER = re.compile(r"[a-zA-Z]\w+")
"""
A regular expression for an identifier, currently letter followed by a number of letters or numbers.

This is the actual UIUA impl, eventually would be good to move to it:
``` rust
pub fn is_ident_char(c: char) -> bool {
    c.is_alphabetic() && !"ⁿₙπτηℂλ".contains(c) || SUBSCRIPT_NUMS.contains(&c)
}
```
"""


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

    # region Base parsing functions

    def parse_optional_chars(self, chars: str):
        if self.input.content.startswith(chars, self.pos):
            self.pos += len(chars)
            return chars

    def parse_optional_pattern(self, pattern: re.Pattern[str]):
        if (match := pattern.match(self.input.content, self.pos)) is not None:
            self.pos = match.regs[0][1]
            return self.input.content[match.pos : self.pos]

    # endregion
    # region: Helpers

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

    # endregion
    # region: Words

    def parse_optional_number(self) -> Number | None:
        if (str_val := self.parse_optional_pattern(NUMBER)) is not None:
            float_val = float(str_val)
            return Number(str_val, float_val)

    def parse_optional_primitive(self) -> Primitive | Modified | None:
        if (prim_val := self.parse_optional_pattern(PRIMITIVE)) is None:
            return None
        prim = PrimitiveSpelling(prim_val)
        if prim.primitive_class() == PrimitiveClass.AGGREGATING_MODIFIER:
            # Need to peek ahead
            self.parse_optional_spaces()
            word = self.expect("aggregated word", Parser.parse_optional_word)
            return Modified(Primitive(prim), (word,))
        return Primitive(prim)

    def parse_optional_array(self) -> Array | None:
        if self.parse_optional_chars("[") is None:
            return None

        # TODO: signature
        lines = self.parse_word_lines()
        # TODO: boxed (ragged) array
        self.expect("close array", lambda parser: parser.parse_optional_chars("]"))

        return Array(None, lines, False, True)

    def parse_optional_func(self) -> Func | None:
        if self.parse_optional_chars("(") is None:
            return None

        # TODO: signature
        lines = self.parse_word_lines()
        # TODO: boxed (ragged) array
        self.expect("close paren", lambda parser: parser.parse_optional_chars(")"))

        return Func(None, lines, True)

    def parse_optional_comment(self) -> Comment | None:
        if self.parse_optional_chars("#") is None:
            return None

        value = self.expect(
            "comment", lambda parser: parser.parse_optional_pattern(NOT_NEWLINE)
        )
        comment = Comment(value)
        return None if SKIP_COMMENT else comment

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
        line = self.parse_many(Parser.parse_optional_word)
        return line

    def parse_word_lines(self) -> tuple[tuple[Spanned[Word], ...], ...]:
        lines = self.parse_many_separated(
            Parser.parse_word_line,
            lambda parser: parser.parse_optional_pattern(NEWLINE),
        )
        # Skip empty lines
        return tuple(line for line in lines if line)

    # endregion
    # region: Items

    def parse_words_item(self) -> WordsItem | None:
        pos = self.pos
        lines = self.parse_word_lines()
        if pos == self.pos:
            # did not make progress
            return None
        return WordsItem(lines)

    def parse_binding_item(self) -> BindingItem | None:
        pos = self.pos
        if (name := self.parse_optional_pattern(IDENTIFIER)) is None:
            return None
        self.parse_optional_spaces()
        arrow_start_pos = self.pos
        if self.parse_optional_chars("←") is None:
            self.pos = pos
            return None
        arrow_end_pos = self.pos

        words = self.parse_word_line()

        self.parse_optional_pattern(NEWLINE)

        return BindingItem(
            name,
            Span(arrow_start_pos, arrow_end_pos, self.input),
            True,
            False,
            None,
            words,
        )

    def parse_optional_item(self) -> Item | None:
        if not self.remaining:
            return None
        if (binding := self.parse_binding_item()) is not None:
            return binding
        pos = self.pos
        words_item = self.parse_words_item()
        if pos == self.pos:
            raise ParseError(
                self.pos, f"Could not parse remaining string: {self.remaining}"
            )
        return words_item

    def parse_items(self) -> Items:
        items = self.parse_many(Parser.parse_optional_item)
        items = tuple(
            item for item in items if not isinstance(item, WordsItem) or item.lines
        )
        return Items(items)

    # endregion


WORD_PARSERS = (
    Parser.parse_optional_array,
    Parser.parse_optional_func,
    Parser.parse_optional_comment,
    Parser.parse_optional_number,
    Parser.parse_optional_primitive,
    Parser.parse_optional_spaces,
)
