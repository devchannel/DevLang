import unittest
from DevLang.lexer import Lexer
from DevLang.errorHandler import ErrorHandler
from DevLang.tokens import Type, Symbol

class TestLexingFailure(unittest.TestCase):

    def test_or_typename(self):
        lexer = Lexer("||Char|", ErrorHandler())
        tokens = lexer.tokenize()

        self.assertEqual(len(lexer.errorHandler.errors), 1)

    def test_unknown_symbol(self):
        lexer = Lexer(". _", ErrorHandler())
        tokens = lexer.tokenize()

        self.assertEqual(len(lexer.errorHandler.errors), 2)