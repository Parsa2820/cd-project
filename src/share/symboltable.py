from collections import OrderedDict
from share.symbol import Symbol


class SymbolTable:
    KEYWORDS = ['if', 'else', 'void', 'int',
                'repeat', 'break', 'until', 'return']

    def __init__(self):
        self.symbol_table = OrderedDict()
        self.last_id = 0
        self.__add_keywords()

    def __add_keywords(self):
        for keyword in SymbolTable.KEYWORDS:
            self.extend(keyword)

    def extend(self, lexeme):
        self.last_id += 1
        self.symbol_table.update({lexeme: Symbol(self.last_id, lexeme)})

    def is_keyword(self, lexeme):
        return lexeme in SymbolTable.KEYWORDS

    def contains(self, lexeme):
        return lexeme in self.symbol_table

    def __str__(self):
        symbols_str = [f'{symbol}' for symbol in self.symbol_table.values()]
        return '\n'.join(symbols_str)
