from pathlib import Path

from xdsl.parser import Input
from xdsl.parser import Parser as XDSLParser
from xdsl.passes import PipelinePass
from xdsl.utils.parse_pipeline import parse_pipeline

from xuiua.compile import get_ctx
from xuiua.frontend.ir_gen import build_module
from xuiua.frontend.parser import Parser as UIUAParser
from xuiua.passes import AVAILABLE_PASSES
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

    ctx = get_ctx()

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

    if passes_str:
        pipeline = PipelinePass(
            tuple(
                pass_type.from_pass_spec(spec)
                for pass_type, spec in PipelinePass.build_pipeline_tuples(
                    AVAILABLE_PASSES, parse_pipeline(passes_str)
                )
            ),
        )
        pipeline.apply(ctx, module)

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
