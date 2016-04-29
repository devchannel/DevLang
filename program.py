import lexer as L
import tokenParser as P


# Maybe we should change the implementation of Lexer and tokenParser
# to a pure implementation
def main():
    lexer = L.Lexer("((1-2)+((3+4)))")
    # lexer = L.Lexer("4 + (5 - 2) ")
    tokens = lexer.tokenize()
    parser = P.Parser(tokens)
    parser.parse()

    lexer1 = L.Lexer("1 / 2 * 5")
    tokens1 = lexer1.tokenize()
    parser1 = P.Parser(tokens1)
    parser1.parse()

main()