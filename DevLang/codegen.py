from .grammar import *
from .mips import Mips

gen = Mips("test.s")
symbol_table = {}
loc_regs = []  # These will be modified and changed by each function


def codegen(ast):
    gen.write(".text\n")
    program = ast.value
    for function in program.functions:
        symbol_table[function.name] = {}  # Create the env for the function
        symbol_table[function.name]['return'] = None  # The return of the func
        gen_function(function)

    # Signify the end of the program
    gen.load_imm("v0", 10)
    gen.syscall()
    print(symbol_table)


def gen_function(function):
    gen.function(function.name)

    for item in function.body:
        gen_item(item, function.name)

    while len(loc_regs) > 0:
        pop_reg(*loc_regs.pop())
        gen.write("")  # Pretty print


def pop_reg(reg, isfloat):
    gen.comment("Popping register " + reg + " off of stack")
    gen.load_word(reg, 0, "sp", isfloat)
    gen.addi("sp", "sp", 4)


def gen_item(item, function):
    if isinstance(item, Statement):
        gen_stmt(item, function)
    elif isinstance(item, Expr):
        # An expression is useless. So don't do any codegen
        # All it does is affect return value
        symbol_table[function]['return'] = fold(item)


def gen_stmt(stmt, function):
    if isinstance(stmt, DeclStmt):
        symbol_table[function][stmt.name] = fold(stmt.expr)
        # We update the return value every single time
        symbol_table[function]['return'] = fold(stmt.expr)
        gen.comment("We've found a Declaration of type " +
                    stmt.type + " with name " + stmt.name)
        # print(type(stmt.expr))
        loc_regs.append(write_decl(stmt.type, stmt.expr, len(loc_regs)))


# All declarations are within functions
# so we need to do some messing with the stack.
def write_decl(type, expr, number):
    # TODO: right now we assume all types are 4 bytes
    # so we just ignore type. We must change this.
    reg = "t" + str(number)
    folded = fold(expr)
    isfloat = isinstance(folded, float)

    if isfloat:
        reg = "f" + str(number)

    gen.comment("Pushing register " + reg + " onto the stack")
    gen.addi("sp", "sp", -4)  # Move sp to make room for 4 bytes

    gen.save_word(reg, 0, "sp", isfloat)
    save_expr(folded, reg)  # Load reg with the value of the decl
    gen.write("")  # Pretty Printing
    return (reg, isfloat)  # For less of a headache later


# Save the value of the expression into register $t0
def save_expr(expr, register):
    if isinstance(expr, AExpr):  # It's an expression
        if isinstance(expr, AInt):
            gen.load_imm(register, expr.val)  # Just load it
        elif isinstance(expr, AFloat):
            gen.load_imm(register, expr.val, isfloat=True)
    elif isinstance(expr, float):
        gen.load_imm(register, expr)
    elif isinstance(expr, int):
        gen.load_imm(register, expr)


# Recursively evaluates the expression given to it.
def fold(expr):
    if isinstance(expr, AInt):
        return int(expr.val)
    if isinstance(expr, AFloat):
        return float(expr.val)
    if isinstance(expr, ABrackets):
        return fold(expr.a_expr)
    left = fold(expr.left)
    right = fold(expr.right)

    if expr.op == "+":
        return left + right
    elif expr.op == "-":
        return left - right
    elif expr.op == "*":
        return left * right
    elif expr.op == "/":
        return left / right
