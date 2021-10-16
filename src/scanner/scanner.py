from .dfa import DFA, Transition


class Scanner:
    def __init__(self, program):
        self.program = program
        transitions = [Transition(1, '[0-9]', 1), Transition(1, '[^0-9]|\x1A', 2), Transition(0, '[A-Za-z]', 3),
                       Transition(3, '[A-Za-z0-9]', 3), Transition(3, '[^A-za-z0-9]|\x1A', 4),
                       Transition(0, '[\n\t\f\v\r ]', 14),
                       Transition(0, '[;:,\[\]\(\){}+\-*<]', 5), Transition(0, '=', 6),
                       Transition(6, '=', 7), Transition(6, '[^=]', 8), Transition(0, '[0-9]', 1),
                       Transition(0, '/', 9), Transition(9, '/', 10), Transition(9, '\*', 12),
                       Transition(12, '[^*]', 12), Transition(12, '\*', 13), Transition(13, '\*', 13),
                       Transition(13, '/', 11), Transition(13, '[^*]', 12), Transition(10, '\x1A|\n', 11),
                       Transition(10, '[^\x1A\n]', 10)]
        self.dfa_instance = DFA(states=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], transitions=transitions,
                                initial=0,
                                finals=[2, 4, 5, 8, 14, 11])

    def get_next_token(self):
        pointer = 0
        n = 1
        while True:
            pointer, data, n = self.dfa_instance.run(self.program, pointer, n)
            print(data)
            if pointer >= len(self.program) - 1:
                return
