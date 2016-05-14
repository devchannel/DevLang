from combinators import *
from tokenList import *

# TODO: define parse_cases()

# Create a TokenList datastructure which is used by the 
# parser combinators for parsing.
# Calculate a parser that given a token list returns a result
# Run the parser and return the result
def parse(tokens, errorHandler):
    token_list = TokenList(tokens)
    result = parse_program().run(token_list)
    # result = test_parse().run(token_list)
    if not result:
        errorHandler.add("Parse", result.error, result.location)
    return result

# program is a collection of functions
def parse_program():
    return RepeatUntil(parse_function(), Tag(Special.EOF)) ^ process_program

def process_program(result_tuple):
    (list_function,_) = result_tuple
    return ProgramFunctions(list_function)

# There are typed and untyped functions
def parse_function():
    return (parse_typed_function() | parse_untyped_function()) * "Failed parsing function"

# |Type|Name param_decl -> code_block
def parse_typed_function():
    return (
        parse_type() + parse_func_name() +
        parse_param_decl() + parse_begin_code_sym() +
        parse_code_block() ^ process_typed_function
        )

def process_typed_function(result_tuple):
    (func_name, type_name, params, _, codeblock) = result_tuple
    (code, _) = codeblock
    return FTyped(func_name, type_name, params, code)

# Name param_decl -> code_block
def parse_untyped_function():
    return (
        parse_func_name() + parse_param_decl() +
        parse_begin_code_sym() + parse_code_block() ^
        process_untyped_function
        )

def process_untyped_function(result_tuple):
    (func_name, params, _, codeblock) = result_tuple
    (code, _) = codeblock
    return FUntyped(func_name, params, code)

# A function can either have parameters or it does not
def parse_param_decl():
    return (
            parse_begin_params_sym() +
            parse_params() ^ process_param_decl
        | 
            Default(PrmEmpty()) * "Failed parsing parameters"
        )

def process_param_decl(result_tulple):
    (_, params) = result_tulple
    return PrmDecl(params)

# We expect at least one parameter
# |type var
# Returns a collection of parameters
def parse_params():
    return (Repeat(parse_type() + parse_var() ^ process_param))# * "Failed parsing parameters"

def process_param(result_tulple):
    (type_name, var_name) = result_tulple
    return Parameter(type_name, var_name)

# Name arg1 arg2 arg3
def parse_func_call():
    return (parse_func_name() + parse_args() ^ process_func_call) * "Failed parsing function call"

def process_func_call(result_tuple):
    (func_name, list_args) = result_tulple
    return FunctionCall(func_name, list_args)

# Arguments is a collection of expressions
def parse_args():
    return (Repeat(Lazy(parse_expr)) ^ process_args) * "Failed parsing arguments"

def process_args(list_expr):
    return Arguments(list_expr)

# List of statements that ends with the keyword End
def parse_code_block():
    return RepeatUntil(Lazy(parse_stmt), parse_end_key())

def parse_stmt():
    return (parse_if_stmt()
            | parse_assign_stmt()
            | parse_return_stmt()# * "Failed parsing return statement"
            | parse_decl_stmt()# * "Failed parsing declaration statement"
            | parse_for_stmt()# * "Failed parsing for statement"
            | parse_case_stmt()
            | parse_while_stmt()# * "Failed parsing while statement"
           ) * "Failed parsing statement"

# Typed assignment. The var should not yet exist
# |Type Var| = expr
def parse_decl_stmt():
    return (
        parse_type() + parse_var() +
        parse_assign_sym() + parse_expr() ^ 
        process_decl_stmt # * "Failed parsing variable declaration"
        )

def process_decl_stmt(result_tuple):
    (type_name, var_name, _, expr) = result_tuple
    return DeclStmt(type_name, var_name, expr)

# Typeless assignment. The var should already exist
# Var = expr
def parse_assign_stmt():
    return (
        parse_var() + parse_assign_sym() +
        parse_expr() ^ process_assign_stmt # * "Failed parsing assignment"
           )

def process_assign_stmt(result_tuple):
    (var_name, _, expr) = result_tuple
    return AssignStmt(var_name, expr)

# If bexpr =>
#    code_block
# =>
#    code_block
def parse_if_stmt():
    return ( 
        parse_if_key() + parse_bexpr() + 
        parse_begin_code_sym() + parse_code_block() +
        parse_begin_code_sym() + parse_code_block() ^
        process_if_stmt 
        )

def process_if_stmt(result_tuple):
    (_, cond, _, block1, _, block2) = result_tuple
    (code1, _) = block1
    (code2, _) = block2
    return IfStmt(cond, code1, code2)

# Return expr
def parse_return_stmt():
    return (parse_return_key() + parse_expr() ^ process_return_stmt)# * "Failed parsing return statement"

def process_return_stmt(result_tuple):
    (_, expr) = result_tuple
    return ReturnStmt(expr)

# Case expr =>
#  cases

def parse_case_stmt():
    return (
        parse_case_key() + parse_expr() +
        parse_begin_code_sym() + parse_cases() ^
        process_case_stmt
    )

def process_case_stmt(result_tuple):
    (_, expr, _, cases) = result_tuple
    return CaseStmt(expr, cases)

# expr1 => code_block1
# expr2 => code_block2
def parse_cases():
    return (
        Repeat(
            parse_expr() + parse_begin_code_sym() +
            parse_code_block() ^ process_case
            )
        )

def process_case(result_tuple):
    (expr, sym, block) = result_tuple
    (code, _) = block
    return Case(expr, code)

# While expr => code_block
def parse_while_stmt():
    return (
        (parse_while_key() + parse_bexpr() +
        parse_begin_code_sym() + parse_code_block() ^
        process_while_stmt) * "Failed parsing while loop"
        )

def process_while_stmt(result_tuple):
    (_, cond, _, block) = result_tuple
    (code, _) = block
    return WhileStmt(cond, code)

# For Var in Num..Num => code_block
def parse_for_stmt():
    return (
        parse_for_key() + parse_var() +
        parse_in_key() + parse_constant_aexpr() +
        parse_range_sym() + parse_constant_aexpr() +
        parse_begin_code_sym() + parse_code_block() ^
        process_for_stmt # * "Failed parsing for loop"
        )

def process_for_stmt(result_tuple):
    (_, var_name, _, low, _, high, _, block) = result_tuple
    (code, _) = block
    return ForStmt(var_name, low, high, code)

# An expression can be an arithmic expression,
# boolean expression or a function call of which the type
# at parsing is unknown
def parse_expr():
    return (parse_aexpr() | parse_bexpr() | parse_func_call() | parse_string()) * "Failed parsing expression"

def parse_string():
    return Tag(Type.String) ^ String

def parse_term_aexpr():
    return (
          parse_constant_aexpr()
        | parse_var_aexpr()
        | parse_func_call_aexpr()
        | parse_brackets_aexpr()
        )


def parse_constant_aexpr():
    return (Tag(Type.Integer32) ^ AInt) | (Tag(Type.Float) ^ AFloat)# * "Failed parsing constant integer"

def parse_var_aexpr():
    return (parse_var() ^ AVar)# * "Failed parsing variable"

def parse_func_call_aexpr():
    return (parse_func_name() + parse_args() ^ process_func_call_aexpr)# * "Failed parsing function call"

def process_func_call_aexpr(result_tuple):
    (func_name, args) = result_tuple
    return AFuncCall(func_name, args)

def parse_brackets_aexpr():
    return (
          parse_constant_bexpr()
        | parse_var_bexpr()
        | parse_func_call_bexpr()
        )
            #* "Failed parsing boolean expression"

def process_brackets_aexpr(result_tuple):
    (_, aexpr, _) = result_tuple
    return ABrackets(aexpr)


def parse_aexpr():
    return parse_level3_aexpr()

def chain_aexpr(tuple_list):
    return chain(tuple_list, ABinaryOp)

def parse_level3_aexpr():
    return ChainL(parse_level2_aexpr(), parse_level3_ops()) ^ chain_aexpr

def parse_level3_ops():
    return Tag(Symbol.Add) | Tag(Symbol.Subtract)

def parse_level2_aexpr():
    return ChainL(parse_term_aexpr(), parse_level2_ops()) ^ chain_aexpr

def parse_level2_ops():
    return Tag(Symbol.Multiply) | Tag(Symbol.Divide)


def parse_term_bexpr():
    return (
        parse_constant_bexpr()
    |
        parse_aexpr() + parse_rel_op() + parse_aexpr() ^ process_rel_bexpr
    |
        parse_brackets_bexpr()
    |
        Tag(Symbol.Not) + Lazy(parse_bexpr) ^ process_not_bexpr
        )

def parse_constant_bexpr():
    return ((Tag(Symbol.TrueVal) | Tag(Symbol.FalseVal)) ^ BConstant) #* "Failed parsing boolean constant"

def parse_var_bexpr():
    return (parse_var() ^ BVar) #* "Failed parsing boolean variable"

def parse_func_call_bexpr():
    return (parse_func_name() + parse_args() ^ process_func_call_bexpr) #* "Failed parsing boolean function call"

def process_func_call_bexpr(result_tuple):
    (func_name, args) = result_tuple
    return BFuncCall(func_name, args)

def parse_brackets_bexpr():
    return (
        parse_open_bracket_sym() + Lazy(parse_bexpr) + parse_close_bracket_sym() ^
        process_brackets_bexpr
        )

def process_brackets_bexpr(result_tuple):
    (_, bexpr, _) = result_tuple
    return BBrackets(bexpr)

def process_not_bexpr(result_tuple):
    (_, bexpr) = result_tuple
    return BNot(bexpr)

def parse_bexpr():
    return parse_level3_bexpr()


def chain_and_bexpr(tuple_list):
    return chain(tuple_list, (lambda l, op, r: BAnd(l, r)))

def chain_or_bexpr(tuple_list):
    return chain(tuple_list, (lambda l, op, r: BOr(l, r)))

def parse_level3_bexpr():
    return ChainL(parse_level2_bexpr(), Tag(Symbol.Or)) ^ chain_or_bexpr

def parse_level2_bexpr():
    return ChainL(parse_term_bexpr(), Tag(Symbol.And)) ^ chain_and_bexpr

def parse_rel_op():
    return (
        Tag(Symbol.Lt) | Tag(Symbol.Lte) |
        Tag(Symbol.Gt) | Tag(Symbol.Gte) |
        Tag(Symbol.Eq) | Tag(Symbol.Neq)
        )

def process_rel_bexpr(result_tuple):
    (term, op, bexpr) = result_tuple
    return BRelOp(term, op, bexpr)


def chain(result_tuple, constructor):
    (term, tuples) = result_tuple
    if len(tuples) > 1:
        (op, expr) = tuples[0]
        chain1 = chain((constructor(term, op, expr), tuples[1:]), constructor)
        return chain1
    elif len(tuples) == 1:
        (op, expr) = tuples[0]
        return constructor(term, op, expr)
    else:
        return term


# Primitive parsing functions

def parse_func_name():
    return Tag(Special.Name)# * "Failed parsing function name"

def parse_var():
    return Tag(Special.Name)# * "Failed parsing variable"

def parse_type():
    return Tag(Special.TypeName)# * "Failed parsing type"

def parse_if_key():
    return Tag(Symbol.If)# * "Failed parsing if keyword"

def parse_end_key():
    return Tag(Symbol.End)# * "Failed parsing end keyword"

def parse_while_key():
    return Tag(Symbol.While)# * "Failed parsing while key"

def parse_for_key():
    return Tag(Symbol.For)# * "Failed parsing for key"

def parse_in_key():
    return Tag(Symbol.In)# * "Failed parsing in key"

def parse_case_key():
    return Tag(Symbol.Case)# * "Failed parsing case key"

def parse_return_key():
    return Tag(Symbol.Return)# * "Failed parsing return key"

def parse_begin_code_sym():
    return Tag(Symbol.FunctionMultiLine)# * "Failed parsing parameter declaration"

def parse_begin_params_sym():
    return Tag(Symbol.ArgumentList)# * "Failed parsing paramaters beginng"

def parse_end_line_sym():
    return Tag(Symbol.Delimiter)# * "Failed parsing end line symbol"

def parse_assign_sym():
    return Tag(Symbol.FunctionOneLine)# * "Failed parsing equal sign"

def parse_open_bracket_sym():
    return Tag(Symbol.OpenBracket)

def parse_close_bracket_sym():
    return Tag(Symbol.CloseBracket)

# parses .., but throws away one so that it counts as a single
# parsed value.
def parse_range_sym():
    return (Tag(Symbol.Dot) + Tag(Symbol.Dot) ^ (lambda two_tuple: two_tuple[0]))# * "Failed parsing range symbol"