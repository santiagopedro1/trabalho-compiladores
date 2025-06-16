import sys
import os

# Adjust path to import from subdirectories
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lexer.lexer import lexer
from syntactic.parser import parser
from semantic.visitor import ASTVisitor
from utils.dot_generator import generate_dot

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_file> <output_file_prefix>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_prefix = sys.argv[2]

    try:
        with open(input_file_path, "r") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file_path}' not found.")
        sys.exit(1)

    lexer.input(code)
    tokens_output_path = f"{output_prefix}_tokens.txt"
    with open(tokens_output_path, "w") as f:
        # Create a clone of the lexer for token output, as it's an iterator
        lexer_clone = lexer.clone()
        while True:
            tok = lexer_clone.token()
            if not tok:
                break
            # Calculate column
            last_cr = code.rfind("\n", 0, tok.lexpos)
            if last_cr < 0:
                last_cr = 0
            col = tok.lexpos - last_cr
            f.write(
                f"{tok.type:<10}: {tok.value:<20} line {tok.lineno:<5} column {col}\n"
            )
    print(f"Tokens saved to {tokens_output_path}")

    ast = parser.parse(code, lexer=lexer)

    if ast:

        dot_output_path = f"{output_prefix}.dot"
        with open(dot_output_path, "w") as f:
            generate_dot(ast, f)
        print(f"AST .dot file saved to {dot_output_path}")

        visitor = ASTVisitor()
        visitor.visit(ast)

        symbol_table_output_path = f"{output_prefix}_symbol_table.txt"
        with open(symbol_table_output_path, "w") as f:
            f.write(visitor.symbol_table.to_string())
        print(f"Symbol table saved to {symbol_table_output_path}")

        tac_output_path = f"{output_prefix}.tac"
        with open(tac_output_path, "w") as f:
            f.write(f"{visitor.symbol_table.total_var_size}\n")
            f.write(
                f"{visitor.symbol_table.temp_var_count * 8}\n"
            )  # Assuming 8 bytes per temp
            for i, line in enumerate(visitor.tac_code):
                f.write(f"{i:03d}: {line}\n")
        print(f"TAC code saved to {tac_output_path}")
    else:
        print("Parsing failed. No output files generated.")
