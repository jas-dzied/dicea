from lexer import RawToken, Number, String, Ident
from astlib import Expression, Block, Builtin

import std
import lexer

def run(tree):
    ctx = Context()
    tree.eval(ctx)
    return ctx

def _lib(ctx, fname):
    if fname.eval(ctx).startswith('#'):
        fname = "/home/jas/Documents/Programming/Python/dicea/stdlib/"+fname.eval(ctx)[1:]+".da"
    else:
        fname = fname.eval(ctx)
    with open(fname, 'r') as file:
        tokens = lexer.Lexer(file.read()).lex()
    tree = generate_tree(tokens)
    response = run(tree)
    ctx.functions = {**ctx.functions, **response.functions}

class Context:
    def __init__(self):
        self.functions = {**{func[1:]: Builtin(getattr(std, func)) for func in dir(std)}, **{'lib': Builtin(_lib)}}
        self.variables = {}
        self.return_value = None
        self.python_context = {}
        self.consts = {}

def generate_tree(tokens, mode=Block):
    if mode == Expression:

        final_tokens = []
        working = []
        expr_level = 0
        bloc_level = 0

        for token in tokens:
            if token == RawToken('('):
                expr_level += 1
                if expr_level > 1 or bloc_level > 0:
                    working.append(token)
            elif token == RawToken(')'):
                expr_level -= 1
                if expr_level == 0 and bloc_level == 0:
                    final_tokens.append(generate_tree(working, Expression))
                    working = []
                else:
                    working.append(token)
            elif token == RawToken('['):
                bloc_level += 1
                if bloc_level > 1 or expr_level > 0:
                    working.append(token)
            elif token == RawToken(']'):
                bloc_level -= 1
                if bloc_level == 0 and expr_level == 0:
                    final_tokens.append(generate_tree(working, Block))
                    working = []
                else:
                    working.append(token)
            else:
                if expr_level > 0 or bloc_level > 0:
                    working.append(token)
                else:
                    final_tokens.append(token)

        return Expression(final_tokens)

    elif mode == Block:

        result = []
        working = []
        level = 0

        for token in tokens:
            if token == RawToken('(') or token == RawToken('['):
                level += 1
                working.append(token)
            elif token == RawToken(')') or token == RawToken(']'):
                level -= 1
                working.append(token)
            elif token == RawToken(';'):
                if level == 0:
                    result.append(generate_tree(working, Expression))
                    working = []
                else:
                    working.append(token)
            else:
                working.append(token)

        return Block(result)


