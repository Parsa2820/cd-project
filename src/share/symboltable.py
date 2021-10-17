from share.token import Token, TokenType

symbol_table = {1: 'if',
                2: 'else',
                3: 'void',
                4: 'int',
                5: 'repeat',
                6: 'break',
                7: 'until',
                8: 'return'}


def extend_symbol_table(symbol_table_length, x):
    symbol_table.update({symbol_table_length + 1: x})
    return Token(TokenType.ID, x)
