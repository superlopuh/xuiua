from pathlib import Path
from typing import Literal

from xdsl.parser import Input

from xuiua.frontend.ir_gen import build_module
from xuiua.frontend.parser import Parser
from xuiua.printer import Printer


def run_parse(src: Path):
    """
    Prints the parse tree, or an error message.
    """

    source = open(src).read()
    parser = Parser(Input(source, str(src)))
    items = parser.parse_items()

    printer = Printer()

    items.print(printer)


def run_lower(src: Path, target: Literal["uiua"]):
    """
    Prints the IR for the given target
    """

    source = open(src).read()
    parser = Parser(Input(source, str(src)))
    items = parser.parse_items()

    module = build_module(items)

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
    lower_parser.add_argument("target", type=str, choices=["uiua"])

    # Run subcommand
    run_parser = subparsers.add_parser("run", help="Compile and run UIUA code")
    run_parser.add_argument("src", type=Path, help="Source file to run")

    args = parser.parse_args()

    if args.command == "parse":
        run_parse(args.src)
    elif args.command == "lower":
        run_lower(args.src, args.target)
    elif args.command == "run":
        run(args.src)


if __name__ == "__main__":
    main()
