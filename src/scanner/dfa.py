import re


def create_token(token_name, lexeme, n):
    return str(n) + '\t' + '(' + token_name + ',' + str(lexeme) + ')'


final_states_name = {2: 'NUMBER', 5: 'SYMBOL', 7: 'SYMBOL', 8: 'SYMBOL', 14: 'WHITECHAR', 11: 'COMMENT', 4: 'ID'}

final_states_with_look_ahead = (2, 4, 8)

comment_or_whitechar = (14, 11)


class DFA:
    def __init__(self, states, transitions, initial, finals):
        self.states = states
        self.transitions = transitions
        self.initial = initial
        self.finals = finals

    def run(self, program, pointer, n):
        state = self.initial
        flag = False
        for i in range(pointer, len(program)):
            if program[i] == '\n':
                n += 1
                flag = True
            available_transitions = [transition for transition in self.transitions if
                                     transition.match(state, program[i])]
            #print("lsoor" ,program[i], state , available_transitions[0].pattern)
            if len(available_transitions) != 1:
                print(program[i], state)
                print(available_transitions)
            state = available_transitions[0].next_state
            if state in self.finals:
                final_state_name = final_states_name[state]
                if state in final_states_with_look_ahead:
                    i -= 1;
                    if flag:
                        n -= 1
                if state in comment_or_whitechar:
                    return i + 1, '', n
                return i + 1, create_token(final_state_name, program[pointer:i + 1], n), n


class Transition:
    def __init__(self, state, pattern, next_state):
        self.state = state
        self.pattern = pattern
        self.next_state = next_state

    def match(self, state, c):
        return re.match(self.pattern, c) and state == self.state
