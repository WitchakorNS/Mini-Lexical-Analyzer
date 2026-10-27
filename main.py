import argparse
from pathlib import Path
import sys
from typing import Optional, Sequence, TextIO

from src.lexer import LexicalError, MiniLexer
from src.output_formatter import format_error, format_token
from src.symbol_table import SymbolTable


def analyze(source: str, output: Optional[TextIO] = None) -> SymbolTable:
    if output is None:
        output = sys.stdout
    symbol_table = SymbolTable()
    for token in MiniLexer().tokenize(source):
        print(format_token(token, symbol_table), file=output)
    return symbol_table


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Mini Lexical Analyzer ด้วย Python และ SLY")
    parser.add_argument("source", type=Path, help="เส้นทางไฟล์ source code .txt (UTF-8)")
    args = parser.parse_args(argv)
    if args.source.suffix.lower() != ".txt":
        parser.error("source file must have a .txt extension")

    try:
        source = args.source.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        print(f"File error: {error}", file=sys.stderr)
        return 2

    try:
        analyze(source)
    except LexicalError as error:
        print(format_error(error))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
