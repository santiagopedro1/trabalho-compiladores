import ply.lex as lex

from .keywords import keywords

reserved = {k: k.upper() for k in keywords}

tokens = [
    # Literals
    "INTEGER",
    "FLOAT",
    "STRING",
    "CHAR",
    "BOOL",
    # Identifiers
    "ID",
    # Operators and Punctuation
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "EQ",
    "NEQ",
    "LT",
    "GT",
    "LE",
    "GE",
    "AND",
    "OR",
    "NOT",
    "ASSIGN",
    "LPAREN",
    "RPAREN",
    "COMMA",
    "RANGE",
    # Keywords
] + list(reserved.values())

t_TRUE = r"\btrue\b"
t_FALSE = r"\bfalse\b"

t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"

t_EQ = r"=="
t_NEQ = r"!="
t_LT = r"<"
t_GT = r">"
t_LE = r"<="
t_GE = r">="

t_AND = r"&&"
t_OR = r"\|\|"
t_NOT = r"!"
t_ASSIGN = r"="

t_LPAREN = r"\("
t_RPAREN = r"\)"

t_COMMA = r","
t_RANGE = r":"
t_IN = r"in"

t_END = r"end"

t_ignore = " \t"


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z0-9_!]*"
    t.type = reserved.get(t.value, "ID")
    return t


def t_FLOAT(t):
    r"(\d+\.\d*|\.\d+)([eE][-+]?\d+)?"
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_STRING(t):
    r"\"([^\\\"]|\\.)*\" "
    # Strip quotes
    t.value = t.value[1:-1]
    return t


def t_CHAR(t):
    r"\'([^\\\']|\\.)\'"
    # Strip quotes
    t.value = t.value[1:-1]
    return t


def t_BOOL(t):
    r"\b(true|false)\b"
    t.value = t.value.lower() == "true"
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def build_lexer():
    return lex.lex()
