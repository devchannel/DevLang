import unittest
from DevLang.lexer import Lexer
from DevLang.errorHandler import ErrorHandler
from DevLang.tokens import Type, Symbol

class TestTokenConversion(unittest.TestCase):

    def setUp(self):
        self.errorH = ErrorHandler()

    def test_type_conversion(self):
        lexer = Lexer("5 'a' \"aa\" 5.0 True False", self.errorH)
        vals = [Type.Integer32, Type.Char, Type.String,
                Type.Float, Type.Bool, Type.Bool]
        tokens = lexer.tokenize()

        self.compare(vals, tokens)

    def test_operator_conversion(self):
        lexer = Lexer("+ - * / && || ! < <= > >= == !=", self.errorH)
        operators = [Symbol.Add, Symbol.Subtract, Symbol.Multiply, Symbol.Divide,
                    Symbol.And, Symbol.Or, Symbol.Not, Symbol.Lt, Symbol.Lte,
                    Symbol.Gt, Symbol.Gte, Symbol.Eq, Symbol.Neq]
        tokens = lexer.tokenize()

        self.compare(operators, tokens)


    def test_keyword_conversion(self):
        lexer = Lexer("If Else End Return For While in Case", self.errorH)
        keywords = [Symbol.If, Symbol.Else, Symbol.End, Symbol.Return, 
                    Symbol.For, Symbol.While, Symbol.In, Symbol.Case]
        tokens = lexer.tokenize()

        self.compare(keywords, tokens)

    def test_Symbol_conversion(self):
        lexer = Lexer("= -> => ( ) \{ \} ; : ..", self.errorH)
        symbols = [Symbol.FunctionOneLine, Symbol.ArgumentList,
                   Symbol.FunctionMultiLine, Symbol.OpenBracket, 
                   Symbol.CloseBracket, Symbol.OpenBrace, 
                   Symbol.CloseBrace, Symbol.Delimiter,
                   Symbol.Colon, Symbol.Range]
        tokens = lexer.tokenize()

        self.compare(symbols, tokens)

    def compare(self, symbols, tokens):
        for i in range(len(symbols)):
            self.assertEqual(symbols[i], tokens[i].type)
