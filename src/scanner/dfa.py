import re


class DFA:
    def __init__(self, states, transitions, initial, final_function_by_final_state, final_states_with_lookahead,
                 valid_character_pattern, ignore_validate_states):
        self.states = states
        self.transitions = transitions
        self.initial = initial
        self.final_function_by_final_state = final_function_by_final_state
        self.final_states_with_lookahead = final_states_with_lookahead
        self.valid_character_pattern = valid_character_pattern
        self.ignore_validate_states = ignore_validate_states

    def validate_character(self, char, forward, state):
        if not re.match(self.valid_character_pattern, char) and state not in self.ignore_validate_states:
            raise BadCharacterError(char, forward)

    def run(self, program, lexeme_begin):
        state = self.initial
        for forward in range(lexeme_begin, len(program)):
            char = program[forward]
            self.validate_character(char, forward, state)
            available_transitions = [
                t for t in self.transitions if t.match(state, char)]
            if len(available_transitions) != 1:
                raise NoAvailableTransitionError(
                    available_transitions, state, char, forward)
            state = available_transitions[0].next_state
            if state in self.final_function_by_final_state.keys():
                if state in self.final_states_with_lookahead:
                    forward -= 1
                lexeme = program[lexeme_begin:forward + 1]
                return self.final_function_by_final_state[state](lexeme)


class Transition:
    def __init__(self, state, pattern, next_state):
        self.state = state
        self.pattern = pattern
        self.next_state = next_state

    def match(self, state, c):
        return re.match(self.pattern, c) and state == self.state


class NoAvailableTransitionError(Exception):
    def __init__(self, transitions, state, c, forward):
        self.transitions = transitions
        self.state = state
        self.c = c
        self.forward = forward

    def __str__(self):
        return (f'There are {len(self.transitions)} transitions '
                f'in the state "{self.state}" and '
                f'for the character "{self.c}".')


class BadCharacterError(Exception):
    def __init__(self, c, forward):
        self.c = c
        self.forward = forward

    def __str__(self):
        return f'The character "{self.c}" is not valid.'
