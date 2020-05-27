from dataclasses import dataclass

from pylox.token import Token


class Expr(object):
    pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass
class Grouping(Expr):
    expression: Expr


@dataclass
class Literal(Expr):
    value: Any


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr


class Visitor:
    def __str__(self):
        return self.__class__.__name__


    def visit_binary_expr(expr: binary):
        pass


    def visit_grouping_expr(expr: grouping):
        pass


    def visit_literal_expr(expr: literal):
        pass


    def visit_unary_expr(expr: unary):
        pass




