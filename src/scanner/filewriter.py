import os
from scanner.scanner import ScannerError
from share.token import TokenType
from share.symboltable import SymbolTable


class ScannerFileWriter:
    SYMBOL_TABLE_FILE_NAME = 'symbol_table.txt'
    TOKEN_FILE_NAME = 'tokens.txt'
    LEXICAL_ERRORS_FILE_NAME = 'lexical_errors.txt'
    NO_LEXICAL_ERRORS_MESSAGE = 'There is no lexical error.'

    def __init__(self, scanner, base_path):
        self.scanner = scanner
        self.lexical_errors = []
        self.base_path = base_path


    def write(self):
        self.__write_tokens()
        self.__write_lexical_errors()
        self.__write_symbol_table()

    def __write_tokens(self):
        previous_line_number = 0
        token_lines = []
        token = self.__get_valid_token()
        while token:
            if token.type not in [TokenType.WHITESPACE, TokenType.COMMENT]:
                if self.scanner.line_number != previous_line_number:
                    token_lines.append(f'{self.scanner.line_number}.\t{token}')
                    previous_line_number = self.scanner.line_number
                else:
                    token_lines[len(token_lines) - 1] += f' {token}'
            token = self.__get_valid_token()
        path = self.__get_file_path(ScannerFileWriter.TOKEN_FILE_NAME)
        with open(path, 'w') as token_file:
            token_file.write('\n'.join(token_lines))
            token_file.write('\n')

    def __get_valid_token(self):
        token = None
        while not token and not self.scanner.is_program_finished():
            try:
                token = self.scanner.get_next_token()
            except ScannerError as error:
                self.lexical_errors.append(error)
        return token

    def __write_lexical_errors(self):
        previous_line_number = 0
        lexical_errors_lines = []
        if len(self.lexical_errors) == 0:
            lexical_errors_lines.append(
                ScannerFileWriter.NO_LEXICAL_ERRORS_MESSAGE)
        else:
            for error in self.lexical_errors:
                if error.line_number != previous_line_number:
                    lexical_errors_lines.append(
                        f'{error.line_number}.\t{error}')
                    previous_line_number = error.line_number
                else:
                    lexical_errors_lines[len(
                        lexical_errors_lines) - 1] += f' {error}'
        path = self.__get_file_path(ScannerFileWriter.LEXICAL_ERRORS_FILE_NAME)                        
        with open(path, 'w') as lexical_errors_file:
            lexical_errors_file.write('\n'.join(lexical_errors_lines))
            lexical_errors_file.write('\n')

    def __write_symbol_table(self):
        path = self.__get_file_path(ScannerFileWriter.SYMBOL_TABLE_FILE_NAME)
        with open(path, 'w') as symbol_table_file:
            symbol_table_file.write(f'{self.scanner.symbol_table}')
            symbol_table_file.write('\n')


    def __get_file_path(self, file_name):
        return os.path.join(self.base_path, file_name)
    