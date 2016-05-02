from tokens import *
from grammar import *


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


# The old arithmetic expression parser, needs to be reworked

# # TODO: Operator precedence
# def parse_AExpr(self):
#     left = None
#     tk = self.peek()
#     if tk.type == Special.OpenBracket: # If we encounter an open bracket
#         self.next()
#         expr = self.parse_AExpr()       # The brackets enclose an expression
#         self.eat(Special.CloseBracket) # It should end with a closing bracket
#         left = ABrackets(expr)
#     elif tk.type == Type.Integer: 
#         left = self.next()
#         tk = self.peek()
#         if self.is_operator(tk.type):  # Integer can be part of another expression
#             self.next()
#             op = tk.type
#             right = self.parse_AExpr() # For now we don't care what is on the rhs
#             left = ABinaryOp(op, AConstant(left.value), right)
#         else:
#              left = AConstant(left.value)
    
#     tk = self.peek()
#     if self.is_operator(tk.type):  # left can be part of some outer expression
#         self.next()
#         op = tk.type
#         right = self.parse_AExpr()
#         return ABinaryOp(op, left, right)
#     else:
#         return left