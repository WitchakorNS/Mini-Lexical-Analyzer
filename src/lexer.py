import re

from sly import Lexer


class LexicalError(ValueError):

    def __init__(self, character: str, lineno: int, index: int, reason: str = "unexpected character"):
        self.character = character
        self.lineno = lineno
        self.index = index
        self.reason = reason
        super().__init__(f"Lexical error: unexpected character {character}")


class MiniLexer(Lexer):
    tokens = {
        "PLUS", "MINUS", "TIMES", "DIVIDE", "ASSIGN", "GT", "GE", "LT", "LE",
        "EQ", "INCREMENT", "DECREMENT", "LPAREN", "RPAREN", "SEMICOLON",
        "IF", "THEN", "ELSE", "ENDIF", "WHILE", "DO", "ENDWHILE", "PRINT",
        "NEWLINE", "READ", "IDENTIFIER", "INTEGER", "STRING",
    }

    ignore = " \t\f\v"

    ignore_line_comment = r'//[^\r\n]*'

    @_(r'/\*[\s\S]*?\*/')
    def ignore_block_comment(self, token):
        self.lineno += len(re.findall(r'\r\n|\r|\n', token.value))

    @_(r'/\*')
    def ignore_unterminated_comment(self, token):
        raise LexicalError("/", token.lineno, token.index, "unterminated block comment")

    @_(r'\r\n|[\r\n]')
    def ignore_newline(self, token):
        self.lineno += 1

    STRING = r'"[^"\r\n]*"'

    @_(r'"')
    def ignore_unterminated_string(self, token):
        raise LexicalError('"', token.lineno, token.index, "unterminated string")

    @_(r'[0-9]+[a-zA-Z][a-zA-Z0-9]*')
    def ignore_invalid_identifier(self, token):
        raise LexicalError(token.value[0], token.lineno, token.index, "identifier starts with a digit")

    IDENTIFIER = r'[a-zA-Z][a-zA-Z0-9]*'
    IDENTIFIER['if'] = "IF"
    IDENTIFIER['then'] = "THEN"
    IDENTIFIER['else'] = "ELSE"
    IDENTIFIER['endif'] = "ENDIF"
    IDENTIFIER['while'] = "WHILE"
    IDENTIFIER['do'] = "DO"
    IDENTIFIER['endwhile'] = "ENDWHILE"
    IDENTIFIER['print'] = "PRINT"
    IDENTIFIER['newline'] = "NEWLINE"
    IDENTIFIER['read'] = "READ"

    INTEGER = r'[0-9]+'

    GE = r'>='
    LE = r'<='
    EQ = r'=='
    INCREMENT = r'\+\+'
    DECREMENT = r'--'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r'='
    GT = r'>'
    LT = r'<'

    LPAREN = r'\('
    RPAREN = r'\)'
    SEMICOLON = r';'

    def error(self, token):
        raise LexicalError(token.value[0], token.lineno, token.index)
