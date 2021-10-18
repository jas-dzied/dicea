import lextools

LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
NUMBERS = '1234567890.-'

class Token:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'({self.__class__.__name__}:{repr(self.value)})'
    def id(self, ctx):
        return self.value
    def eval(self, ctx):
        return self.value
    def _id(self):
        return f'{self.__class__.__name__}::{self.value}'
    def __eq__(self, other):
        return self._id() == other._id()

class RawToken(Token):
    pass
class Number(Token):
    def __init__(self, value):
        if '.' in value:
            self.value = float(value)
        else:
            self.value = int(value)
class String(Token):
    pass
class Ident(Token):
    def eval(self, ctx):
        try:
            return ctx.consts[self.id(ctx)]
        except KeyError:
            try:
                return ctx.variables[self.id(ctx)]
            except KeyError:
                return ctx.functions[self.id(ctx)]

class Lexer(lextools.Lexer):

    def lex(self):
        tokens = []

        while self.i < len(self.text)-1:

            if self.char in LETTERS:
                tokens.append(Ident(self.make_while(LETTERS+NUMBERS)))
            elif self.char in NUMBERS:
                tokens.append(Number(self.make_while(NUMBERS)))
            elif self.char in '"'+"'":
                tokens.append(String(self.make_until('"'+"'")))
            elif self.char in ' \n':
                self.advance()
            else:
                tokens.append(RawToken(self.make_raw()))

        return tokens
