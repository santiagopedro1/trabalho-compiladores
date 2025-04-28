from lex import build_lexer

import sys

def tokenize_file(filename):
    lexer = build_lexer()

    with open(filename) as f:
        data = f.read()

    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break 
        
        last_cr = data.rfind('\n', 0, tok.lexpos)
        column = tok.lexpos - last_cr if last_cr != -1 else tok.lexpos + 1
        
        print(f'{tok.type:<10}: {tok.value:<50} line {tok.lineno:<2} column {column:<2}')
    
    return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python main.py <filename>')
        sys.exit(1)
    
    tokenize_file(sys.argv[1])