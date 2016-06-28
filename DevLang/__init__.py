from .lexer import Lexer
from .parsers import parse
from .errorHandler import ErrorHandler
from .analyzer import Analyzer
from .codegen import codegen


# Maybe we should change the implementation of Lexer and tokenParser
# to a pure implementation
def compile(path):
    with open(path) as file:
        x = file.read()

    errorHandler = ErrorHandler()
    lexer = Lexer(x, errorHandler)
    tokens = lexer.tokenize()

    # if there is any errors, print them
    if errorHandler:
        print(errorHandler)

    #print("\n".join(str(x) for x in tokens))

    result = parse(tokens, errorHandler)

    if errorHandler:
        print(errorHandler)

    #print(result)

    analysis = Analyzer(result)
    analysis.analyze()
    sym_table = analysis.symbol_table

    gen_filename = path.split("/")[-1].split(".")[-2] + ".S"
    codegen(result, gen_filename, sym_table)
