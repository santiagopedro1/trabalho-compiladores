import collections
from sintatica.ast_nodes import *

TYPE_SIZES = {
    "INTEGER": 4,
    "FLOAT": 8,
}

# Global state
tac_raw_instructions = []
program_variables = collections.OrderedDict()
temp_variables = collections.OrderedDict()

next_program_var_offset = 0
next_temp_var_offset = 0
temp_counter = 0


def get_temp_var(result_type_name_str):
    global temp_counter, next_temp_var_offset, temp_variables

    temp_name = f"t{temp_counter}"
    temp_counter += 1

    size = TYPE_SIZES.get(result_type_name_str)
    if size is None:
        raise ValueError(
            f"Unknown type '{result_type_name_str}' for temp var {temp_name}"
        )

    if temp_name not in temp_variables:
        temp_variables[temp_name] = {
            "offset": next_temp_var_offset,
            "size": size,
            "type_name": result_type_name_str,
        }
        next_temp_var_offset += size

    return temp_name


def process_node(node):
    global next_program_var_offset

    if node is None:
        return None, None

    node_type = node.__class__.__name__

    if node_type == "BinaryOp":
        left_repr, left_type = process_node(node.left)
        right_repr, right_type = process_node(node.right)

        if left_type is None or right_type is None:
            raise TypeError(f"BinaryOp operands have indeterminate types.")

        result_type = "FLOAT" if "FLOAT" in (left_type, right_type) else "INTEGER"
        op_map = {
            "+": ("ADD", "FADD"),
            "-": ("SUB", "FSUB"),
            "*": ("MUL", "FMUL"),
            "/": ("DIV", "FDIV"),
        }

        int_op, float_op = op_map.get(node.op, (None, None))
        if not int_op:
            raise ValueError(f"Unsupported binary operator: {node.op}")
        op = float_op if result_type == "FLOAT" else int_op

        result_var = get_temp_var(result_type)
        tac_raw_instructions.append(
            {
                "type": "BINARY",
                "op": op,
                "dest": result_var,
                "src1": left_repr,
                "src2": right_repr,
            }
        )
        return result_var, result_type

    elif node_type == "Literal":
        if node.type_name not in TYPE_SIZES:
            raise ValueError(f"Unknown literal type: {node.type_name}")
        return node.value, node.type_name

    elif node_type == "Identifier":
        if node.name not in program_variables:
            raise NameError(f"Undeclared variable: {node.name}")
        return node.name, program_variables[node.name]["type_name"]

    elif node_type == "Assignment":
        if not isinstance(node.id, Identifier):
            raise TypeError("LHS of assignment must be an Identifier")

        target = node.id.name
        val_repr, val_type = process_node(node.expr)

        size = TYPE_SIZES[val_type]
        if target not in program_variables:
            program_variables[target] = {
                "offset": next_program_var_offset,
                "size": size,
                "type_name": val_type,
            }
            next_program_var_offset += size
        else:
            if program_variables[target]["size"] != size:
                print(
                    f"Warning: reassignment of variable '{target}' with different size"
                )
            program_variables[target]["type_name"] = val_type

        tac_raw_instructions.append(
            {"type": "ASSIGN", "dest": target, "src1": val_repr}
        )
        return target, val_type

    elif node_type == "Program":
        for stmt in getattr(node, "statements", []):
            process_node(stmt)
        return None, None

    return None, None


def format_operand(operand):
    if isinstance(operand, str):
        if operand in program_variables:
            return f"{program_variables[operand]['offset']:03d}(SP)"
        elif operand in temp_variables:
            return f"{temp_variables[operand]['offset']:03d}(Rx)"
        else:
            raise ValueError(f"Unknown operand: {operand}")
    elif isinstance(operand, (int, float)):
        return str(operand)
    else:
        raise TypeError(f"Unsupported operand type: {type(operand)}")
