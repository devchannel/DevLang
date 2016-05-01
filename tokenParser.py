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

    # returns a copy of the tokenlist
    def copy(self):
        return TokenList(self.tokens, self.pos)


# Basic parser class
class Parser:
    # Will be overridden by subclasses
    def run(self, token_list):
        return None

    # called by + operator
    def __add__(self, other):
        return Concatenate(self, other)

    # called by * operator
    def __mul__(self, other):
        return Exp(self, other)

    # called by | operator
    def __or__(self, other):
        return Alternate(self, other)

    # called by ^ operator
    def __xor__(self, function):
        return Process(self, function)


class Reserved(Parser):
    def __init__(self, token):
        self.token = token

    def run(self, token_list):
        t = token_list.peek()
        if t.value == self.token.value and t.type == self.token.type:
            return token_list.next()
        return None


class Tag(Parser):
    def __init__(self, token_type):
        self.token_type = token_type

    def run(self, token_list):
        if token_list.peek().type == self.token_type:
            return token_list.next()
        return None


# Returns a tuple of the results of two parsers
# return None if either parser fails
# does not advance the tokenlist on failure
class Concatenate(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def run(self, token_list):
        token_list_copy = token_list.copy()
        left_result = self.left.run(token_list_copy)
        if left_result:
            right_result = self.right.run(token_list_copy)
            if right_result:
                token_list.pos = token_list_copy.pos
                return (left_result, right_result)
        return None


def test(tokens):
    token_list = TokenList(tokens)
    print((Tag(Type.Integer) + Reserved(Token(Operator.Subtract, '-', 0)) + Tag(Type.Integer)).run(token_list))
    print(token_list)


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