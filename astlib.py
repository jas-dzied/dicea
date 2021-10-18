import copy

class Expression:
    def __init__(self, tokens):
        self.tokens = tokens
    def __repr__(self):
        return f'Expr{repr(self.tokens)}'
    def eval(self, ctx):
        func_token = self.tokens[0]
        try:
            func = ctx.functions[func_token.id(ctx)]
        except KeyError:
            func = func_token.id(ctx)
        return func.call(ctx, *self.tokens[1:])
    def id(self, ctx):
        func_token = self.tokens[0]
        func = ctx.functions[func_token.id(ctx)]
        return func.call(ctx, *self.tokens[1:])

class Block:
    def __init__(self, expressions):
        self.expressions = expressions
    def __repr__(self):
        return f'Block{repr(self.expressions)}'
    def eval(self, ctx):
        for expression in self.expressions:
            expression.eval(ctx)
        return ctx.return_value
    def id(self, ctx):
        for expression in self.expressions:
            expression.eval(ctx)
        return ctx.return_value

class Builtin:
    def __init__(self, func):
        self.func = func
    def call(self, *args):
        return self.func(*args)

class Custom:
    def __init__(self, tokens, arguments):
        self.tokens = tokens
        self.arguments = arguments
    def call(self, ctx, *args):
        old_ctx = copy.deepcopy(ctx.variables)
        ctx.variables = {argname: args[i].eval(ctx) for i, argname in enumerate(self.arguments)}
        value = self.tokens.eval(ctx)
        ctx.variables = old_ctx
        return value
