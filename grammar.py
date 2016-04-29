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

class ABrackets(AExpr):
    def __init__(self,a_expr):
        self.a_expr = a_expr

    def __str__(self):
        return "(" + self.a_expr.__str__() + ")"

class ABinaryOp(AExpr):
    def __init__(self,op,left,right):
        self.op = op
        self.left = left
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

class BBrackets(BExpr):
    def __init__(self,b_expr):
        self.b_expr = b_expr

class BUnary(BExpr):
    def __init__(self,b_expr):
        self.b_expr = b_expr

class BBinaryOp(BExpr):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
