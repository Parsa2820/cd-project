from .dfa import DFA, BadCharacterError, Transition, NoAvailableTransitionError, BadCharacterError
from share.token import Token, TokenType
from share.symboltable import SymbolTable


class Scanner:
    NUMBER_TRANSITIONS = [Transition(0, '[0-9]', 1),
                          Transition(1, '[0-9]', 1),
                          Transition(1, '[^0-9A-Za-z]|\x1A', 2)]

    ID_KEYWORD_TRANSITIONS = [Transition(0, '[A-Za-z]', 3),
                              Transition(3, '[A-Za-z0-9]', 3),
                              Transition(3, '[^A-Za-z0-9]|\x1A', 4)]

    SYMBOL_TRANSITIONS = [Transition(0, '[;:,\[\]\(\){}+\-*<]', 5),
                          Transition(0, '=', 6),
                          Transition(6, '=', 7),
                          Transition(6, '[^=]', 8)]

    COMMENT_TRANSITIONS = [Transition(0, '/', 9),
                           Transition(9, '/', 10),
                           Transition(9, '\*', 12),
                           Transition(12, '[^*\x1A]', 12),
                           Transition(12, '\*', 13),
                           Transition(13, '\*', 13),
                           Transition(13, '/', 11),
                           Transition(13, '[^/*\x1A]', 12),
                           Transition(10, '\x1A|\n', 11),
                           Transition(10, '[^\x1A\n]', 10)]

    WHITESPACE_TRANSITIONS = [Transition(0, '[\n\t\f\v\r ]', 14)]

    LAST_TOKEN = Token(TokenType.ID, '$')

    def __init__(self, program, symbol_table):
        self.program = program
        self.dfa_instance = self.__create_DFA()
        self.lexeme_begin = 0
        self.line_number = 1
        self.symbol_table = symbol_table

    def __create_DFA(self):
        states = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        transitions = []
        transitions.extend(Scanner.NUMBER_TRANSITIONS)
        transitions.extend(Scanner.ID_KEYWORD_TRANSITIONS)
        transitions.extend(Scanner.SYMBOL_TRANSITIONS)
        transitions.extend(Scanner.COMMENT_TRANSITIONS)
        transitions.extend(Scanner.WHITESPACE_TRANSITIONS)
        initial = 0
        final_function_by_final_state = {2: Scanner.__get_final_function(TokenType.NUM),
                                         4: self.__get_final_function_id_keyword(),
                                         5: Scanner.__get_final_function(TokenType.SYMBOL),
                                         7: Scanner.__get_final_function(TokenType.SYMBOL),
                                         8: Scanner.__get_final_function(TokenType.SYMBOL),
                                         11: Scanner.__get_final_function(TokenType.COMMENT),
                                         14: Scanner.__get_final_function(TokenType.WHITESPACE)}
        final_states_with_lookahead = [2, 4, 8]
        valid_character_pattern = '[\/A-Za-z0-9;:,\[\]\(\)\{\}+\-*<=\n\r\t\v\f\x1A ]'
        ignore_validate_states = [10, 12, 13]
        return DFA(states, transitions,
                   initial, final_function_by_final_state,
                   final_states_with_lookahead, valid_character_pattern, ignore_validate_states
                   )

    def __get_final_function(token_type):
        return lambda x: Token(token_type, x)

    def __get_final_function_id_keyword(self):
        def keyword_id_function(x):
            if self.symbol_table.is_keyword(x):
                return Token(TokenType.KEYWORD, x)
            elif self.symbol_table.contains(x):
                return Token(TokenType.ID, x)
            else:
                self.symbol_table.extend(x)
                return Token(TokenType.ID, x)

        return keyword_id_function

    def __handle_errors(self, error: NoAvailableTransitionError):
        if error.state in [12, 13]:
            error_lexeme = self.__get_error_lexeme(error.forward)
            self.lexeme_begin = error.forward + 1
            raise UnclosedCommentError(self.line_number, error_lexeme)
        elif error.state == 1:
            self.__handle_invalid_number_error(error)
        else:
            self.__handle_invalid_input_error(BadCharacterError(
                c=error.c, forward=error.forward - 1))

    def __handle_invalid_number_error(self, error: NoAvailableTransitionError):
        error_lexeme = self.__get_error_lexeme(error.forward)
        self.lexeme_begin = error.forward + 1
        raise InvalidNumberError(self.line_number, error_lexeme)

    def __handle_invalid_input_error(self, error: BadCharacterError):
        error_lexeme = self.__get_error_lexeme(error.forward)
        self.lexeme_begin = error.forward + 1
        raise InvalidInputError(self.line_number, error_lexeme)

    def __get_error_lexeme(self, forward):
        return self.program[self.lexeme_begin:forward + 1]

    def __validate_token(self, token):
        self.__check_panic_mode_for_star(token)
        self.__check_unmatched_comment_error(token)

    def __check_unmatched_comment_error(self, token):
        if token.type == TokenType.SYMBOL and token.value == '*' and self.program[self.lexeme_begin] == '/':
            self.lexeme_begin += 1
            raise UnmatchedCommentError(self.line_number)

    def __check_panic_mode_for_star(self, token):
        self.lexeme_begin -= 1
        try:
            if token.type == TokenType.SYMBOL and token.value == '*':
                self.dfa_instance.validate_character(
                    self.program[self.lexeme_begin+1], self.lexeme_begin+1, 5)
        except BadCharacterError as e:
            self.__handle_invalid_input_error(e)
        self.lexeme_begin += 1

    def get_next_token(self):
        if self.is_program_finished():
            return Scanner.LAST_TOKEN
        try:
            token = self.dfa_instance.run(self.program, self.lexeme_begin)
            if token is None:
                return Scanner.LAST_TOKEN
            self.line_number += self.program[self.lexeme_begin:self.lexeme_begin + len(
                token.value)].count('\n')
            self.lexeme_begin += len(token.value)
            self.__validate_token(token)

            return token
        except BadCharacterError as e:
            self.__handle_invalid_input_error(e)
        except NoAvailableTransitionError as e:
            self.__handle_errors(e)

    def is_program_finished(self):
        return self.lexeme_begin >= len(self.program) - 1


class ScannerError(Exception):
    def __init__(self, line_number, error_lexeme, error_type):
        self.line_number = line_number
        self.error_lexeme = error_lexeme
        self.error_type = error_type

    def __str__(self):
        return f'({self.error_lexeme}, {self.error_type})'


class UnmatchedCommentError(ScannerError):
    def __init__(self, line_number):
        super().__init__(line_number, '*/', 'Unmatched comment')


class UnclosedCommentError(ScannerError):
    def __init__(self, line_number, error_lexeme):
        short_lexeme = f'{error_lexeme[:7]}{"..." if len(error_lexeme) > 7 else ""}'
        super().__init__(line_number, short_lexeme, 'Unclosed comment')


class InvalidInputError(ScannerError):
    def __init__(self, line_number, error_lexeme):
        super().__init__(line_number, error_lexeme, 'Invalid input')


class InvalidNumberError(ScannerError):
    def __init__(self, line_number, error_lexeme):
        super().__init__(line_number, error_lexeme, 'Invalid number')
