from llvmlite import ir
from .grammar import *

# The Symbol Table represents every function
# It has all the variables and returns of each function
symbol_table = {}
module = None


def codegen(ast, filename):
    global module
    module = ir.Module(filename)
    for function in ast.value.functions:
        symbol_table[function.name] = {'return': None, 'ref': function}
        codegen_function(function)


def codegen_function(function):
    try:  # It's typed
        func_ret = box(function.type)
    except AttributeError:  # It's untyped
        func_ret = deduce_type(function)

    func_args = function.params

    # Converts the function parameters to a tuple of LLVM types
    # Sort of functional black magic
    func_args = tuple(map(lambda x: box(x.type_name), func_args.params))

    func_type = ir.FunctionType(func_ret, func_args)

    # All of the above was just a setup for this, which only names the func
    func = ir.Function(module, func_type, name=function.name)

    # Now we go through and generate code for everything else

    codegen_body(function.body, func)


def codegen_body(body, function):
    for statement in body:
        pass


def deduce_type(f, returns=None):

    if returns is None:
        returns = [f]

    for statement in f.body:

        try:  # It's a normal statement
            statement_type = statement.type

        except AttributeError:  # It's a block, like an if or a while
            if isinstance(statement, ReturnStmt):
                return pybox(statement.expr)

            if isinstance(statement, AssignStmt):
                statement_type = pybox(statement.expr)

            elif isinstance(statement, AExpr):
                statement_type = deduce_aexpr(statement)

            # TODO: Cover for Case statements
            else:
                statement_type = deduce_block(statement.block)

            # In the case of if statements...
            # We assume that that the if and else block ret the same type
            # That is because our SA should check this

        if statement_type in returns:
            continue

        returns.append(statement_type)
        """
        elif statement.type is a function:
            deduce_type(statement.type, types)
        else:
            types.add(statement.type)
        """
    # Return the last return value given
    symbol_table[f.name]['return'] = returns[-1]
    print (returns[-1])
    return returns[-1]


def deduce_block(block):
    returns = []
    for statement in block:
        try:  # Declaration
            statement_type = box(statement.type)
        except AttributeError:
            try:  # Assignment
                statement_type = devbox(statement.expr)
            except AttributeError:  # Block
                statement_type = deduce_block(statement.block)
        returns.append(statement_type)
    return returns[-1]  # The last return


def deduce_aexpr(expr):
    # TODO: Function calls and variables expressions
    if isinstance(expr, AInt):
        return ir.IntType(64)
    elif isinstance(expr, AFloat):
        return ir.DoubleType()
    elif isinstance(expr, ABinaryOp):
        if isinstance(deduce_aexpr(expr.left), ir.DoubleType):
            return ir.DoubleType()
        elif isinstance(deduce_aexpr(expr.right), ir.DoubleType):
            return ir.DoubleType()
        return ir.IntType(64)
    elif isinstance(expr, ABrackets):
        return deduce_aexpr(expr.a_expr)


# TODO: The type checker should do this
def box(dev_type):
    if dev_type == "int32":
        return ir.IntType(32)
    if dev_type == "int64":
        return ir.IntType(64)
    if dev_type == "char":
        return ir.IntType(8)  # We have an 8 bit character set
    if dev_type == "string":
        # We need to specify the size if we use an array
        # So instead we use a pointer to a char
        return ir.PointerType(ir.IntType(8))  # Hooray for pointers!
    if dev_type == "bool":
        return ir.IntType(1)
    if dev_type == "float":
        return ir.DoubleType()


# The same thing as box, but it uses Python types
def pybox(dev_var):
    try:  # Int's are rep'd as strings
        dev_var = int(dev_var)
    except Exception:
        pass  # We might need to do something for bools later
    dev_type = type(dev_var)
    if dev_type == int:
        return ir.IntType(64)
    if dev_type == str and len(dev_var) == 1:
        return ir.IntType(8)  # We have an 8 bit character set
    if dev_type == str:
        # We need to specify the size if we use an array
        # So instead we use a pointer to a char
        return ir.PointerType(ir.IntType(8))  # Hooray for pointers!
    if dev_type == bool:
        return ir.IntType(1)
    if dev_type == float:
        return ir.DoubleType()


# Same as above, but with types from grammar.py
def devbox(dev_type):
    return pybox(dev_type.val)
