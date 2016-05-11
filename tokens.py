from enum import Enum

# not sure what I should have called this
class Symbol(Enum):
    Add = '+'
    Subtract = '-'
    Multiply = '*'
    Divide = '/'
    # And = "&&"
    # Or = "||"
    # Not = "!"
    # Lt = "<"
    # Lte = "<="
    # Gt = ">"
    # Gte = ">="
    # Eq = "=="
    FunctionOneLine = '='
    ArgumentList = '->'
    FunctionMultiLine = '=>'
    If = "If"
    Else = "Else"
    End = "End"
    Return = "Return"
    For = "For"
    While = "While"
    In = "in"
    Case = "Case"
    TrueVal = "True"
    FalseVal = "False"
    OpenBracket = "("
    CloseBracket = ")"
    OpenBrace = "{"
    CloseBrace = "}"
    Delimiter = ";"
    Colon = ":"
    Dot = "."
    Or = "||"


class Special(Enum):
    EOF = 0
    Unknown = 1
    Name = 2
    TypeName = 3


class Type(Enum):
    Integer32 = "int32"
    Integer64 = "int64"
    Char = "char"
    String = "string"
    Float = "float"
    Bool = "bool"


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
