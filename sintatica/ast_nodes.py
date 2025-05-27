class Program:
    def __init__(self, statements):
        self.statements = statements if statements else []


class Expression:
    pass


class BinaryOp(Expression):
    def __init__(self, left, op, right):
        self.left, self.op, self.right = left, op, right


class RangeOp(Expression):
    def __init__(self, start, end):
        self.start, self.end = start, end


class UnaryOp(Expression):
    def __init__(self, op, expr):
        self.op, self.expr = op, expr


class Literal(Expression):
    def __init__(self, value, type_name):
        self.value, self.type_name = value, type_name


class Identifier(Expression):
    def __init__(self, name):
        self.name = name


class Assignment(Expression):
    def __init__(self, id, expr):
        self.id, self.expr = id, expr


class FunctionCall(Expression):
    def __init__(self, function_name, args):
        self.function_name, self.args = function_name, args


class IfStatement:
    def __init__(self, condition, true_block, else_block=None):
        self.condition, self.true_block, self.else_block = (
            condition,
            true_block,
            else_block,
        )


class WhileLoop:
    def __init__(self, condition, block):
        self.condition, self.block = condition, block


class ForLoop:
    def __init__(self, var, iterator, block):
        self.var, self.iterator, self.block = var, iterator, block


class FunctionDef:
    def __init__(self, name, params, body):
        self.name, self.params, self.body = name, params, body


class Block:
    def __init__(self, statements):
        self.statements = statements


class ReturnStatement:
    def __init__(self, expr):
        self.expr = expr
