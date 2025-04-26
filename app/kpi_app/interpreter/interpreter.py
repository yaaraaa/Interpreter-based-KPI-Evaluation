from abc import ABC, abstractmethod
from .lexer import TokenType
from .parser import binary_operations
import re


class NodeVisitor(ABC):
    @abstractmethod
    def visit_bin_op(self, node):
        pass

    @abstractmethod
    def visit_num(self, node):
        pass

    @abstractmethod
    def visit_unary_op(self, node):
        pass

    @abstractmethod
    def visit_regex_op(self, node):
        pass


class Interpreter(NodeVisitor):
    def visit_bin_op(self, node):
        operation = binary_operations.get(node.op.type)
        if not operation:
            raise ValueError(f"Operation {node.op.type} not supported.")
        return operation(node.left.accept(self), node.right.accept(self))

    def visit_num(self, node):
        return node.value

    def visit_unary_op(self, node):
        op_type = node.op.type
        if op_type == TokenType.PLUS:
            return +node.expr.accept(self)
        elif op_type == TokenType.MINUS:
            return -node.expr.accept(self)

    def visit_regex_op(self, node):
        value = str(node.value.value)
        pattern = node.pattern.value
        return bool(re.match(pattern, value))

    def interpret(self, tree):
        return tree.accept(self)
