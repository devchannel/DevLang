from .lexer import Lexer
from .parsers import parse
from .errorHandler import ErrorHandler
from .type_checker import type_check


# Maybe we should change the implementation of Lexer and tokenParser
# to a pure implementation
def compile(path):
    with open(path) as file:
        x = file.read()

    errorHandler = ErrorHandler()
    lexer = Lexer(x, errorHandler)
    tokens = lexer.tokenize()

    # if there is any errors, print them and exit
    if errorHandler:
        print(errorHandler)
        return

    #print("\n".join(str(x) for x in tokens))

    result = parse(tokens, errorHandler)

    if errorHandler:
        print(errorHandler)
        return

    type_check(result)