from sintatica.ast_nodes import *


class SymbolEntry:
    def __init__(self, name, var_type, size, offset):
        self.name = name
        self.var_type = var_type
        self.size = size
        self.offset = offset


class SymbolTable:
    TYPE_SIZES = {"INTEGER": 4, "FLOAT": 8}

    def __init__(self):
        self.table = {}
        self.offset = 0

    def insert(self, name, var_type):
        if name in self.table:
            return
        size = self.TYPE_SIZES.get(var_type, 0)
        entry = SymbolEntry(name, var_type, size, self.offset)
        self.table[name] = entry
        self.offset += size

    def lookup(self, name):
        if name not in self.table:
            print(f"UNDEFINED SYMBOL. A variavel {name} nao foi declarada.")
            return -21
        return self.table[name]

    def print_table(self):
        return "\n".join(
            f"Name: {entry.name}, Type: {entry.var_type}, Size: {entry.size}, Offset: {entry.offset}"
            for entry in self.table.values()
        )


def get_things_from_node(node, symbol_table):
    if isinstance(node, Identifier):
        symbol = symbol_table.lookup(node.name)
        if symbol == -21:
            return None
        return symbol.var_type
    elif isinstance(node, Literal):
        return node.type_name
    elif isinstance(node, BinaryOp):
        left = get_things_from_node(node.left, symbol_table)
        right = get_things_from_node(node.right, symbol_table)
        if left == "FLOAT" or right == "FLOAT":
            return "FLOAT"
        return "INTEGER"
    return None


def get_name_from_identifier(node):
    if isinstance(node, Identifier):
        return node.name
    return None


def proccess_node(node, symbol_table):

    if isinstance(node, Assignment):
        left = get_name_from_identifier(node.id)
        right = get_things_from_node(node.expr, symbol_table)

        symbol_table.insert(left, right)

    elif isinstance(node, Program):
        for statement in node.statements:
            proccess_node(statement, symbol_table)
