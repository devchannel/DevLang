from combinators import *
from tokenList import *

def parse(tokens):
    token_list = TokenList(tokens)
    result = parse_ABinaryOp().run(token_list)
    return result

def parse_ABinaryOp():
    return parse_AConstant() + Tag(Symbol.Subtract) + parse_AConstant() ^ (lambda x: ABinaryOp(*x))

def abin_op_func(parsed):
    ((x,y),z) = parsed
    return ABinaryOp(y,x,z)

def parse_AConstant():
    return Tag(Type.Integer32) ^ AConstant

