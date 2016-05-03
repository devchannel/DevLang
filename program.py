import lexer as L
import parsers as P
from errorHandler import ErrorHandler


# Maybe we should change the implementation of Lexer and tokenParser
# to a pure implementation
def main():
    errorHandler = ErrorHandler()
    lexer = L.Lexer("1 + 2", errorHandler)
    tokens = lexer.tokenize()

    # if there is any errors, print them and exit
    if errorHandler:
        print(errorHandler)
        return

    print(tokens)

    result = P.parse(tokens)
    print(result)

main()