from .grammar import *

def type_check(ast):
    program = ast.value

    for function in program.functions:
        for item in function.body:
            #print(item)
            #print(type(item))
            if isinstance(item, Statement):
                # We are now certain that this is a declaration
                stmt = type(item)
                if stmt in checks:
                    checks[stmt](item)

def decl_type_check(stmt):
    if stmt.type in ['int32', 'int64', 'int']:
        if not isinstance(stmt.expr, AExpr):
            #TODO: Use the Error Handler to properly handle this
            raise Exception(str(stmt.expr) + ", Is not an Integer Expression!")  

def if_type_check(stmt):
    if not isinstance(stmt.cond, BExpr):
        #TODO: Use the Error Handler to properly handle this
        raise Exception(str(stmt.cond) + ", Is not a Boolean Expression!")

checks = {
    DeclStmt    :   decl_type_check,
    IfStmt      :   if_type_check  
}