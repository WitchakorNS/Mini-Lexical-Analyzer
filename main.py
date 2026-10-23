"""ผู้รับผิดชอบ: เตย — อ่านไฟล์และเชื่อม Lexer, Symbol Table และตัวแสดงผล."""

import argparse
from pathlib import Path
import sys
from typing import Optional, Sequence, TextIO

from src.lexer import LexicalError, MiniLexer
from src.output_formatter import format_error, format_token
from src.symbol_table import SymbolTable


# ผู้รับผิดชอบ: เตย — วิเคราะห์ทีละ token เพื่อเก็บผลก่อน error และไม่อ่าน token ถัดไป
def analyze(source: str, output: Optional[TextIO] = None) -> SymbolTable:
    """แสดงผลตามลำดับที่พบ และส่ง exception ให้ผู้เรียกเมื่อเกิด lexical error."""
    if output is None:
        output = sys.stdout
    symbol_table = SymbolTable()  # สร้างใหม่ทุกครั้ง ป้องกันชื่อจากไฟล์ก่อนหน้าปะปน
    for token in MiniLexer().tokenize(source):
        print(format_token(token, symbol_table), file=output)
    return symbol_table


# ผู้รับผิดชอบ: เตย — รับ path จาก command line และแยก error ของไฟล์กับ error ของภาษา
def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Mini Lexical Analyzer ด้วย Python และ SLY")
    parser.add_argument("source", type=Path, help="เส้นทางไฟล์ source code .txt (UTF-8)")
    args = parser.parse_args(argv)
    if args.source.suffix.lower() != ".txt":
        parser.error("source file must have a .txt extension")

    try:
        # utf-8-sig อ่านได้ทั้ง UTF-8 ปกติและไฟล์ที่มี BOM จาก editor บน Windows
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


# ผู้รับผิดชอบ: เตย — การ import เพื่อทดสอบจะไม่ทำให้โปรแกรม CLI เริ่มทำงาน
if __name__ == "__main__":
    raise SystemExit(main())
