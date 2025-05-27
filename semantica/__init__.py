from semantica.symbol_table import proccess_node, SymbolTable

from semantica.tac import (
    process_node,
    format_operand,
    tac_raw_instructions,
    next_program_var_offset,
    next_temp_var_offset,
)


def generate_symbol_table_from_ast(ast):
    symbol_table = SymbolTable()
    proccess_node(ast, symbol_table)
    return symbol_table


def generate_tac(ast):
    process_node(ast)

    output_lines = [
        str(next_program_var_offset),
        str(next_temp_var_offset),
    ]

    for i, instr in enumerate(tac_raw_instructions):
        dest = format_operand(instr["dest"])
        src1 = format_operand(instr["src1"])

        if instr["type"] == "BINARY":
            src2 = format_operand(instr["src2"])
            line = f"{i:03d}:   {dest} := {src1} {instr['op']} {src2}"
        elif instr["type"] == "ASSIGN":
            line = f"{i:03d}:   {dest} := {src1}"
        else:
            raise ValueError(f"Unknown instruction type: {instr['type']}")

        output_lines.append(line)

    return "\n".join(output_lines)
