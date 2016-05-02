from combinators import *
from tokenList import *

def parse(tokens):
    token_list = TokenList(tokens)
    result = parse_ABinaryOp().run(token_list)
    return result

def parse_ABinaryOp():
    return parse_AConstant() + Tag(Operator.Subtract) + parse_AConstant() ^ bin_op_func

def abin_op_func(parsed):
    ((x,y),z) = parsed
    return ABinaryOp(y,x,z)

def parse_AConstant():
    return Tag(Type.Integer) ^ AConstant

