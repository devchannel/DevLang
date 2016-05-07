
#  Program definition
class Program():
    pass

class ProgramFunctions(Program):
    def __init__(self, functions):
        self.functions = functions

# Functions
class Function():
    pass

class FTyped(Function):
    def __init__(self, name, type, params, body):
        self.name = name
        self.type = type
        self.params = params
        self.body = body

class FUntyped(Function):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

# Parameter declaration

class PrmDeclaration():
    pass

class PrmDecl(PrmDeclaration):
    def __init__(self, params):
        self.params = params

class PrmEmpty(PrmDeclaration):
    pass

# parameters

# If the parameter declaration is not empty
# then we must have at least one parameter
class Parameter():
    def __init__(self, type_name, var_name):
        self.type_name = type_name
        self.var_name = var_name

class FunctionCall():
    def __init__(self, name, args):
        self.name = name
        self.args = args

# sequence of expressions

class Arguments():
    def __init__(self, args):
        self.args = args

#statements

class Statement():
    pass

class DeclStmt(Statement):
    def __init__(self, type, name, expr):
        self.type = type
        self.name = name
        self.expr = expr

class AssignStmt(Statement):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class IfStmt(Statement):
    def __init__(self, cond, block1, block2):
        self.cond = cond
        self.b1 = b1
        self.b2 = b2

class ForStmt(Statement):
    def __init__(self, name, low, high, block):
        self.name = name
        self.low = low
        self.high = high
        self.block = block

class WhileStmt(Statement):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block

class CaseStmt(Statement):
    def __init__(self, expr, cases):
        self.expr = expr
        self.cases = cases

class ReturnStmt(Statement):
    def __init__(self, expr):
        self.expr = expr

# Different cases of a case stmt

class Cases():
    pass

class Case(Cases):
    def __init__(self, expr, block, cases):
        self.expr = expr
        self.block = block
        self.cases = cases

class CaseEmpty(Cases):
    pass

#  Expressions
class Expr():
    pass

#  Arithmetic Expressions
class AExpr(Expr):
    pass

class AConstant(AExpr):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return self.val


class AVar(AExpr):
    def __init__(self,name):
        self.name = name

class AFuncCall(AExpr):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class ABrackets(AExpr):
    def __init__(self,a_expr):
        self.a_expr = a_expr

    def __str__(self):
        return "(" + self.a_expr.__str__() + ")"

class ABinaryOp(AExpr):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return self.left.__str__() + " " + self.op.__str__() + " " + self.right.__str__()

#  Boolean Expressions

class BExpr(Expr):
    pass

class BConstant(BExpr):
    def __init__(self,val):
        self.val = val

class BVar (BExpr):
    def __init__(self,val):
        self.val = val

class BFuncCall(BExpr):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class BBrackets(BExpr):
    def __init__(self,b_expr):
        self.b_expr = b_expr

class BUnary(BExpr):
    def __init__(self,b_expr):
        self.b_expr = b_expr

class BBinaryOp(BExpr):

    def __init__(self, left, op, right):
        self.op = op
        self.left = left
        self.right = right
