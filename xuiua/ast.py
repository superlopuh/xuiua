from __future__ import annotations


from enum import StrEnum
from typing import Callable, Generic, NamedTuple, TypeAlias, TypeVar
from xdsl.parser import Span as CodeSpan

from xuiua.printer import Printer


class Ident:
    "A Uiua identifier."

    name: str

    def print(self, printer: Printer):
        printer.print(self.name)


class Signature:
    args: int
    "The number of arguments the function pops off the stack."
    outputs: int
    "The number of values the function pushes onto the stack."

    def print(self, printer: Printer):
        printer.print(f"{self.args}|{self.outputs}")


T = TypeVar("T")


class Spanned(Generic[T], NamedTuple):
    value: T
    span: CodeSpan

    @staticmethod
    def _print_span(code_span: CodeSpan, printer: Printer):
        printer.print(f"{code_span.start}-{code_span.end}")

    def print(self, printer: Printer, value_print: Callable[[T, Printer], None]):
        Spanned._print_span(self.span, printer)
        printer.print(": ")
        value_print(self.value, printer)


class NamedModuleKind(NamedTuple):
    named_module: Spanned[Ident]

    def print(self, printer: Printer):
        self.named_module.print(printer, Ident.print)


class ModuleKind: ...


class ImportLine:
    tilde_span: CodeSpan
    "The span of the ~"

    items: tuple[Spanned[Ident], ...]
    "The imported items"

    def print(self, printer: Printer) -> None:
        raise NotImplementedError


class ScopedModule(NamedTuple):
    open_span: CodeSpan
    "The span of the opening delimiter"
    kind: ModuleKind
    items: tuple[Item, ...]
    imports: ImportLine | None
    code_span: CodeSpan
    "The span of the closing delimiter"

    def print(self, printer: Printer) -> None:
        raise NotImplementedError


class WordsItem(NamedTuple):
    """Just some code."""

    lines: tuple[tuple[Spanned[Word], ...], ...]

    def print(self, printer: Printer):
        with printer.indented():
            printer.print("Words(")
            printer.print("\n[")
            with printer.indented():
                for line in self.lines:
                    printer.print("\n[")
                    with printer.indented():
                        for item in line:
                            printer.print("\n")
                            item.print(printer, print_word)
                            printer.print(",")
                    printer.print("\n],")
            printer.print("\n]")
        printer.print("\n)")


class BindingItem(NamedTuple):
    name: str
    arrow_span: CodeSpan
    public: bool
    array_macro: bool
    signature: Signature | None
    words: tuple[Word, ...]

    def print(self, printer: Printer) -> None:
        raise NotImplementedError


class ImportItem(NamedTuple):
    name: Spanned[Ident]
    "The name given to the imported module"

    tilde_span: CodeSpan
    "The span of the ~"

    path: Spanned[str]
    "The import path"

    lines: tuple[ImportLine | None, ...]
    "The import lines"


class ModuleItem(NamedTuple):
    scoped_module: ScopedModule

    def print(self, printer: Printer) -> None:
        raise NotImplementedError


class Items(NamedTuple):
    items: tuple[Item, ...]

    def print(self, printer: Printer):
        with printer.indented():
            printer.print("[")
            for item in self.items:
                printer.print("\n")
                item.print(printer)
                printer.print(",")
        printer.print("\n]\n")


Item: TypeAlias = ScopedModule | WordsItem | BindingItem | ModuleItem


# region Word


class Number(NamedTuple):
    str_val: str
    float_val: float

    def print(self, printer: Printer) -> None:
        printer.print('"')
        printer.print(self.str_val)
        printer.print('"')


class Array(NamedTuple):
    "A stack array notation term"

    signature: Spanned[Signature] | None
    "The array's inner signature"

    lines: tuple[tuple[Spanned[Word], ...], ...]
    "The words in the array"

    boxes: bool
    "Whether this is a box array"

    closed: bool
    "Whether a closing bracket was found"

    def print(self, printer: Printer) -> None:
        printer.print("arr(")
        assert len(self.lines) == 1
        with printer.indented():
            for spanned_word in self.lines[0]:
                printer.print("\n")
                spanned_word.value.print(printer)
                printer.print(",")
        printer.print("\n)")


class Comment(NamedTuple):
    value: str

    def print(self, printer: Printer) -> None:
        printer.print("#")
        printer.print(self.value)


class Spaces(NamedTuple):
    "Only used for formatting"

    def print(self, printer: Printer) -> None:
        printer.print("<spaces>")


class PrimitiveSpelling(StrEnum):
    """
    from refs.rs

    (2, Add, DyadicPervasive, ("add", '+')),

    First item is the number of inputs, if there are parens then that's the number of outputs.
    """

    ADD = "+"
    DUPLICATE = "."

    def num_inputs(self) -> int:
        match self:
            case PrimitiveSpelling.ADD:
                return 2
            case PrimitiveSpelling.DUPLICATE:
                return 1

    def num_outputs(self) -> int:
        match self:
            case PrimitiveSpelling.ADD:
                return 1
            case PrimitiveSpelling.DUPLICATE:
                return 2


class Primitive(NamedTuple):
    spelling: PrimitiveSpelling

    def print(self, printer: Printer):
        printer.print(self.spelling.name)


Word: TypeAlias = Number | Array | Comment | Spaces | Primitive


def print_word(word: Word, printer: Printer) -> None:
    word.print(printer)


# pub enum Word {
#     -Number(String, f64),
#     Char(String),
#     String(String),
#     MultilineString(Vec<Sp<String>>),
#     FormatString(Vec<String>),
#     MultilineFormatString(Vec<Sp<Vec<String>>>),
#     Label(String),
#     Ref(Ref),
#     IncompleteRef {
#         path: Vec<RefComponent>,
#         in_macro_arg: bool,
#     },
#     Strand(Vec<Sp<Word>>),
#     Undertied(Vec<Sp<Word>>),
#     -Array(Arr),
#     Func(Func),
#     Pack(FunctionPack),
#     -Primitive(Primitive),
#     SemicolonPop,
#     Modified(Box<Modified>),
#     Placeholder(PlaceholderOp),
#     StackSwizzle(StackSwizzle),
#     ArraySwizzle(ArraySwizzle),
#     -Comment(String),
#     Spaces,
#     BreakLine,
#     UnbreakLine,
#     SemanticComment(SemanticComment),
#     OutputComment {
#         i: usize,
#         n: usize,
#     },
# }

# endregion
