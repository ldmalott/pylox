from typing import List, Any

from pylox.token_type import TokenType
from pylox.token import Token

from loguru import logger


def is_digit(c: str):
    return c is not None and c >= '0' and c <= '9'


def is_alpha(c: str):
    return c is not None and ((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_')


def is_alphanumeric(c: str):
    return is_alpha(c) or is_digit(c)


keywords = {
    'and': TokenType.AND,
    'class': TokenType.CLASS,
    'else': TokenType.ELSE,
    'false': TokenType.FALSE,
    'for': TokenType.FOR,
    'fun': TokenType.FUN,
    'if': TokenType.IF,
    'nil': TokenType.NIL,
    'or': TokenType.OR,
    'print': TokenType.PRINT,
    'return': TokenType.RETURN,
    'super': TokenType.SUPER,
    'this': TokenType.THIS,
    'true': TokenType.TRUE,
    'var': TokenType.VAR,
    'while': TokenType.WHILE
}


class Scanner(object):
    def __init__(self, source: str, error_handler: Any):
        self.source = source
        self.error_handler = error_handler
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> List[Token]:
        self.tokens = []
        while not self.at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self):
        character = self.advance()

        if character == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif character == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif character == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif character == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif character == ',':
            self.add_token(TokenType.COMMA)
        elif character == '.':
            self.add_token(TokenType.DOT)
        elif character == '-':
            self.add_token(TokenType.MINUS)
        elif character == '+':
            self.add_token(TokenType.PLUS)
        elif character == ';':
            self.add_token(TokenType.SEMICOLON)
        elif character == '*':
            self.add_token(TokenType.STAR)
        elif character == '!':
            self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif character == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif character == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif character == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif character == '/':
            # Check for comment string
            if self.match('/'):
                while self.peek() != '\n' and not self.at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif character in (' ', '\r', '\t'):
            pass
        elif character == '\n':
            self.line += 1

        elif character == '"':
            self.add_string()
        else:
            if is_digit(character):
                self.add_number()
            elif is_alpha(character):
                self.add_identifier()
            else:
                self.error_handler.error(self.line, 'Unexpected character.')

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def match(self, expected: str):
        if self.at_end():
            return False

        if self.source[self.current] == expected:
            self.current += 1
            return True

        return False

    def peek(self) -> str:
        if self.at_end():
            return None
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return None
        return self.source[self.current + 1]

    def add_token(self, token_type: TokenType, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def add_string(self):
        while self.peek() != '"' and not self.at_end():
            # support multi-line strings, increment line if newline encounteredj
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.at_end():
            self.error_handler.error(self.line, 'Unterminated string.')
            return

        # closing "
        self.advance()

        # trim surrounding quotes from literal
        value = self.source[self.start + 1: self.current - 1]
        self.add_token(TokenType.STRING, literal=value)

    def add_number(self):
        while is_digit(self.peek()):
            self.advance()

        # consume fractional part
        if self.peek() == '.' and is_digit(self.peek_next()):
            self.advance()

            while is_digit(self.peek()):
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start: self.current]))

    def add_identifier(self):
        while is_alphanumeric(self.peek()):
            self.advance()

        text = self.source[self.start: self.current]
        token_type = keywords.get(text, TokenType.IDENTIFIER)

        self.add_token(token_type)
