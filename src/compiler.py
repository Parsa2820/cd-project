from scanner import scanner
from share.token import TokenType

symbol_table = {1: 'if',
                2: 'else',
                3: 'void',
                4: 'int',
                5: 'repeat',
                6: 'break',
                7: 'until',
                8: 'return'}


def initialize_symbol_table():
    symbol_table_file = open("symbol_table.txt", "w")
    for id in symbol_table.keys():
        symbol_table_file.write(f'{id}.\t{symbol_table[id]}\n')
    return symbol_table_file


def get_all_tokens():
    global symbol_table
    symbol_table = scanner.symbol_table
    symbol_table_length = 8
    symbol_table_file = initialize_symbol_table()
    program = read_file()
    program_scanner = scanner.Scanner(str(program))
    prev_line_number = 1
    token_file = open("tokens.txt", "w")
    token_file.write('1.\t')
    token = program_scanner.get_next_token()
    while token:
        if not (token.type == TokenType.WHITESPACE or token.type == TokenType.COMMENT):
            if prev_line_number == program_scanner.line_number:
                token_file.write(str(token) + ' ')
            else:
                prev_line_number = program_scanner.line_number
                token_file.write('\n')
                token_file.write(str(program_scanner.line_number) + '.\t' + str(token) + ' ')
        if symbol_table_length != len(symbol_table):
            symbol_table_file.write(f'{len(scanner.symbol_table)}.\t{token.value}\n')
            symbol_table_length = len(symbol_table)
        token = program_scanner.get_next_token()

    token_file.close()


def read_file():
    with open("input.txt", "r") as program_file:
        program = program_file.read()
    program += chr(26)
    return program


if __name__ == '__main__':
    get_all_tokens()
