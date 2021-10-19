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


def write_tokens_file(scanner):
    prev_line_number = 0
    token_file = open("tokens.txt", "w")
    lexical_errors_file = open("lexical_errors.txt", "w")
    try:
        token = scanner.get_next_token()
    except ScannerError as error:
        write_lexical_error_file(lexical_errors_file, error)
    first_line_flag = True
    while token:
        if token.type == TokenType.WHITESPACE or token.type == TokenType.COMMENT:
            try:
                token = scanner.get_next_token()
            except ScannerError as error:
                write_lexical_error_file(lexical_errors_file, error)
            continue
        if prev_line_number != scanner.line_number:
            prev_line_number = scanner.line_number
            if  first_line_flag:
                token_file.write(f'{prev_line_number}.\t')
            else:
                token_file.write(f'\n{prev_line_number}.\t')
            first_line_flag = False
        token_file.write(f'{str(token)} ')
        try:
            token = scanner.get_next_token()
        except ScannerError as error:
            write_lexical_error_file(lexical_errors_file, error)
    lexical_errors_file.close()
    token_file.close()


def run_parser():
    program = read_all_file()
    program_scanner = Scanner(program)
    write_tokens_file(program_scanner)
    write_symbol_table_file()


if __name__ == '__main__':
    run_parser()
