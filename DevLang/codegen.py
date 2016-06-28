from llvmlite import ir
from .grammar import *

# The Symbol Table represents every function
# It has all the variables and returns of each function
symbol_table = {}
module = None


def codegen(ast, filename, sym_table):
    global module
    global symbol_table
    symbol_table = sym_table

    module = ir.Module(filename)
    for function in ast.value.functions:
        codegen_function(function)
    file = open(filename, 'w')
    file.write(repr(module))


def codegen_function(function):
    func_ret = symbol_table[function.name]['ret_type']
    func_args = symbol_table[function.name]['args']

    func_type = ir.FunctionType(func_ret, func_args)

    # All of the above was just a setup for this, which only names the func
    func = ir.Function(module, func_type, name=function.name)

    # Now we go through and generate code for everything else

    codegen_body(function.body, func)


def codegen_body(body, function):
    for statement in body:
        pass

types = {
    'int32': ir.IntType(32),
    'int64': ir.IntType(64),
    'float': ir.DoubleType(),
    'char': ir.IntType(8),
    'string': ir.PointerType(ir.IntType(8)),
    'bool': ir.IntType(1)
}


def box(dev_type):
        return types[dev_type]
