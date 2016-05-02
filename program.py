import lexer as L
import parsers as P


# Maybe we should change the implementation of Lexer and tokenParser
# to a pure implementation
def main():
    lexer = L.Lexer("1 - 2")
    tokens = lexer.tokenize()
    result = P.parse(tokens)
    print(result)

main()