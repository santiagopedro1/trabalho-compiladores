from lexico import build_lexer
from sintatica import parse
from sintatica.ast_graphviz import generate_dot_for_ast

from sys import argv, exit
from os import path

from traceback import print_exc


def tokenize_file(input_file, output_file, lexer):
    with open(input_file) as f:
        data = f.read()

    print("\n===== LEXICAL ANALYSIS =====")
    lexer.input(data)

    tokens_found = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        last_cr = data.rfind("\n", 0, tok.lexpos)
        column = tok.lexpos - last_cr if last_cr != -1 else tok.lexpos + 1
        token_info = (
            f"{tok.type:<10}: {tok.value:<50} line {tok.lineno:<2} column {column:<2}"
        )
        tokens_found.append((tok.type, tok.value, tok.lineno, column))

    with open(f"{output_file}.txt", "w") as out_file:
        for token in tokens_found:
            out_file.write(
                f"{token[0]:<10}: {token[1]:<50} line {token[2]:<2} column {token[3]:<2}\n"
            )

    print("TOKENS WRITTEN TO FILE " + f"{output_file}.txt")


def parse_file(input_file, output_file, lexer):
    with open(input_file) as f:
        data = f.read()

    print("\n===== PARSING =====")
    ast = parse(data, lexer)
    generate_dot_for_ast(ast, output_file)

    return ast


if __name__ == "__main__":
    if len(argv) < 4:
        print("Usage: python main.py [lexico|sintatico|all] <input_file> <output_file>")
        exit(1)

    action = argv[1].lower()
    input_file = argv[2]
    output_file = argv[3]

    try:
        lexer = build_lexer()
        if action == "lexico":
            tokenize_file(input_file, output_file, lexer)
        elif action == "sintatico":
            parse_file(input_file, output_file, lexer)
        elif action == "all":
            tokenize_file(input_file, output_file, lexer)
            parse_file(input_file, output_file, lexer)
        else:
            print("Unknown action. Use 'lexico', 'sintatico', or 'all'.")
    except Exception as e:
        print(f"Error: {e}")
        print_exc()
