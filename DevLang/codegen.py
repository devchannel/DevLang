from llvmlite import ir

# The Symbol Table represents every function
# It has all the variables and returns of each function
symbol_table = {}
module = None


def codegen(ast, filename):
    global module
    module = ir.Module(filename)
    for function in ast.value.functions:
        symbol_table[function.name] = {'return': None}
        codegen_function(function)


def codegen_function(function):
    try:  # It's typed
        func_ret = box(function.type)
    except AttributeError:  # It's untyped
        func_ret = infer_type(function)

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

def infer_type(function):
    # TODO: Actually implement this
    return ir.IntType(32)


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


