from .grammar import *
from .mips import Mips

gen = Mips("test.s")


def codegen(ast):
    gen.write(".text\n")
    program = ast.value
    for function in program.functions:
        gen_function(function)

    # Signify the end of the program
    gen.load_imm("v0", 10)
    gen.syscall()


def gen_function(function):
    gen.function(function.name)
    i = 0
    for item in function.body:
        if isinstance(item, DeclStmt):
            gen.comment("We've found a Declaration of type " +
                        item.type + " with name " + item.name)
            write_decl(item.type, item.expr, i)
            i += 1
    while(i > 0):
        i -= 1
        pop_reg("t" + str(i))


def pop_reg(reg):
    gen.comment("Popping register " + reg + " off of stack")
    gen.load_word(reg, 0, "sp")
    gen.addi("sp", "sp", 4)


# All declarations are within functions
# so we need to do some messing with the stack.
def write_decl(type, expr, number):
    # TODO: right now we assume all types are 4 bytes
    # so we just ignore it. We must change this.
    gen.comment("Pushing register $t" + str(number) + " onto the stack")
    gen.addi("sp", "sp", -4)  # Move sp to make room for 4 bytes
    gen.save_word("t" + str(number), 0, "sp")
    save_expr(expr, "t" + str(number))  # Load reg with the value of the decl
    gen.write("")  # Pretty Printing


# Save the value of the expression into register $t0
def save_expr(expr, register):
    if isinstance(expr, AExpr):  # It's an expression
        if isinstance(expr, AInt):
            gen.load_imm(register, expr.val)  # Just load it
        elif isinstance(expr, ABrackets) or isinstance(expr, ABinaryOp):
            gen.load_imm(register, str(fold(expr)))  # Fold expression


# Recursively evaluates the expression given to it.
def fold(expr):
    if isinstance(expr, AInt):
        return int(expr.val)
    if isinstance(expr, AFloat):
        return float(expr.val)
    if isinstance(expr, ABrackets):
        fold(expr.a_expr)
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
