import lexer as L
import parsers as P
from errorHandler import ErrorHandler


# Maybe we should change the implementation of Lexer and tokenParser
# to a pure implementation
def main():
    with open("test.devlang") as file:
        x = file.read()

    errorHandler = ErrorHandler()
    lexer = L.Lexer(x, errorHandler)
    tokens = lexer.tokenize()

    # if there is any errors, print them and exit
    if errorHandler:
        print(errorHandler)
        return

    #print("\n".join(str(x) for x in tokens))

    result = P.parse(tokens)
    print(result)

main()