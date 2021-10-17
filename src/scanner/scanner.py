from .dfa import DFA, Transition
from share.token import Token, TokenType
from compiler import symbol_table


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


def extend_symbol_table(symbol_table_length, x):
    symbol_table.update({symbol_table_length + 1: x})
    return Token(TokenType.ID, x)


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
                                         4: keyword_id_function,
                                         5: self.__get_final_function(TokenType.SYMBOL),
                                         7: self.__get_final_function(TokenType.SYMBOL),
                                         8: self.__get_final_function(TokenType.SYMBOL),
                                         11: self.__get_final_function(TokenType.COMMENT),
                                         14: self.__get_final_function(TokenType.WHITESPACE)}
        self.dfa_instance = DFA(states, transitions, initial, final_function_by_final_state)
        self.begin_lexeme = 0
        self.line_number = 1

    def __get_number_transitions(self):
        number_transitions = [Transition(0, '[0-9]', 1),
                              Transition(1, '[0-9]', 1),
                              Transition(1, '[^0-9]|\x1A', 2)]
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
                               Transition(12, '[^*]', 12),
                               Transition(12, '\*', 13),
                               Transition(13, '\*', 13),
                               Transition(13, '/', 11),
                               Transition(13, '[^/*]', 12),
                               Transition(10, '\x1A|\n', 11),
                               Transition(10, '[^\x1A\n]', 10)]
        return comment_transitions

    def __get_white_space_transitions(self):
        white_space_transitions = [Transition(0, '[\n\t\f\v\r ]', 14)]
        return white_space_transitions

    def __get_final_function(self, token_type):
        return lambda x: Token(token_type, x)

    def __get_final_function_id_keyword(self):
        return lambda x: Token(TokenType.KEYWORD, x)

    def get_next_token(self):
        if self.begin_lexeme < len(self.program) - 1:
            self.begin_lexeme, token, self.line_number = self.dfa_instance.run(self.program, self.begin_lexeme,
                                                                               self.line_number)
            return token
        return
