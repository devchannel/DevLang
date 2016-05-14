from grammar import *

def type_check(ast):
    program = ast.value

    for function in program.functions:
        for item in function.body:
            #print(item)
            #print(type(item))
            if isinstance(item, DeclStmt):
                # We are now certain that this is a declaration
                #TODO: Use our Enums to make this simpler
                if item.type == 'int32' or item.type == 'int64' or item.type == 'int':
                    if not (isinstance(item.expr, AInt) or isinstance(item.expr, AFloat)):
                        #TODO: use the Error handler to handle this
                        raise Exception("This is not an Integer, " + str(item.expr))

