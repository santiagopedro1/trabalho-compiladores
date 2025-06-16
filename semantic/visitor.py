# compiler/semantic/visitor.py
from .symbol_table import SymbolTable


class ASTVisitor:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.tac_code = []
        self.label_count = 0

    def new_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    def new_temp_location(self):
        """Creates a new temporary variable location in a register-like format."""
        offset = self.symbol_table.temp_var_count * 8  # Assuming 8 bytes per temp
        self.symbol_table.temp_var_count += 1
        return f"{offset:03d}(Rx)"

    def visit(self, node):
        if node is None:
            return None, None  # Return value/location and type
        method_name = f"visit_{node.type}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for child in node.children:
            self.visit(child)
        return None, None

    def visit_program(self, node):
        self.visit(node.children[0])
        return None, None

    def visit_statement_list(self, node):
        for stmt in node.children:
            self.visit(stmt)
        return None, None

    def visit_expression_statement(self, node):
        self.visit(node.children[0])
        return None, None

    def visit_assign(self, node):
        var_name = node.children[0].leaf
        expr_location, expr_type = self.visit(node.children[1])

        symbol = self.symbol_table.get_symbol(var_name)
        if not symbol:
            # First, add the symbol to the table.
            self.symbol_table.add_symbol(var_name, expr_type)
            # Then, retrieve the newly created symbol object.
            symbol = self.symbol_table.get_symbol(var_name)
        elif symbol["type"] != expr_type and expr_type is not None:
            print(
                f"Warning: Type mismatch for '{var_name}'. Assigning new type {expr_type}."
            )
            symbol["type"] = expr_type

        var_location = f"{symbol['offset']:03d}(SP)"

        op = node.leaf
        if op == "=":
            self.tac_code.append(f"{var_location} := {expr_location}")
        else:  # For +=, -=, etc.
            op_map = {"+=": "ADD", "-=": "SUB", "*=": "MUL", "/=": "DIV"}
            temp_reg = self.new_temp_location()
            self.tac_code.append(
                f"{temp_reg} := {var_location} {op_map[op]} {expr_location}"
            )
            self.tac_code.append(f"{var_location} := {temp_reg}")

        return None, None

    def visit_if_statement(self, node):
        end_label = self.new_label()
        clauses = node.children

        if_clause = (clauses[0], clauses[1])
        elseif_clauses = [c for c in clauses[2:] if c.type == "elseif"]
        else_clause = next((c for c in clauses[2:] if c.type == "else"), None)

        has_following_clauses = elseif_clauses or else_clause
        next_clause_label = self.new_label() if has_following_clauses else end_label

        cond_result, _ = self.visit(if_clause[0])
        self.tac_code.append(f"if_false {cond_result} goto {next_clause_label}")
        self.visit(if_clause[1])
        self.tac_code.append(f"goto {end_label}")

        if has_following_clauses:
            self.tac_code.append(f"{next_clause_label}:")

        for i, elseif in enumerate(elseif_clauses):
            is_last_elseif = i == len(elseif_clauses) - 1
            has_else = else_clause is not None
            next_clause_label = (
                self.new_label() if not (is_last_elseif and not has_else) else end_label
            )

            cond_result, _ = self.visit(elseif.children[0])
            self.tac_code.append(f"if_false {cond_result} goto {next_clause_label}")
            self.visit(elseif.children[1])
            self.tac_code.append(f"goto {end_label}")

            if next_clause_label != end_label:
                self.tac_code.append(f"{next_clause_label}:")

        if else_clause:
            self.visit(else_clause.children[0])

        self.tac_code.append(f"{end_label}:")
        return None, None

    def visit_while_loop(self, node):
        start_label = self.new_label()
        end_label = self.new_label()

        self.tac_code.append(f"{start_label}:")
        cond_result, _ = self.visit(node.children[0])
        self.tac_code.append(f"if_false {cond_result} goto {end_label}")
        self.visit(node.children[1])
        self.tac_code.append(f"goto {start_label}")
        self.tac_code.append(f"{end_label}:")
        return None, None

    def visit_function_def(self, node):
        func_name = node.children[0].leaf
        self.symbol_table.add_symbol(func_name, "Function")
        self.symbol_table.enter_scope(func_name)

        self.tac_code.append(f"func_begin {func_name}")

        for param in node.children[1].children:
            param_name = param.leaf
            self.symbol_table.add_symbol(param_name, "Any")
            self.tac_code.append(f"pop_param {param_name}")

        self.visit(node.children[2])  # Function body
        self.tac_code.append(f"func_end {func_name}")
        self.symbol_table.exit_scope()
        return None, None

    def visit_bin_op(self, node):
        op_map = {
            "+": "ADD",
            "-": "SUB",
            "*": "MUL",
            "/": "DIV",
            "%": "MOD",
            "==": "EQ",
            "!=": "NE",
            "<": "LT",
            "<=": "LE",
            ">": "GT",
            ">=": "GE",
        }
        op = op_map.get(node.leaf, node.leaf.upper())

        left_val, left_type = self.visit(node.children[0])
        right_val, right_type = self.visit(node.children[1])

        temp_location = self.new_temp_location()

        result_type = "Float" if "Float" in (left_type, right_type) else "Integer"

        self.tac_code.append(f"{temp_location} := {left_val} {op} {right_val}")
        return temp_location, result_type

    def visit_unary_op(self, node):
        operand_val, operand_type = self.visit(node.children[0])
        temp_location = self.new_temp_location()
        self.tac_code.append(f"{temp_location} := 0 SUB {operand_val}")
        return temp_location, operand_type

    def visit_integer(self, node):
        return node.leaf, "Integer"

    def visit_float(self, node):
        return node.leaf, "Float"

    def visit_string(self, node):
        return node.leaf, "String"

    def visit_identifier(self, node):
        symbol = self.symbol_table.get_symbol(node.leaf)
        if not symbol:
            print(f"Error: Variable '{node.leaf}' not defined.")
            return node.leaf, "Undefined"

        location = f"{symbol['offset']:03d}(SP)"
        return location, symbol["type"]
