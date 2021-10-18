from astlib import Block, Custom, Expression
from lexer import String, Number, Ident
import random

## OUTPUT ##
def _println(ctx, *args):
    print(*[arg.eval(ctx) for arg in args])
def _print(ctx, *args):
    print(*[arg.eval(ctx) for arg in args], end="")

## MATHS ##
def _add(ctx, a, b):
    return a.eval(ctx) + b.eval(ctx)
def _adds(ctx, *items):
    current = items[0].eval(ctx)
    for item in items[1:]:
        current += item.eval(ctx)
    return current
def _subtract(ctx, a, b):
    return a.eval(ctx) - b.eval(ctx)
def _times(ctx, a, b):
    return a.eval(ctx) * b.eval(ctx)
def _divide(ctx, a, b):
    return a.eval(ctx) / b.eval(ctx)
def _random(ctx, a, b):
    return random.randint(a.eval(ctx), b.eval(ctx))

## BOOLEAN LOGIC ##
def _equal(ctx, a, b):
    return a.eval(ctx) == b.eval(ctx)
def _notequal(ctx, a, b):
    return a.eval(ctx) != b.eval(ctx)
def _greater(ctx, a, b):
    return a.eval(ctx) > b.eval(ctx)
def _less(ctx, a, b):
    return a.eval(ctx) < b.eval(ctx)
def _greater_or_equal(ctx, a, b):
    return a.eval(ctx) >= b.eval(ctx)
def _less_or_equal(ctx, a, b):
    return a.eval(ctx) <= b.eval(ctx)

def _not(ctx, a):
    return not(a.eval(ctx))
def _and(ctx, a, b):
    return a.eval(ctx) and b.eval(ctx)
def _or(ctx, a, b):
    return a.eval(ctx) or b.eval(ctx)

## VARIABLES AND FUNCTIONS ##
def _set(ctx, name, value):
    ctx.variables[name.id(ctx)] = value.eval(ctx)
def _get(ctx, name):
    return ctx.variables[name.id(ctx)]
def _define(ctx, name, actions, *arguments):
    ctx.functions[name.id(ctx)] = Custom(actions, [arg.id(ctx) for arg in arguments])
def _function(ctx, actions, *arguments):
    return Custom(actions, [arg.id(ctx) for arg in arguments])
def _return(ctx, value):
    ctx.return_value = value.eval(ctx)
def _raw(ctx, value):
    return value
def _const(ctx, name, value):
    ctx.consts[name.id(ctx)] = value.eval(ctx)

## PYTHON INTEGRATION ##
def _python_exec(ctx, command):
    if " os " in command or ",os" in command or "os," in command or ", os" in command:
        return
    else:
        exec(command.eval(ctx), ctx.python_context)
def _python_eval(ctx, command):
    return eval(command.eval(ctx), ctx.python_context)

## CONTROL FLOW ##
def _if(ctx, condition, actions, else_actions=Block([])):
    if condition.eval(ctx):
        return actions.eval(ctx)
    else:
        return else_actions.eval(ctx)
def _while(ctx, condition, actions):
    while condition.eval(ctx):
        actions.eval(ctx)
    return ctx.return_value
def _for(ctx, name, iterator, actions):
    for i in iterator.eval(ctx):
        ctx.variables[name.id(ctx)] = i
        actions.eval(ctx)

## BASIC DATA TYPES ##
def _number(ctx, value):
    as_str = str(value.eval(ctx))
    if "." in as_str:
        return float(as_str)
    else:
        return int(as_str)
def _string(ctx, value):
    return str(value.eval(ctx))
def _repr(ctx, value):
    return repr(value.eval(ctx))
def _bool(ctx, value):
    return bool(value.eval(ctx))
def _list(ctx, *values):
    return [value.eval(ctx) for value in values]

## LIST FUNCTIONS ##
def _range(ctx, start, end):
    return range(start.eval(ctx), end.eval(ctx))
def _push(ctx, lst, item):
    lst.eval(ctx).append(item.eval(ctx))
def _pop(ctx, lst, index=None):
    if index:
        return lst.eval(ctx).pop(index.eval(ctx))
    else:
        return lst.eval(ctx).pop()

def _retoken(token):
    if isinstance(token, str):
        return String(token)
    elif isinstance(token, int) or isinstance(token, float):
        return Number(token)
    elif isinstance(token, list):
        return Expression([Ident('list'), *list(map(_retoken, token))])

def _map(ctx, lst, func):
    function = ctx.functions[func.id(ctx)]
    input_tokens = list(map(_retoken, lst.eval(ctx)))
    return list(map(lambda x: function.call(ctx, x), input_tokens))

def _roll(ctx, count, sides):
    global randgen
    return [random.randint(1, sides.eval(ctx)) for _ in range(count.eval(ctx))]
