from .dfa import DFA, BadCharacterError, Transition, NoAvailableTransitionError, BadCharacterError
from share.token import Token, TokenType
from share.symboltable import symbol_table, extend_symbol_table


class Scanner:
    def __init__(self, program):
        self.program = program
        states = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        transitions = []
        transitions.extend(self.__get_number_transitions())
        transitions.extend(self.__get_id_keyword_transitions())
        transitions.extend(self.__get_symbol_transitions())
        transitions.extend(self.__get_comment_transitions())
        transitions.extend(self.__get_white_space_transitions())
        initial = 0
        final_function_by_final_state = {2: self.__get_final_function(TokenType.NUM),
                                         4: self.__get_final_function_id_keyword(),
                                         5: self.__get_final_function(TokenType.SYMBOL),
                                         7: self.__get_final_function(TokenType.SYMBOL),
                                         8: self.__get_final_function(TokenType.SYMBOL),
                                         11: self.__get_final_function(TokenType.COMMENT),
                                         14: self.__get_final_function(TokenType.WHITESPACE)}
        final_states_with_lookahead = [2, 4, 8]
        valid_character_pattern = '[\/A-Za-z0-9;:,\[\]\(\)\{\}+\-*<=\n\r\t\v\f\x1A ]'
        self.dfa_instance = DFA(states, transitions,
                                initial, final_function_by_final_state,
                                final_states_with_lookahead, valid_character_pattern
                                )
        self.lexeme_begin = 0
        self.line_number = 1

    def __get_number_transitions(self):
        number_transitions = [Transition(0, '[0-9]', 1),
                              Transition(1, '[0-9]', 1),
                              Transition(1, '[^0-9A-Za-z]|\x1A', 2)]
        return number_transitions

    def __get_id_keyword_transitions(self):
        id_keyword_transitions = [Transition(0, '[A-Za-z]', 3),
                                  Transition(3, '[A-Za-z0-9]', 3),
                                  Transition(3, '[^A-Za-z0-9]|\x1A', 4)]
        return id_keyword_transitions

    def __get_symbol_transitions(self):
        symbol_transitions = [Transition(0, '[;:,\[\]\(\){}+\-*<]', 5),
                              Transition(0, '=', 6),
                              Transition(6, '=', 7),
                              Transition(6, '[^=]', 8)]
        return symbol_transitions

    def __get_comment_transitions(self):
        comment_transitions = [Transition(0, '/', 9),
                               Transition(9, '/', 10),
                               Transition(9, '\*', 12),
                               Transition(12, '[^*\x1A]', 12),
                               Transition(12, '\*', 13),
                               Transition(13, '\*', 13),
                               Transition(13, '/', 11),
                               Transition(13, '[^/*\x1A]', 12),
                               Transition(10, '\x1A|\n', 11),
                               Transition(10, '[^\x1A\n]', 10)]
        return comment_transitions

    def __get_white_space_transitions(self):
        white_space_transitions = [Transition(0, '[\n\t\f\v\r ]', 14)]
        return white_space_transitions

    def __get_final_function(self, token_type):
        return lambda x: Token(token_type, x)

    def __get_final_function_id_keyword(self):
        def keyword_id_function(x):
            for i in range(1, 9):
                if symbol_table[i] == x:
                    return Token(TokenType.KEYWORD, x)

            symbol_table_length = len(symbol_table.keys())
            if symbol_table_length == 8:
                return extend_symbol_table(symbol_table_length, x)
            for i in range(9, symbol_table_length + 1):
                if symbol_table[i] == x:
                    return Token(TokenType.ID, x)
            return extend_symbol_table(symbol_table_length, x)

        return keyword_id_function

    def __handle_errors(self, error: NoAvailableTransitionError):
        if error.state in [12, 13]:
            error_lexeme = self.__get_error_lexeme(error.forward)
            self.lexeme_begin = error.forward + 1
            raise UnclosedCommentError(self.line_number, error_lexeme)
        elif error.state == 1:
            self.__handle_invalid_number_error(error)
        else:
            return None

    def __handle_invalid_number_error(self, error: NoAvailableTransitionError):
        error_lexeme = self.__get_error_lexeme(error.forward)
        self.lexeme_begin = error.forward + 1
        raise InvalidNumberError(self.line_number, error_lexeme)

    def __handle_invalid_input(self, error: BadCharacterError):
        error_lexeme = self.__get_error_lexeme(error.forward)
        self.lexeme_begin = error.forward + 1
        raise InvalidInputError(self.line_number, error_lexeme)

    def __get_error_lexeme(self, forward):
        return self.program[self.lexeme_begin:forward + 1]

    def __validate_token(self, token):
        self.__check_unmatched_comment_error(token)

    def __check_unmatched_comment_error(self, token):
        if token.type == TokenType.SYMBOL and token.value == '*' and self.program[self.lexeme_begin] == '/':
            self.lexeme_begin += 1
            raise UnmatchedCommentError(self.line_number)

    def get_next_token(self):
        if self.lexeme_begin > len(self.program):
            return None
        try:
            token = self.dfa_instance.run(self.program, self.lexeme_begin)
            if token is None:
                return None
            print(token.type)
            self.line_number += self.program[self.lexeme_begin:self.lexeme_begin + len(
                token.value)].count('\n')
            self.lexeme_begin += len(token.value)
            self.__validate_token(token)
            return token
        except BadCharacterError as e:
            self.__handle_invalid_input(e)
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
