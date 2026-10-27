"""กฎ SLY สำหรับ Mini Lexical Analyzer.

การจำแนก token ใช้ Regular Expression ของ SLY ไม่ใช่การวนตรวจอักขระเอง
"""

import re

from sly import Lexer


# exception ทำให้ generator หยุดทันทีโดยไม่ข้าม error ไปต่อ
class LexicalError(ValueError):
    """เก็บอักขระ ตำแหน่ง และเหตุผล โดยคงข้อความแสดงผลตามรูปแบบโจทย์."""

    def __init__(self, character: str, lineno: int, index: int, reason: str = "unexpected character"):
        self.character = character
        self.lineno = lineno
        self.index = index
        self.reason = reason
        super().__init__(f"Lexical error: unexpected character {character}")


class MiniLexer(Lexer):
    # รวมชื่อ token ที่ใช้เป็นสัญญาระหว่าง Lexer กับ Formatter
    tokens = {
        "PLUS", "MINUS", "TIMES", "DIVIDE", "ASSIGN", "GT", "GE", "LT", "LE",
        "EQ", "INCREMENT", "DECREMENT", "LPAREN", "RPAREN", "SEMICOLON",
        "IF", "THEN", "ELSE", "ENDIF", "WHILE", "DO", "ENDWHILE", "PRINT",
        "NEWLINE", "READ", "IDENTIFIER", "INTEGER", "STRING",
    }

    # ข้าม whitespace ระหว่าง token; newline นับแยกด้านล่าง
    ignore = " \t\f\v"

    # วางกฎ comment ก่อน DIVIDE เพื่อไม่แยก // หรือ /* เป็น /
    ignore_line_comment = r'//[^\r\n]*'

    @_(r'/\*[\s\S]*?\*/')
    def ignore_block_comment(self, token):
        # Non-greedy จบที่ */ แรก และนับ CRLF เป็นการขึ้นบรรทัดใหม่ครั้งเดียว
        self.lineno += len(re.findall(r'\r\n|\r|\n', token.value))

    @_(r'/\*')
    def ignore_unterminated_comment(self, token):
        # ข้อตกลงกลุ่ม: เมื่อกฎ block comment สมบูรณ์ไม่ match ให้หยุดที่ / เปิด
        raise LexicalError("/", token.lineno, token.index, "unterminated block comment")

    @_(r'\r\n|[\r\n]')
    def ignore_newline(self, token):
        self.lineno += 1

    # เก็บ double quote ไว้ใน value สำหรับผลลัพธ์ตามโจทย์
    # Backslash เป็นอักขระธรรมดา ไม่แปล escape sequence และไม่ escape เครื่องหมาย quote
    STRING = r'"[^"\r\n]*"'

    # ถ้าไม่มี quote ปิดในบรรทัด ให้ error ที่ quote เปิด
    @_(r'"')
    def ignore_unterminated_string(self, token):
        raise LexicalError('"', token.lineno, token.index, "unterminated string")

    # ปฏิเสธชื่อขึ้นต้นด้วยตัวเลขก่อนกฎ INTEGER
    # ข้อตกลงกลุ่ม: 1score เป็นชื่อผิดกฎ ไม่แยกเป็น INTEGER 1 และ IDENTIFIER score
    @_(r'[0-9]+[a-zA-Z][a-zA-Z0-9]*')
    def ignore_invalid_identifier(self, token):
        raise LexicalError(token.value[0], token.lineno, token.index, "identifier starts with a digit")

    # ชื่อต้องขึ้นต้นด้วยตัวอักษรอังกฤษ ห้าม underscore
    IDENTIFIER = r'[a-zA-Z][a-zA-Z0-9]*'
    # Remap หลัง match ชื่อเต็ม ทำให้ if1/iffy เป็น Identifier และแยก case ถูกต้อง
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

    # จำนวนเต็มไม่ติดลบ เก็บ lexeme เดิม เช่น 001 ไม่แปลงเป็น 1
    INTEGER = r'[0-9]+'

    # กฎสองอักขระต้องมาก่อนกฎสั้น เพราะ SLY เลือกตามลำดับกฎ
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

    # วงเล็บและ semicolon เป็น token แยกจาก operator
    LPAREN = r'\('
    RPAREN = r'\)'
    SEMICOLON = r';'

    # SLY ส่งข้อความที่เหลือมา จึงเลือกอักขระแรกที่ไม่ตรงกฎ
    def error(self, token):
        raise LexicalError(token.value[0], token.lineno, token.index)
