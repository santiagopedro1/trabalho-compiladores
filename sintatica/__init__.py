import ply.yacc as yacc
from lexico import tokens, build_lexer
from .ast_nodes import *

precedence = (
    ("right", "ASSIGN"),
    ("left", "OR"),
    ("left", "AND"),
    ("nonassoc", "EQ", "NEQ", "LT", "GT", "LE", "GE"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
    ("right", "NOT"),
)


# Grammar rules
def p_program(p):
    "program : statement_list"
    p[0] = Program(p[1])


def p_statement_list(p):
    """statement_list : statement_list statement
    | statement"""
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]


def p_statement(p):
    """statement : expression
    | if_statement
    | while_statement
    | for_statement
    | function_def
    | return_statement"""
    p[0] = p[1]


def p_block(p):
    """block : statement_list END
    | statement"""
    if len(p) == 4:
        p[0] = Block(p[2])
    elif len(p) == 3:
        p[0] = Block(p[1])
    else:
        p[0] = Block([p[1]])


def p_if_statement(p):
    """if_statement : IF expression block
    | IF expression block ELSE block"""
    p[0] = IfStatement(p[2], p[3], p[5] if len(p) == 6 else None)


def p_while_statement(p):
    """while_statement : WHILE expression block"""
    p[0] = WhileLoop(p[2], p[3])


def p_for_statement(p):
    """for_statement : FOR ID IN range_statement block"""
    p[0] = ForLoop(Identifier(p[2]), p[4], p[5])


def p_range_statement(p):
    """range_statement : expression RANGE expression"""
    p[0] = RangeOp(p[1], p[3])


def p_function_def(p):
    """function_def : FUNCTION ID LPAREN param_list RPAREN block
    | FUNCTION ID LPAREN param_list RPAREN statement_list END"""
    body = p[6] if len(p) == 7 else Block(p[6])
    p[0] = FunctionDef(p[2], p[4], body)


def p_return_statement(p):
    "return_statement : RETURN expression"
    p[0] = ReturnStatement(p[2])


def p_param_list(p):
    """param_list : non_empty_param_list
    | empty"""
    p[0] = p[1]


def p_non_empty_param_list(p):
    """non_empty_param_list : non_empty_param_list COMMA ID
    | ID"""
    p[0] = p[1] + [Identifier(p[3])] if len(p) == 4 else [Identifier(p[1])]


def p_arg_list(p):
    """arg_list : non_empty_arg_list
    | empty"""
    p[0] = p[1]


def p_non_empty_arg_list(p):
    """non_empty_arg_list : non_empty_arg_list COMMA expression
    | expression"""
    p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]


def p_expression_binary(p):
    """expression : expression PLUS expression
    | expression MINUS expression
    | expression TIMES expression
    | expression DIVIDE expression
    | expression AND expression
    | expression OR expression
    | expression EQ expression
    | expression NEQ expression
    | expression LT expression
    | expression GT expression
    | expression LE expression
    | expression GE expression"""
    p[0] = BinaryOp(p[1], p[2], p[3])


def p_expression_unary(p):
    """expression : NOT expression"""
    p[0] = UnaryOp(p[1], p[2])


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression_assignment(p):
    "expression : ID ASSIGN expression"
    p[0] = Assignment(Identifier(p[1]), p[3])


def p_expression_function_call(p):
    "expression : ID LPAREN arg_list RPAREN"
    p[0] = FunctionCall(p[1], p[3])


def p_expression_literal(p):
    """expression : INTEGER
    | FLOAT
    | STRING
    | CHAR
    | BOOL
    | TRUE
    | FALSE"""
    if isinstance(p[1], int):
        p[0] = Literal(p[1], "INTEGER")
    elif isinstance(p[1], float):
        p[0] = Literal(p[1], "FLOAT")
    elif isinstance(p[1], str) and p.slice[1].type == "STRING":
        p[0] = Literal(p[1], "STRING")
    elif isinstance(p[1], str) and p.slice[1].type == "CHAR":
        p[0] = Literal(p[1], "CHAR")
    elif p[1] in ("true", "false"):
        p[0] = Literal(p[1], "BOOL")


def p_expression_id(p):
    "expression : ID"
    p[0] = Identifier(p[1])


def p_empty(p):
    "empty :"
    p[0] = []


def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', line {p.lineno}, {p.type}")
    else:
        print("Syntax error at EOF")
    import sys

    sys.exit(1)


def build_parser(debug=False):
    return yacc.yacc(debug=debug)


def parse(source_code, lexer, debug=False):
    parser = build_parser(debug=debug)
    return parser.parse(source_code, lexer=lexer)
