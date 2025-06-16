import ply.lex as lex

reserved = {
    "if": "IF",
    "elseif": "ELSEIF",
    "else": "ELSE",
    "while": "WHILE",
    "function": "FUNCTION",
    "end": "END",
    "return": "RETURN",
}

tokens = [
    "ID",
    "INTEGER",
    "FLOAT",
    "STRING",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MOD",
    "ASSIGN",
    "PLUS_ASSIGN",
    "MINUS_ASSIGN",
    "TIMES_ASSIGN",
    "DIVIDE_ASSIGN",
    "EQ",
    "NE",
    "LT",
    "LE",
    "GT",
    "GE",
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
    "COMMA",
    "SEMICOLON",
    "NEWLINE",
] + list(reserved.values())

t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_MOD = r"%"
t_ASSIGN = r"="
t_PLUS_ASSIGN = r"\+="
t_MINUS_ASSIGN = r"-="
t_TIMES_ASSIGN = r"\*="
t_DIVIDE_ASSIGN = r"\/="
t_EQ = r"=="
t_NE = r"!="
t_LT = r"<"
t_LE = r"<="
t_GT = r">"
t_GE = r">="
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_COMMA = r","
t_SEMICOLON = r";"


def t_FLOAT(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_STRING(t):
    r"\"([^\\\n]|(\\.))*?\" "
    t.value = str(t.value)
    return t


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, "ID")
    return t


def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    pass


t_ignore = " \t"


def t_comment(t):
    r"\#.*"
    pass


def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()
