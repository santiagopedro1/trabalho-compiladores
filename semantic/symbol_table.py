class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.scope_stack = ["global"]
        self.symbols["global"] = {}
        self.total_var_size = 0
        self.temp_var_count = 0

    def enter_scope(self, name):
        self.scope_stack.append(name)
        if name not in self.symbols:
            self.symbols[name] = {}

    def exit_scope(self):
        self.scope_stack.pop()

    def add_symbol(self, name, type):
        current_scope = self.scope_stack[-1]
        if name not in self.symbols[current_scope]:
            self.symbols[current_scope][name] = {
                "type": type,
                "size": 8,
                "offset": self.total_var_size,
            }
            self.total_var_size += 8
            return True
        return False

    def get_symbol(self, name):
        for scope_name in reversed(self.scope_stack):
            if name in self.symbols[scope_name]:
                return self.symbols[scope_name][name]
        return None

    def new_temp(self):
        temp_name = f"t{self.temp_var_count}"
        self.temp_var_count += 1
        return temp_name

    def to_string(self):
        output = ""
        for scope, symbols in self.symbols.items():
            output += f"--- Scope: {scope} ---\n"
            for name, info in symbols.items():
                output += f"  - Name: {name}, Type: {info['type']}, Size: {info['size']}, Offset: {info['offset']}\n"
        return output
