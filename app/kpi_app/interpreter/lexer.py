from abc import ABC, abstractmethod


# Token Types
class TokenType:
    INTEGER = 'INTEGER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MUL = 'MUL'
    DIV = 'DIV'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    REGEX = 'REGEX'
    PATTERN = 'PATTERN'
    STRING = 'STRING'
    COMMA = 'COMMA'
    EOF = 'EOF'


# Define a dictionary to map operators to token types
OPERATORS = {
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.MUL,
    '/': TokenType.DIV,
    '(': TokenType.LPAREN,
    ')': TokenType.RPAREN,
}


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {repr(self.value)})"

    def __repr__(self):
        return self.__str__()


class TokenHandler(ABC):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    @abstractmethod
    def handle(self, lexer):
        """Try to generate a token. If not possible, call the next handler."""
        pass


class IntegerHandler(TokenHandler):
    def handle(self, lexer):
        if lexer.current_char is not None and lexer.current_char.isdigit():
            return Token(TokenType.INTEGER, lexer.integer())
        elif self.next_handler:
            return self.next_handler.handle(lexer)


class RegexHandler(TokenHandler):
    def handle(self, lexer):
        if lexer.current_char is not None and lexer.text[lexer.pos:lexer.pos + 5] == "Regex":
            lexer.pos += 5
            lexer.current_char = lexer.text[lexer.pos] if lexer.pos < len(lexer.text) else None
            return Token(TokenType.REGEX, 'Regex')
        elif self.next_handler:
            return self.next_handler.handle(lexer)


class OperatorHandler(TokenHandler):
    def handle(self, lexer):
        if lexer.current_char is not None and lexer.current_char in OPERATORS:
            token_type = OPERATORS[lexer.current_char]
            token = Token(token_type, lexer.current_char)
            lexer.advance()
            return token
        elif self.next_handler:
            return self.next_handler.handle(lexer)


class PatternHandler(TokenHandler):
    def handle(self, lexer):
        if lexer.current_char == '"':
            return Token(TokenType.PATTERN, lexer.regex_pattern())
        elif self.next_handler:
            return self.next_handler.handle(lexer)


class StringHandler(TokenHandler):
    def handle(self, lexer):
        if lexer.current_char is not None and lexer.current_char.isalpha():
            return Token(TokenType.STRING, lexer.string())
        elif self.next_handler:
            return self.next_handler.handle(lexer)


class CommaHandler(TokenHandler):
    def handle(self, lexer):
        if lexer.current_char == ',':
            lexer.advance()
            return Token(TokenType.COMMA, ',')
        elif self.next_handler:
            return self.next_handler.handle(lexer)


class ParenthesisHandler(TokenHandler):
    def handle(self, lexer):
        if lexer.current_char == '(':
            lexer.advance()
            return Token(TokenType.LPAREN, '(')
        elif lexer.current_char == ')':
            lexer.advance()
            return Token(TokenType.RPAREN, ')')
        elif self.next_handler:
            return self.next_handler.handle(lexer)


class EOFHandler(TokenHandler):
    def handle(self, lexer):
        if lexer.current_char is None:
            return Token(TokenType.EOF, None)
        elif self.next_handler:
            return self.next_handler.handle(lexer)


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        # Set up the chain of token handlers
        self.token_handler_chain = IntegerHandler(
            RegexHandler(
                OperatorHandler(
                    PatternHandler(
                        StringHandler(
                            CommaHandler(
                                ParenthesisHandler(
                                    EOFHandler()
                                )
                            )
                        )
                    )
                )
            )
        )

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def regex_pattern(self):
        result = ''
        if self.current_char == '"':
            self.advance()
            while self.current_char is not None and self.current_char != '"':
                result += self.current_char
                self.advance()
            self.advance() 
        return result

    def string(self):
        """Return a generic string token."""
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        """Use the token handler chain to get the next token."""
        self.skip_whitespace()
        return self.token_handler_chain.handle(self)
