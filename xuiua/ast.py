from __future__ import annotations

from typing import Generic, NamedTuple, TypeAlias, TypeVar
from xdsl.parser import Span as CodeSpan


class Ident:
    "A Uiua identifier."

    name: str


class Signature:
    args: int
    "The number of arguments the function pops off the stack."
    outputs: int
    "The number of values the function pushes onto the stack."


T = TypeVar("T")


class Spanned(Generic[T], NamedTuple):
    value: T
    span: CodeSpan


class NamedModuleKind(NamedTuple):
    named_module: Spanned[Ident]


class ModuleKind: ...


class ImportLine:
    tilde_span: CodeSpan
    "The span of the ~"

    items: list[Spanned[Ident]]
    "The imported items"


class ScopedModule(NamedTuple):
    open_span: CodeSpan
    "The span of the opening delimiter"
    kind: ModuleKind
    items: list["Item"]
    imports: ImportLine | None
    code_span: CodeSpan
    "The span of the closing delimiter"


class WordsItem(NamedTuple):
    """Just some code."""

    lines: list[list[Spanned[Word]]]


class BindingItem(NamedTuple):
    name: str
    arrow_span: CodeSpan
    public: bool
    array_macro: bool
    signature: Signature | None
    words: list[Word]


class ImportItem(NamedTuple):
    name: Spanned[Ident]
    "The name given to the imported module"

    tilde_span: CodeSpan
    "The span of the ~"

    path: Spanned[str]
    "The import path"

    lines: list[ImportLine | None]
    "The import lines"


class ModuleItem(NamedTuple):
    scoped_module: ScopedModule


Item: TypeAlias = ScopedModule | WordsItem | BindingItem | ModuleItem


# region Word


class Number(NamedTuple):
    str_val: str
    float_val: float


class Array(NamedTuple):
    "A stack array notation term"

    signature: Spanned[Signature] | None
    "The array's inner signature"

    lines: list[list[Spanned[Word]]]
    "The words in the array"

    boxes: bool
    "Whether this is a box array"

    closed: bool
    "Whether a closing bracket was found"


class Comment(NamedTuple):
    value: str


class Spaces(NamedTuple):
    "Only used for formatting"


Word: TypeAlias = Number | Array | Comment | Spaces

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
#     Primitive(Primitive),
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
