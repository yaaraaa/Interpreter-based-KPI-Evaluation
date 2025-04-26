import operator
from .lexer import TokenType
from abc import ABC, abstractmethod


# Map token types to corresponding operations
binary_operations = {
    'PLUS': operator.add,
    'MINUS': operator.sub,
    'MUL': operator.mul,
    'DIV': operator.floordiv,
}


class OperatorFactory:
    """Factory to create AST nodes for binary operations."""

    @staticmethod
    def create(left, token, right):
        if token.type in binary_operations:
            return BinOp(left, token, right)
        else:
            raise ValueError(f"Unsupported operator: {token.type}")


class ASTNode(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def accept(self, visitor):
        return visitor.visit_bin_op(self)


class Num(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def accept(self, visitor):
        return visitor.visit_num(self)


class UnaryOp(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_unary_op(self)


class RegexOp(ASTNode):
    def __init__(self, value, pattern):
        self.value = value
        self.pattern = pattern

    def accept(self, visitor):
        return visitor.visit_regex_op(self)


# Define operator precedence
PRECEDENCE = {
    'PLUS': 1,
    'MINUS': 1,
    'MUL': 2,
    'DIV': 2,
    'MOD': 2,
    # Add more operators with their precedence as needed
}


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise ValueError("Invalid syntax")

    def factor(self):
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        elif token.type == TokenType.REGEX:
            return self.regex_operation()

    def regex_operation(self):
        """Parse a regex operation: Regex(value, "pattern")"""
        self.eat(TokenType.REGEX)
        self.eat(TokenType.LPAREN)
        value_token = self.current_token  # Get the actual value in place of ATTR
        if value_token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
        elif value_token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
        else:
            raise ValueError("Expected a STRING or INTEGER token")

        self.eat(TokenType.COMMA)  # Expect comma here

        pattern = self.current_token
        self.eat(TokenType.PATTERN)
        self.eat(TokenType.RPAREN)
        return RegexOp(value_token, pattern)

    def parse_expression(self, precedence_level=1):
        node = self.factor()
        while self.current_token.type in PRECEDENCE and PRECEDENCE[self.current_token.type] >= precedence_level:
            token = self.current_token
            self.eat(token.type)
            node = OperatorFactory.create(left=node, token=token, right=self.parse_expression(PRECEDENCE[token.type] + 1))
        return node

    def expr(self):
        return self.parse_expression()

    def parse(self):
        node = self.expr()
        if self.current_token.type != TokenType.EOF:
            raise ValueError("Unexpected token after expression")
        return node
