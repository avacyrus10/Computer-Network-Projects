from dataclasses import dataclass
from enum import Enum


class ScopeType(Enum):
    PARAM = 1
    LOCAL = 2
    FUNC = 3
    GLOBAL = 4


class VarType(Enum):
    INT = 1
    VOID = 2
    ARR = 3


@dataclass
class Token:
    lexeme: str = ''
    type: str = ''
    context: str = ''
    line_num: int = 0


@dataclass
class Row:
    lexeme: str
    addr: str
    scope: int
    param_len: int
    rv_address: str
    scope_type: ScopeType
    var_type: VarType


class SymbolTable:

    def __init__(self):
        self.rows = []

    def add_row(self, lexeme=None, addr=None, scope=None, param_len=None, rv_address=None, scope_type=None, var_type=None ):
        for row in self.rows:
            if lexeme == row.lexeme:
                return
        row = Row(lexeme=lexeme, addr=addr, scope=scope, param_len=param_len, rv_address=rv_address,
                  scope_type=scope_type, var_type=var_type)
        self.rows.append(row)
