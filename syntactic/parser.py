import ply.yacc as yacc
from lexer.lexer import tokens
from .ast_nodes import Node


precedence = (
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE", "MOD"),
    ("right", "UMINUS"),
)


def p_program(p):
    """program : statement_list
    | empty"""

    if p[1] is None:
        p[0] = Node("program", [Node("statement_list", [])])
    else:
        p[0] = Node("program", [p[1]])


def p_statement_list(p):
    """statement_list : statement_list statement
    | statement"""
    if len(p) == 3:

        if p[2]:
            p[1].children.append(p[2])
        p[0] = p[1]
    else:

        p[0] = Node("statement_list", [p[1]] if p[1] else [])


def p_statement(p):
    """statement : assignment_statement
    | if_statement
    | while_statement
    | function_def_statement
    | expression_statement"""

    p[0] = p[1]


def p_expression_statement(p):
    "expression_statement : expression"
    p[0] = Node("expression_statement", [p[1]])


def p_assignment_statement(p):
    """assignment_statement : ID ASSIGN expression
    | ID PLUS_ASSIGN expression
    | ID MINUS_ASSIGN expression
    | ID TIMES_ASSIGN expression
    | ID DIVIDE_ASSIGN expression"""
    p[0] = Node("assign", [Node("identifier", leaf=p[1]), p[3]], p[2])


def p_if_statement(p):
    """if_statement : IF expression statement_list else_if_clauses_opt else_clause_opt END"""
    children = [p[2], p[3]]
    if p[4]:
        children.extend(p[4])
    if p[5]:
        children.append(p[5])
    p[0] = Node("if_statement", children)


def p_else_if_clauses_opt(p):
    """else_if_clauses_opt : else_if_clauses
    | empty"""
    p[0] = p[1] if p[1] else []


def p_else_if_clauses(p):
    """else_if_clauses : else_if_clauses else_if_clause
    | else_if_clause"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_else_if_clause(p):
    "else_if_clause : ELSEIF expression statement_list"
    p[0] = Node("elseif", [p[2], p[3]])


def p_else_clause_opt(p):
    """else_clause_opt : else_clause
    | empty"""
    p[0] = p[1]


def p_else_clause(p):
    "else_clause : ELSE statement_list"
    p[0] = Node("else", [p[2]])


def p_while_statement(p):
    "while_statement : WHILE expression statement_list END"
    p[0] = Node("while_loop", [p[2], p[3]])


def p_function_def_statement(p):
    "function_def_statement : FUNCTION ID LPAREN param_list_opt RPAREN statement_list END"
    p[0] = Node("function_def", [Node("identifier", leaf=p[2]), p[4], p[6]])


def p_param_list_opt(p):
    """param_list_opt : param_list
    | empty"""
    p[0] = p[1] if p[1] else Node("param_list", [])


def p_param_list(p):
    """param_list : param_list COMMA ID
    | ID"""
    if len(p) == 4:
        p[1].children.append(Node("param", leaf=p[3]))
        p[0] = p[1]
    else:
        p[0] = Node("param_list", [Node("param", leaf=p[1])])


def p_expression_binop(p):
    """expression : expression PLUS expression
    | expression MINUS expression
    | expression TIMES expression
    | expression DIVIDE expression
    | expression MOD expression
    | expression EQ expression
    | expression NE expression
    | expression LT expression
    | expression LE expression
    | expression GT expression
    | expression GE expression"""
    p[0] = Node("bin_op", [p[1], p[3]], p[2])


def p_expression_uminus(p):
    "expression : MINUS expression %prec UMINUS"
    p[0] = Node("unary_op", [p[2]], "-")


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression_term(p):
    """expression : INTEGER
    | FLOAT
    | STRING
    | ID"""
    token = p.slice[1]
    if token.type == "INTEGER":
        p[0] = Node("integer", leaf=p[1])
    elif token.type == "FLOAT":
        p[0] = Node("float", leaf=p[1])
    elif token.type == "STRING":
        p[0] = Node("string", leaf=p[1])
    elif token.type == "ID":
        p[0] = Node("identifier", leaf=p[1])


def p_empty(p):
    "empty :"
    pass


def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (type: {p.type}) on line {p.lineno}")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()
