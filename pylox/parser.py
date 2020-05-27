from dataclasses import dataclass

from pylox.token import Token


class Expr(object):
    pass


class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr
