import re

class DFA:
    def __init__(self, states, transitions, initial, finals):
        self.states = states
        self.transitions = transitions
        self.initial = initial
        self.finals = finals

    def run(self, word):
        state = self.initial
        for c in word:
            available_transitions = [transition for transition in self.transitions if transition.match(state, c)]
            if len(available_transitions) != 1:
                return False
            state = available_transitions[0].next_state
        return state in self.finals

class Transition:
    def __init__(self, state, pattern, next_state):
        self.state = state
        self.pattern = pattern
        self.next_state = next_state
    
    def match(self, state, c):
        return re.match(self.pattern, c) and state == self.state