from .tokens import *
from .grammar import *


# Stores a list of tokens and the position in the list
class TokenList:
    def __init__(self, tokens, pos=0):
        # The list of tokens from the lexer
        self.tokens = tokens
        self.pos = pos

    def  __repr__(self):
        return str(self.tokens[self.pos:])

    def __str__(self):
        return str(self.tokens[self.pos:])

    # Return the next token
    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        raise Exception("Attempted to look past last token")

    # Move forward and return current token
    def next(self):
        self.pos += 1
        if self.pos-1 < len(self.tokens):
            return self.tokens[self.pos-1]
        raise Exception("Attempted to move past last token")

    # return next token and move forward if it matches the given type
    # if it does not match, return None
    def eat(self, token_type):
        if self.peek().type == token_type:
            return self.next()
        return None

    # the same as eat but it takes a list of tokens instead of a single one
    def eat_any(self, token_types):
        if self.peek().type in token_types:
            return self.next()
        return None

    # Ruturns a list of the next n tokens
    def peek_many(self, n):
        if self.pos+n < len(self.tokens):
            return self.tokens[self.pos:self.pos+n]
        raise Exception("Attempted to look past last token")


    def copy(self):
        return TokenList(self.tokens, self.pos)