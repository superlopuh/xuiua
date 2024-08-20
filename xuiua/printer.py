from contextlib import contextmanager
from typing import IO


class Printer:
    stream: IO[str] | None
    indentation_level: int
    indentation_factor: int

    def __init__(
        self,
        stream: IO[str] | None = None,
        *,
        indentation_level: int = 0,
        indentation_factor: int = 2,
    ) -> None:
        self.stream = stream
        self.indentation_level = indentation_level
        self.indentation_factor = indentation_factor

    def _print_new_line(
        self, indent: int | None = None, print_message: bool = True
    ) -> None:
        indent = self.indentation_level if indent is None else indent
        # Prints a newline, bypassing the `print_string` method
        print(file=self.stream)
        num_spaces = indent * self.indentation_factor
        # Prints indentation, bypassing the `print_string` method
        print(" " * num_spaces, end="", file=self.stream)
        self._current_column = num_spaces

    @contextmanager
    def indented(self, amount: int = 1):
        """
        Increases the indentation level by the provided amount
        for the duration of the context.

        Only affects new lines printed within the context.
        """

        self.indentation_level += amount
        try:
            yield
        finally:
            self.indentation_level -= amount

    def print(self, text: str, *, indent: int | None = None) -> None:
        """
        Prints a string to the printer's output.

        This function takes into account indentation level when
        printing new lines.
        If the indentation level is specified as 0, the string is printed as-is, if `None`
        then the `Printer` instance's indentation level is used.
        """

        num_newlines = text.count("\n")

        if not num_newlines:
            print(text, end="", file=self.stream)
            return

        indent = self.indentation_level if indent is None else indent
        lines = text.split("\n")

        # Line and column information is not computed ahead of time
        # as indent-aware newline printing may use it as part of
        # callbacks.
        print(lines[0], end="", file=self.stream)
        for line in lines[1:]:
            self._print_new_line(indent=indent)
            print(line, end="", file=self.stream)
            self._current_column += len(line)
