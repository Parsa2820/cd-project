from .dfa import DFA, Transition


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
        finals = [2, 4, 5, 8, 14, 11]
        self.dfa_instance = DFA(states, transitions, initial, finals)

    def __get_number_transitions(self):
        number_transitions = [Transition(0, '[0-9]', 1),
                              Transition(1, '[0-9]', 1),
                              Transition(1, '[^0-9]|\x1A', 2)]
        return number_transitions

    def __get_id_keyword_transitions(self):
        id_keyword_transitions = [Transition(0, '[A-Za-z]', 3),
                                  Transition(3, '[A-Za-z0-9]', 3),
                                  Transition(3, '[^A-za-z0-9]|\x1A', 4)]
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
                               Transition(13, '[^*]', 12),
                               Transition(10, '\x1A|\n', 11),
                               Transition(10, '[^\x1A\n]', 10)]
        return comment_transitions

    def __get_white_space_transitions(self):
        white_space_transitions = [Transition(0, '[\n\t\f\v\r ]', 14)]
        return white_space_transitions

    def get_next_token(self):
        pointer = 0
        n = 1
        while True:
            pointer, data, n = self.dfa_instance.run(self.program, pointer, n)
            print(data)
            if pointer >= len(self.program) - 1:
                return
