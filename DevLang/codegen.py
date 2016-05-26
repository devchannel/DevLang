from .grammar import *

file = open("test.s", mode="w")

# TODO: Clean up the code and make it OOP


def codegen(ast):
    program = ast.value
    for function in program.functions:
        # TODO: Only codegen functions, and just work downwards from within it
        i = 0
        for item in function.body:
            if isinstance(item, DeclStmt):
                file.write("# We've found a Declaration of type " +
                           item.type + " with name " + item.name + "\n")
                write_decl(item.type, item.expr, i)
                i += 1


def load_immediate(register, value):
    file.write("li $" + register + ", " + value + "\n")


# All declarations are within functions
# so we need to do some messing with the stack.
def write_decl(type, expr, number):
    # TODO: right now we assume all types are 4 bytes
    # so we just ignore it. We must change this.
    file.write("addi $sp, $sp, -4\n")  # Move sp to make room for 4 bytes
    save_expr(expr)  # We've loaded t0 with the value of the decl
    file.write("sw $r" + str(number) + ", 0($t0)\n\n")


# Save the value of the expression into register $t0
def save_expr(expr):
    if isinstance(expr, AExpr):  # It's an expression
        if isinstance(expr, AInt) or isinstance(expr, AFloat):
            load_immediate("t0", expr.val)  # Just load it
        elif isinstance(expr, ABrackets) or isinstance(expr, ABinaryOp):
            load_immediate("t0", str(fold(expr)))  # Fold evals the expression


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
