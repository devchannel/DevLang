from .grammar import *

file = open("test.s", mode="w")

# TODO: Clean up the code and make it OOP


def codegen(ast):
    file.write(".text\n")
    program = ast.value
    for function in program.functions:
        gen_function(function)
    file.write("li $v0, 10\nsyscall\n")  # Signify the end of the program


def gen_function(function):
    file.write("\n.globl " + function.name + "\n")
    file.write(function.name + ":\n")  # Write the label
    i = 0
    for item in function.body:
        if isinstance(item, DeclStmt):
            file.write("# We've found a Declaration of type " +
                       item.type + " with name " + item.name + "\n")
            write_decl(item.type, item.expr, i)
            i += 1
    while(i > 0):
        pop_reg("t" + str(i))
        i -= 1


def pop_reg(reg):
    file.write("# Pushing register " + reg + " off of stack\n")
    file.write("lw $" + reg + ", 0($sp)\n")
    file.write("addi $sp, $sp, 4\n\n")


def load_immediate(register, value):
    file.write("li $" + register + ", " + value + "\n")


# All declarations are within functions
# so we need to do some messing with the stack.
def write_decl(type, expr, number):
    # TODO: right now we assume all types are 4 bytes
    # so we just ignore it. We must change this.
    file.write("addi $sp, $sp, -4\n")  # Move sp to make room for 4 bytes
    file.write("sw $t" + str(number) + ",0($sp)\n")
    save_expr(expr, "t" + str(number))  # Load reg with the value of the decl
    file.write("\n")  # Pretty Printing


# Save the value of the expression into register $t0
def save_expr(expr, register):
    if isinstance(expr, AExpr):  # It's an expression
        if isinstance(expr, AInt):
            load_immediate(register, expr.val)  # Just load it
        elif isinstance(expr, ABrackets) or isinstance(expr, ABinaryOp):
            load_immediate(register, str(fold(expr)))  # Fold expression


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
