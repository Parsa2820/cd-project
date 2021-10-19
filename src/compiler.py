from scanner.scanner import Scanner, ScannerError
from share.token import TokenType
from share.symboltable import symbol_table


def read_all_file():
    with open("input.txt", "r") as program_file:
        program = program_file.read()
    program += chr(26)
    return program


def write_symbol_table_file():
    with open("symbol_table.txt", "w") as symbol_table_file:
        for id in symbol_table.keys():
            symbol_table_file.write(f'{id}.\t{symbol_table[id]}\n')


def write_lexical_error_file(lexical_errors_file, lexical_error):
    lexical_errors_file.write(f'{lexical_error}\n')


def get_valid_token(lexical_errors_file, scanner):
    token = False
    while not token and scanner.lexeme_begin != len(scanner.program):
        try:
            token = scanner.get_next_token()
        except ScannerError as error:
            write_lexical_error_file(lexical_errors_file, error)
    return token


def write_tokens_file(scanner):
    prev_line_number = 0
    token_file = open("tokens.txt", "w")
    lexical_errors_file = open("lexical_errors.txt", "w")
    lexical_error_counts = 0
    token = get_valid_token(lexical_errors_file, scanner)
    first_line_flag = True

    while token:
        try:
            if token.type == TokenType.WHITESPACE or token.type == TokenType.COMMENT:
                token = scanner.get_next_token()

                continue
            if prev_line_number != scanner.line_number:
                prev_line_number = scanner.line_number
                if first_line_flag:
                    token_file.write(f'{prev_line_number}.\t')
                else:
                    token_file.write(f'\n{prev_line_number}.\t')
                first_line_flag = False
            print('asla', token.type)
            token_file.write(f'{str(token)} ')

            token = scanner.get_next_token()

        except ScannerError as error:
            lexical_error_counts += 1
            write_lexical_error_file(lexical_errors_file, error)
            token = get_valid_token(lexical_errors_file,scanner)
    if lexical_error_counts == 0:
        lexical_errors_file.write('There is no lexical error.')
    lexical_errors_file.close()
    token_file.close()


def run_parser():
    program = read_all_file()
    program_scanner = Scanner(program)
    write_tokens_file(program_scanner)
    write_symbol_table_file()


if __name__ == '__main__':
    run_parser()
