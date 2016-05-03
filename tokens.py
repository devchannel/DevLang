from enum import Enum


class Operator(Enum):
    Add = '+'
    Subtract = '-'
    Multiply = '*'
    Divide = '/'
    FunctionOneLine = '='
    FunctionMultiLine = '=>'
    ArgumentList = '->'
    TypeSeparator = '|'


# The ones in the list in the lexer need to be first:
# (OpenBracket, CloseBracket, Delimiter)
class Special(Enum):
    OpenBracket = 0
    CloseBracket = 1
    Delimiter = 2
    EOF = 3
    Unknown = 4


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
