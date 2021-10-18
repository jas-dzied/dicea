class Lexer:
    def __init__(self, text):
        self.text = text+' '
        self.i = -1
        self.line = 0
        self.column = -1
        self.advance()
    def advance(self):
        self.i += 1
        self.column += 1
        self.char = self.text[self.i]
        if self.char == '\n':
            self.line += 1
            self.column = -1

    def make_while(self, condition):
        result = ''
        while self.char in condition:
            result += self.char
            self.advance()
        return result

    def make_until(self, condition):
        result = ''
        self.advance()
        while not(self.char in condition):
            result += self.char
            self.advance()
        self.advance()
        return result

    def make_raw(self):
        value = self.char
        self.advance()
        return value
