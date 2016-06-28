from .grammar import *
from llvmlite import ir

types = {
    'int32': ir.IntType(32),
    'int64': ir.IntType(64),
    'float': ir.DoubleType(),
    'char': ir.IntType(8),
    'string': ir.PointerType(ir.IntType(8)),
    'bool': ir.IntType(1)
}


class Analyzer:
    """ Analyzer
    Takes an AST and validates it. Then fills out information for the codegen
    """
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = {}

    # Returns a symbol_table
    def analyze(self):
        program = self.ast.value

        for function in program.functions:
            self.symbol_table[function.name] = {
                # The first is the type of the return
                # The second is a reference to the actual function type
                # The vars are a dict of names and types, including params
                # Args is a tuple of types for the args
                'ret_type': None, 'ref': function, 'vars': {}, 'args': ()
            }
            func_sym = self.symbol_table[function.name]

            try:  # It has parameters
                parameters = function.params.params
            except AttributeError:  # No parameters
                parameters = []

            for param in parameters:
                func_sym['vars'][param.var_name] = self.box(param.type_name)

            # Some black magic that fills the args tuple
            func_sym['args'] = tuple(map(lambda x: self.box(x.type_name), parameters))

            self.analyze_function(function)

    def analyze_function(self, func):
        try:  # It's typed
            self.symbol_table[func.name]['ret_type'] = self.pybox(statement.expr)
        except AttributeError:  # It's untyped
            self.symbol_table[func.name]['ret_type'] = deduce_type(func)
        ret_value = self.symbol_table[func.name]['ret_type']

    def deduce_type(self, f, returns=None):
        if returns is None:
            returns = [f]

        for statement in f.body:
            num = 0  # Used to maintain the current index
            try:  # It's a normal statement
                statement_type = statement.type

            except AttributeError:  # It's a block, like an if or a while

                if num == len(f.body):  # This is the last statement
                    if isinstace(statement, IfStmt):
                        # If the if and else are different types
                        # Then we error
                        if_ret = deduce_block(statement.block)
                        else_ret = deduce_block(statement.els.block)
                        if type(if_ret) != type(else_ret):
                            raise Exception("If and Else return different types") 

                elif isinstance(statement, ReturnStmt):
                    return self.pybox(statement.expr)

                elif isinstance(statement, AssignStmt):
                    statement_type = self.pybox(statement.expr)

                elif isinstance(statement, AExpr):
                    statement_type = self.deduce_aexpr(statement)

                # TODO: Cover for Case statements
                else:
                    statement_type = self.deduce_block(statement.block)

                num += 1
            if statement_type in returns:
                continue

            returns.append(statement_type)

        # Return the last return value given
        return returns[-1]

    def deduce_block(self, block):
        returns = []
        for statement in block:
            try:  # Declaration
                statement_type = self.box(statement.type)
            except AttributeError:
                try:  # Assignment
                    statement_type = self.devbox(statement.expr)
                except AttributeError:  # Block
                    statement_type = self.deduce_block(statement.block)
            returns.append(statement_type)
        return returns[-1]  # The last return

    def deduce_aexpr(self, expr):
        # TODO: Function calls and variables expressions
        if isinstance(expr, AInt):
            return types['int64']
        elif isinstance(expr, AFloat):
            return types['float']
        elif isinstance(expr, ABinaryOp):
            if isinstance(self.deduce_aexpr(expr.left), ir.DoubleType):
                return types['float']
            elif isinstance(self.deduce_aexpr(expr.right), ir.DoubleType):
                return types['float']
            return types['int64']
        elif isinstance(expr, ABrackets):
            return self.deduce_aexpr(expr.a_expr)

    # TODO: The type checker should do this
    def box(self, dev_type):
        return types[dev_type]

    # The same thing as box, but it uses Python types
    def pybox(self, dev_var):
        try:  # Int's are rep'd as strings
            dev_var = int(dev_var)
        except Exception:
            pass  # We might need to do something for bools later
        dev_type = type(dev_var)
        if dev_type == int:
            return types['int64']
        if dev_type == str and len(dev_var) == 1:
            return types['char']
        if dev_type == str:
            return types['string']
        if dev_type == bool:
            return types['bool']
        if dev_type == float:
            return types['float']

    # Same as above, but with types from grammar.py
    def devbox(self, dev_type):
        return self.pybox(dev_type.val)
