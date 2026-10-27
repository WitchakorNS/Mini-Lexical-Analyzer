from sly.lex import Token

from .lexer import LexicalError
from .symbol_table import SymbolTable


OPERATOR_TYPES = frozenset({
    "PLUS", "MINUS", "TIMES", "DIVIDE", "ASSIGN", "GT", "GE", "LT", "LE",
    "EQ", "INCREMENT", "DECREMENT",
})
KEYWORD_TYPES = frozenset({
    "IF", "THEN", "ELSE", "ENDIF", "WHILE", "DO", "ENDWHILE", "PRINT", "NEWLINE", "READ",
})
TOKEN_LABELS = {
    **dict.fromkeys(OPERATOR_TYPES, "operator"),
    **dict.fromkeys(KEYWORD_TYPES, "keyword"),
    "INTEGER": "integer",
    "STRING": "string",
    "LPAREN": "left parenthesis",
    "RPAREN": "right parenthesis",
    "SEMICOLON": "semicolon",
}


def format_token(token: Token, symbol_table: SymbolTable) -> str:
    if token.type == "IDENTIFIER":
        if symbol_table.add(token.value):
            return f"new identifier: {token.value}"
        return f'identifier "{token.value}" already in symbol table'
    return f"{TOKEN_LABELS[token.type]}: {token.value}"


def format_error(error: LexicalError) -> str:
    return str(error)
