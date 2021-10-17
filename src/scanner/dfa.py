import re
from share.token import Token, TokenType


def create_token(token_name, lexeme, n):
    return str(n) + '\t' + '(' + token_name + ',' + str(lexeme) + ')'


final_states_name = {2: 'NUMBER', 5: 'SYMBOL', 7: 'SYMBOL', 8: 'SYMBOL', 14: 'WHITECHAR', 11: 'COMMENT', 4: 'ID'}

final_states_with_look_ahead = (2, 4, 8)

comment_or_whitechar = (14, 11)


class DFA:
    def __init__(self, states, transitions, initial, final_function_by_final_state):
        self.states = states
        self.transitions = transitions
        self.initial = initial
        self.final_function_by_final_state = final_function_by_final_state

    def run(self, program, pointer, line_number):
        state = self.initial
        for forward in range(pointer, len(program)):
            if program[forward] == '\n':
                line_number += 1
            available_transitions = [transition for transition in self.transitions
                                     if transition.match(state, program[forward])]
            if len(available_transitions) != 1:
                # handle error seperate function
                print(state)
                print('saa', program[forward], state)
                print((available_transitions[0].pattern , available_transitions[1].pattern))
            state = available_transitions[0].next_state
            if state in self.final_function_by_final_state.keys():
                # print('sa')
                if state in final_states_with_look_ahead:
                    forward -= 1
                    if program[forward] == '\n':
                        line_number -= 1
                lexeme = program[pointer:forward + 1]
                result = forward + 1, self.final_function_by_final_state[state](lexeme), line_number
                return result


class Transition:
    def __init__(self, state, pattern, next_state):
        self.state = state
        self.pattern = pattern
        self.next_state = next_state

    def match(self, state, c):
        return re.match(self.pattern, c) and state == self.state
