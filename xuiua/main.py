from pathlib import Path

from xdsl.context import MLContext
from xdsl.dialects.builtin import Builtin
from xdsl.dialects.func import Func
from xdsl.parser import Input
from xdsl.parser import Parser as XDSLParser

from xuiua.dialect import UIUA
from xuiua.frontend.ir_gen import build_module
from xuiua.frontend.parser import Parser as UIUAParser
from xuiua.printer import Printer


def run_parse(src: Path):
    """
    Prints the parse tree, or an error message.
    """

    source = open(src).read()
    parser = UIUAParser(Input(source, str(src)))
    items = parser.parse_items()

    printer = Printer()

    items.print(printer)


def run_lower(src: Path, passes_str: str | None):
    """
    Prints the IR for the given target
    """

    assert not passes_str

    ctx = MLContext()
    ctx.register_dialect("builtin", lambda: Builtin)
    ctx.register_dialect("func", lambda: Func)
    ctx.register_dialect("uiua", lambda: UIUA)

    source = open(src).read()
    match src.suffix:
        case ".ua":
            parser = UIUAParser(Input(source, str(src)))
            items = parser.parse_items()
            module = build_module(items)
        case ".mlir":
            parser = XDSLParser(ctx, source, str(src))
            module = parser.parse_module()
        case unknown:
            raise ValueError(f"Cannot parse file with extension {unknown}")

    print(str(module))


def run(src: Path):
    print("Cannot compile and run UIUA yet")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="XUIUA compiler")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Parse subcommand
    parse_parser = subparsers.add_parser("parse", help="Parse and print the AST")
    parse_parser.add_argument("src", type=Path, help="Source file to parse")

    # Lower subcommand
    lower_parser = subparsers.add_parser(
        "lower", help="Lower Uiua to target representation"
    )
    lower_parser.add_argument("src", type=Path, help="Source file to parse")
    lower_parser.add_argument("passes", nargs="?", type=str, default="")

    # Run subcommand
    run_parser = subparsers.add_parser("run", help="Compile and run UIUA code")
    run_parser.add_argument("src", type=Path, help="Source file to run")

    args = parser.parse_args()

    if args.command == "parse":
        run_parse(args.src)
    elif args.command == "lower":
        run_lower(args.src, args.passes)
    elif args.command == "run":
        run(args.src)


if __name__ == "__main__":
    main()
