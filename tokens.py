from enum import Enum


class Operator(Enum):
    plus = '+'
    sub = '-'
    mult = '*'
    div = '/'
    func_one = '='
    func_multi = '=>'
    arg_list = '->'
    type_sep = '|'


class Special(Enum):
    EOF = 0
    Whitespace = 1
    NewLine = 2


class Type(Enum):
    Integer = 0
    Char = 1
    String = 2


class Keyword(Enum):
    Return = 0


class Token():
    def __init__(self, type, value, loc):
        # For now, one of the Operators or an EOF
        self.type = type
        self.value = value
        self.loc = loc

    def __repr__(self):
        return "({}, {}, {})".format(self.type.name, self.value, self.loc)

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return len(self.value)
