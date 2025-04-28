import ply.lex as lex

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'KEYWORD',
    'ID',
    'TNAME',
    'TDECL',
    "ASSIGN",
    "STRING",
    "COMMA",
    "BIGGERTHAN",
    "SMALLERTHAN"
)

t_NUMBER  = r'\d+(.\d+)?'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ID      = r'[a-z_][a-zA-Z0-9_]*'
t_TNAME   = r'[A-Z][a-zA-Z0-9_]*'
t_TDECL   = r'::'
t_ASSIGN  = r'='
t_STRING  = r'"[^"]*"'
t_COMMA   = r','
t_BIGGERTHAN = r'>'
t_SMALLERTHAN = r'<'

def load_keywords():
    with open('keywords') as f:
        return f.read().splitlines()


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def generate_keyword_rule(keywords):
    return r'(' + '|'.join(keywords) + r')'

def build_lexer():
    kws = load_keywords()
    global t_KEYWORD
    t_KEYWORD = generate_keyword_rule(kws)
    return lex.lex()