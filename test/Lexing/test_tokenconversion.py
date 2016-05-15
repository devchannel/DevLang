import unittest
from source.lexer import Lexer
from source.errorHandler import ErrorHandler
from source.tokens import Type

class TestTokenConversion(unittest.TestCase):

    def setUp(self):
        self.errorH = ErrorHandler()

    def test_Integer32(self):
        lexer = Lexer("5", self.errorH)
        token = lexer.tokenize()[0]
        self.assertEqual(Type.Integer32, token.type)