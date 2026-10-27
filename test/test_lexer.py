"""Tests สำหรับ Mini Lexical Analyzer.

รันจากรากโปรเจกต์ด้วย python -m pytest -q
"""

from io import StringIO
from pathlib import Path
import subprocess
import sys

import pytest

from main import analyze, main
from src.lexer import LexicalError, MiniLexer
from src.output_formatter import format_error, format_token
from src.symbol_table import SymbolTable


# helpers ใช้ร่วมกันโดยตรวจทั้งชนิด token และ lexeme ต้นฉบับ
ROOT = Path(__file__).resolve().parents[1]


def tokenize(source):
    return [(token.type, token.value) for token in MiniLexer().tokenize(source)]


def render(source):
    output = StringIO()
    table = analyze(source, output)
    return output.getvalue(), table


# Operators ครบ 12 ตัว วงเล็บ semicolon และกฎที่ซ้อนกัน
@pytest.mark.parametrize("lexeme,kind", [
    ("+", "PLUS"), ("-", "MINUS"), ("*", "TIMES"), ("/", "DIVIDE"),
    ("=", "ASSIGN"), (">", "GT"), (">=", "GE"), ("<", "LT"), ("<=", "LE"),
    ("==", "EQ"), ("++", "INCREMENT"), ("--", "DECREMENT"),
])
def test_operators_all(lexeme, kind):
    assert tokenize(lexeme) == [(kind, lexeme)]


def test_operators_long_before_short():
    assert tokenize(">=> <== === +++ ---") == [
        ("GE", ">="), ("GT", ">"), ("LE", "<="), ("ASSIGN", "="),
        ("EQ", "=="), ("ASSIGN", "="), ("INCREMENT", "++"), ("PLUS", "+"),
        ("DECREMENT", "--"), ("MINUS", "-"),
    ]


def test_delimiters_adjacent():
    assert tokenize("(A);") == [
        ("LPAREN", "("), ("IDENTIFIER", "A"), ("RPAREN", ")"), ("SEMICOLON", ";"),
    ]


# Keyword แบบตรงคำและตรง case เท่านั้น
@pytest.mark.parametrize("keyword,kind", [
    ("if", "IF"), ("then", "THEN"), ("else", "ELSE"), ("endif", "ENDIF"),
    ("while", "WHILE"), ("do", "DO"), ("endwhile", "ENDWHILE"),
    ("print", "PRINT"), ("newline", "NEWLINE"), ("read", "READ"),
])
def test_keywords_all(keyword, kind):
    assert tokenize(keyword) == [(kind, keyword)]


@pytest.mark.parametrize("name", ["If", "IF", "Print", "READ", "if1", "iffy", "newlines"])
def test_keywords_case_and_prefix_are_identifiers(name):
    assert tokenize(name) == [("IDENTIFIER", name)]


@pytest.mark.parametrize("name", ["A", "B", "x", "score", "id1", "id2", "student123"])
def test_identifier_accepted(name):
    assert tokenize(name) == [("IDENTIFIER", name)]


@pytest.mark.parametrize("source,character", [
    ("1score", "1"), ("123abc", "1"), ("_score", "_"), ("student_name", "_"),
    ("@id", "@"), ("ชื่อ", "ช"),
])
def test_identifier_rejected(source, character):
    with pytest.raises(LexicalError) as caught:
        tokenize(source)
    assert caught.value.character == character


# Integer เก็บค่าข้อความเดิมและไม่รวมเครื่องหมายลบ
@pytest.mark.parametrize("value", ["0", "123", "12345", "001", "9" * 5000])
def test_integer_accepted(value):
    assert tokenize(value) == [("INTEGER", value)]


def test_integer_negative_is_operator_and_integer():
    assert tokenize("-10") == [("MINUS", "-"), ("INTEGER", "10")]


def test_integer_decimal_is_error_at_dot():
    stream = MiniLexer().tokenize("1.5")
    assert next(stream).value == "1"
    with pytest.raises(LexicalError) as caught:
        next(stream)
    assert caught.value.character == "."


@pytest.mark.parametrize("source", ['""', '"Hello World"', '"Score is 100"',
    '"// /* */ @ _ +"', '"ภาษาไทย"', '"a\tb"', r'"a\nb"'])
def test_string_accepted(source):
    assert tokenize(source) == [("STRING", source)]


@pytest.mark.parametrize("source", ['"Hello World', '"Hello\nWorld"', '"Hello\rWorld"'])
def test_string_unterminated_or_multiline(source):
    with pytest.raises(LexicalError) as caught:
        tokenize(source)
    assert caught.value.character == '"'
    assert caught.value.reason == "unterminated string"


def test_string_backslash_does_not_escape_quote():
    # โจทย์ยังไม่รองรับ escape: quote หลัง backslash จบ String ตามปกติ
    source = '"a' + "\\" + '" B'
    assert tokenize(source) == [("STRING", source[:-2]), ("IDENTIFIER", "B")]


# Comment ไม่ผลิต token และไม่ตรวจอักขระภายในเป็น error
@pytest.mark.parametrize("comment", [
    "// @ _ \" ignored", "/* @ _ \" ignored */", "/* first\nsecond\nthird */",
    "/**/", "/* one */ /* two */", "/* outer /* no nesting */",
])
def test_comment_ignored(comment):
    assert tokenize(comment) == []


def test_comment_and_division_priority():
    assert tokenize("A/2/* @ ignored */+B// rest\n/C") == [
        ("IDENTIFIER", "A"), ("DIVIDE", "/"), ("INTEGER", "2"), ("PLUS", "+"),
        ("IDENTIFIER", "B"), ("DIVIDE", "/"), ("IDENTIFIER", "C"),
    ]


def test_comment_non_greedy():
    assert tokenize("/* one */ A /* two */ B") == [("IDENTIFIER", "A"), ("IDENTIFIER", "B")]


@pytest.mark.parametrize("source", ["/* never closed", "/*/", "/*", "/*\n@"])
def test_comment_unterminated(source):
    with pytest.raises(LexicalError) as caught:
        tokenize(source)
    assert (caught.value.character, caught.value.index) == ("/", 0)
    assert caught.value.reason == "unterminated block comment"


def test_whitespace_newline_keyword_is_a_token():
    assert tokenize(" \t\r\n\n\r\f\vnewline\n") == [("NEWLINE", "newline")]


@pytest.mark.parametrize("ending", ["\n", "\r\n", "\r"])
def test_whitespace_and_comment_line_numbers(ending):
    source = f"A{ending}/* first{ending}second */{ending}B @ C"
    stream = MiniLexer().tokenize(source)
    assert next(stream).lineno == 1
    assert next(stream).lineno == 4
    with pytest.raises(LexicalError) as caught:
        next(stream)
    assert caught.value.lineno == 4
    assert caught.value.index == source.index("@")


def test_lexical_error_stops_generator_immediately():
    stream = MiniLexer().tokenize("A @ B")
    assert next(stream).value == "A"
    with pytest.raises(LexicalError, match="^Lexical error: unexpected character @$"):
        next(stream)
    assert list(stream) == []


# เก็บเฉพาะ Identifier ไม่ซ้ำ โดยแยก case และคงลำดับที่พบ
def test_symbol_table_new_duplicate_and_case():
    table = SymbolTable()
    assert table.add("A") is True
    assert table.add("A") is False
    assert table.add("a") is True
    assert "A" in table
    assert "B" not in table
    assert len(table) == 2
    assert table.identifiers == ("A", "a")


def test_symbol_table_only_identifiers():
    _, table = render('if A == 123 then print "hidden"; (A) // ignored\nendif')
    assert table.identifiers == ("A",)


def test_output_exact_labels_quotes_and_order():
    output, _ = render('A A + if 123 "Hello World" ();')
    assert output == (
        'new identifier: A\nidentifier "A" already in symbol table\n'
        'operator: +\nkeyword: if\ninteger: 123\nstring: "Hello World"\n'
        'left parenthesis: (\nright parenthesis: )\nsemicolon: ;\n'
    )


@pytest.mark.parametrize("lexeme", ["+", "-", "*", "/", "=", ">", ">=", "<", "<=", "==", "++", "--"])
def test_output_operators(lexeme):
    output, table = render(lexeme)
    assert output == f"operator: {lexeme}\n"
    assert len(table) == 0


@pytest.mark.parametrize("word", ["if", "then", "else", "endif", "while", "do", "endwhile", "print", "newline", "read"])
def test_output_keywords(word):
    output, table = render(word)
    assert output == f"keyword: {word}\n"
    assert len(table) == 0


def test_output_error_format():
    assert format_error(LexicalError("@", 1, 2)) == "Lexical error: unexpected character @"


def test_output_no_symbol_after_error():
    table = SymbolTable()
    with pytest.raises(LexicalError):
        for token in MiniLexer().tokenize("A @ B"):
            format_token(token, table)
    assert table.identifiers == ("A",)


# Golden outputs จาก PDF หน้า 8–9 ไม่สร้าง expected ด้วย Lexer
SAMPLE1_OUTPUT = '''new identifier: A
operator: +
new identifier: B
operator: -
operator: *
keyword: if
keyword: then
new identifier: id1
new identifier: id2
identifier "id1" already in symbol table
string: "Hello World"
'''

SAMPLE2_OUTPUT = '''keyword: read
new identifier: A
semicolon: ;
keyword: read
new identifier: B
semicolon: ;
keyword: if
identifier "A" already in symbol table
operator: >=
identifier "B" already in symbol table
keyword: then
keyword: print
string: "A is greater"
semicolon: ;
keyword: print
keyword: newline
semicolon: ;
keyword: endif
identifier "A" already in symbol table
operator: ++
semicolon: ;
'''


@pytest.mark.parametrize("filename,expected,exit_code", [
    ("sample1.txt", SAMPLE1_OUTPUT, 0),
    ("sample2.txt", SAMPLE2_OUTPUT, 0),
    ("lexical_error.txt", "new identifier: A\nLexical error: unexpected character @\n", 1),
])
def test_integration_cli_pdf_examples(filename, expected, exit_code):
    result = subprocess.run(
        [sys.executable, str(ROOT / "main.py"), str(ROOT / "inputs" / filename)],
        capture_output=True, text=True, check=False, cwd=ROOT,
    )
    assert result.returncode == exit_code
    assert result.stdout == expected
    assert result.stderr == ""


def test_integration_independent_symbol_tables():
    first_output, first_table = render("A")
    second_output, second_table = render("A")
    assert first_output == second_output == "new identifier: A\n"
    assert first_table is not second_table


@pytest.mark.parametrize("source", ["", " \t\n", "// comment", "/* comment */"])
def test_integration_empty_or_comment_only(source):
    output, table = render(source)
    assert output == ""
    assert len(table) == 0


def test_integration_all_token_types():
    source = (ROOT / "inputs/all_tokens.txt").read_text(encoding="utf-8")
    assert {token.type for token in MiniLexer().tokenize(source)} == MiniLexer.tokens


def test_integration_utf8_bom_and_path_with_spaces(tmp_path, capsys):
    source_file = tmp_path / "example input.txt"
    source_file.write_text('print "สวัสดี";', encoding="utf-8-sig")
    assert main([str(source_file)]) == 0
    assert capsys.readouterr().out == 'keyword: print\nstring: "สวัสดี"\nsemicolon: ;\n'


def test_integration_missing_file(tmp_path, capsys):
    assert main([str(tmp_path / "missing.txt")]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("File error: ")


def test_integration_invalid_encoding(tmp_path, capsys):
    source_file = tmp_path / "invalid.txt"
    source_file.write_bytes(b"\xff")
    assert main([str(source_file)]) == 2
    assert capsys.readouterr().err.startswith("File error: ")


def test_integration_wrong_extension(tmp_path, capsys):
    with pytest.raises(SystemExit) as caught:
        main([str(tmp_path / "source.py")])
    assert caught.value.code == 2
    assert ".txt extension" in capsys.readouterr().err
