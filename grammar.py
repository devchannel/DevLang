
# for nice output
def indentString(str):
    return "\n".join("    "+x for x in str.split("\n"))

#  Program definition
class Program():
    pass

class ProgramFunctions(Program):
    def __init__(self, functions):
        self.functions = functions

    def __str__(self):
        out = "\n\n".join(str(i) for i in self.functions)
        return out

    def __repr__(self):
        return "Program("+repr(self.functions)+")"

# Functions
class Function():
    pass

class FTyped(Function):
    def __init__(self, type, name, params, body):
        self.name = name
        self.type = type
        self.params = params
        self.body = body

    def __str__(self):
        out = ""
        out += "Typed Function: "+self.name+"("+self.type+") -> Parameters: "+str(self.params)+":\n"
        out += indentString("\n".join(str(i) for i in self.body))
        return out

    def __repr__(self):
        return "FTyped("+self.type+", "+self.name+", "+repr(self.params)+", "+repr(self.body)+")"


class FUntyped(Function):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __str__(self):
        out = ""
        out += "Untyped Function: "+self.name+" -> Parameters: "+str(self.params)+":\n"
        out += indentString("\n".join(str(i) for i in self.body))
        return out

    def __repr__(self):
        return "FUntyped("+self.name+", "+repr(self.params)+", "+repr(self.body)+")"


# Parameter declaration

class PrmDeclaration():
    pass

class PrmDecl(PrmDeclaration):
    def __init__(self, params):
        self.params = params

    def __str__(self):
        return ", ".join(str(i) for i in self.params)

    def __repr__(self):
        return "PrmDecl("+repr(self.params)+")"

class PrmEmpty(PrmDeclaration):
    def __repr__(self):
        return "PrmEmpty"

# parameters

# If the parameter declaration is not empty
# then we must have at least one parameter
class Parameter():
    def __init__(self, type_name, var_name):
        self.type_name = type_name
        self.var_name = var_name

    def __str__(self):
        return self.var_name+"("+self.type_name+")"

    def __repr__(self):
        return "Parameter("+self.type_name+", "+self.var_name+")"

class FunctionCall():
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        return name+str(args)

    def __repr__(self):
        return "FunctionCall("+self.name+", "+self.args+")"

# sequence of expressions

class Arguments():
    def __init__(self, args):
        self.args = args

    def __str__(self):
        return "("+", ".join(str(i) for i in self.args)+")"

    def __repr__(self):
        return "Arguments("+repr(self.args)+")"

#statements

class Statement():
    pass

class DeclStmt(Statement):
    def __init__(self, t, name, expr):
        self.type = t
        self.name = name
        self.expr = expr

    def __str__(self):
        return "Declare "+self.type+"("+self.type+") = "+str(self.expr)

    def __repr__(self):
        return "DeclStmt("+self.type+", "+self.name+", "+repr(self.expr)+")"

class AssignStmt(Statement):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def __str__(self):
        return "Assign "+self.name+" = "+str(self.expr)

    def __repr__(self):
        return "AssignStmt("+self.name+", "+repr(self.expr)+")"

# What are block 1 and 2? I will assume Else
class IfStmt(Statement):
    def __init__(self, cond, block1, block2):
        self.cond = cond
        self.b1 = b1
        self.b2 = b2

    def __str__(self):
        out = "If "+str(self.cond)+" then\n"
        out += indentString("\n".join(str(i) for i in self.b1))+"\n"
        out += "Else\n"
        out += indentString("\n".join(str(i) for i in self.b2))
        return out

    def __repr__(self):
        return "IfStmt("+repr(self.cond)+", "+repr(self.b1)+", "+repr(self.b2)+")"

class ForStmt(Statement):
    def __init__(self, name, low, high, block):
        self.name = name
        self.low = low
        self.high = high
        self.block = block

    def __str__(self):
        out = "For "+str(self.name)+" in "+str(low)+" to "+str(high)+" do\n"
        out += indentString("\n".join(str(i) for i in self.block))
        return out

    def __repr__(self):
        return "ForStmt("+self.name+", "+repr(self.low)+", "+repr(self.high)+", "+repr(self.block)+")"

class WhileStmt(Statement):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block

    def __str__(self):
        out = "While "+str(self.cond)+" do\n"
        out += indentString("\n".join(str(i) for i in self.block))
        return out

    def __repr__(self):
        return "WhileStmt("+repr(self.cond)+", "+repr(self.block)+")"

class CaseStmt(Statement):
    def __init__(self, expr, cases):
        self.expr = expr
        self.cases = cases

    def __str__(self):
        out = "Case Statement "+str(self.expr)+"\n"
        out += indentString(str(self.cases))
        return out

    def __repr__(self):
        return "CaseStmt("+repr(self.expr)+", "+repr(self.cases)+")"

class ReturnStmt(Statement):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return "Return "+self.expr

    def __repr__(self):
        return "ReturnStmt("+repr(self.expr)+")"

# Different cases of a case stmt

class Cases():
    pass

class Case(Cases):
    def __init__(self, expr, block, cases):
        self.expr = expr
        self.block = block
        self.cases = cases

    def __str__(self):
        out =  "Case "+str(self.expr)+":\n"
        out += indentString(str(self.block))+"\n"
        out += str(self.cases)
        return out

    def __repr__(self):
        return "Case("+repr(self.expr)+", "+repr(self.block)+", "+repr(self.cases)+")"

class CaseEmpty(Cases):
    def __repr__(self):
        return "CaseEmpty"

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
        return str(self.val)

    def __repr__(self):
        return "AConstant("+repr(self.val)+")"


class AVar(AExpr):
    def __init__(self,name):
        self.name = name

    def __str__(self):
        return "AVar["+self.name+"]"

    def __repr__(self):
        return "AVar("+self.name+")"

class AFuncCall(AExpr):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        return "AFuncCall["+self.name+"("+ ", ".join(i for i in self.args) +")]"

    def __repr__(self):
        return "AFuncCall("+self.name+", "+repr(self.args)+")"


class ABrackets(AExpr):
    def __init__(self,a_expr):
        self.a_expr = a_expr

    def __str__(self):
        return "("+str(self.a_expr)+")"

    def __repr__(self):
        return "ABrackets("+repr(self.a_expr)+")"

class ABinaryOp(AExpr):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return str(self.left)+" "+str(self.op)+" "+str(self.right)

    def __repr__(self):
        return "ABinaryOp("+repr(self.left)+", "+repr(self.op)+", "+repr(self.right)+")"

#  Boolean Expressions

class BExpr(Expr):
    pass

class BConstant(BExpr):
    def __init__(self,val):
        self.val = val

    def __str__(self):
        return "BConstant["+str(self.val)+"]"

    def __repr__(self):
        return "BConstant("+repr(self.val)+")"

class BVar(BExpr):
    def __init__(self,val):
        self.name = name

    def __str__(self):
        return "BVar["+str(self.val)+"]"

    def __repr__(self):
        return "BVar("+self.name+")"

class BFuncCall(BExpr):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        return "BFuncCall["+self.name+"("+ ", ".join(i for i in self.args) +")]"

    def __repr__(self):
        return "BFuncCall("+self.name+", "+repr(self.args)+")"

class BBrackets(BExpr):
    def __init__(self,b_expr):
        self.b_expr = b_expr

    def __str__(self):
        return "("+str(self.b_expr)+")"

    def __repr__(self):
        return "BBrackets("+repr(self.b_expr)+")"

class BAnd(BExpr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self): 
        return str(self.left) + " " + "&&" + " " + str(self.right)

    def __repr__(self):
        return "BAnd(" + repr(self.left) + ", " + repr(self.right) + ")"

class BOr(BExpr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self): 
        return str(self.left) + " " + "||" + " " + str(self.right)

    def __repr__(self):
        return "BOr(" + repr(self.left) + ", " + repr(self.right) + ")"

class BNot(BExpr):
    def __init__(self, b_expr):
        self.b_expr = b_expr

    def __str__(self): 
        return "!" + str(self.b_expr)

    def __repr__(self):
        return "BNot(" + repr(self.b_expr) + ")"

class BRelOp(BExpr):
    def __init__(self, left, op, right):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.left)+" "+str(self.op)+" "+str(self.right)

    def __repr__(self):
        return "BRelOp("+repr(self.left)+", "+repr(self.op)+", "+repr(self.right)+")"