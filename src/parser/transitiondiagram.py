import enum
from scanner.scanner import Scanner
from share.token import Token, TokenType
from share.symboltable import SymbolTable


def is_in_token_set(input_token, token_set):
    for token in token_set:
        if token.type != input_token.type:
            continue
        elif token.type == TokenType.KEYWORD or token.type == TokenType.SYMBOL:
            if token.value == input_token.value:
                return True
        else:
            return True
    return False


def update_current_token():
    TransitionDiagram.current_token = TransitionDiagram.scanner.next_token()


class First:
    def __init__(self, tokens, has_epsilon, has_dollar):
        self.tokens = tokens
        self.has_epsilon = has_epsilon



class Follow:
    def __init__(self, tokens, has_dollar):
        self.tokens = tokens



class TransitionDiagram:
    scanner: Scanner = None
    current_token: Token = None

    def __init__(self, states, scanner, init_state, first, follow ):
        self.states = states
        self.init_state = init_state
        self.first = first
        self.follow = follow

    def parse(self):
        current_state = self.init_state
        while not current_state.is_final:
            pass


class State:
    def __init__(self, number, transitions, is_final):
        self.number = number
        self.transitions = transitions
        self.is_final = is_final

    def transmit(self, token):
        for transition in self.transitions:
            if not transition.match_first(token):
                continue
            if transition.match(token):
                TransitionDiagramtransition.destination_state
        return None


class AbstractTransitionType:

    def __init__(self, state):
        self.destination_state = state

    def match(self, token):
        pass

    def match_first(self, token):
        pass


class EpsilonTransition(AbstractTransitionType):
    def match(self, token):
        return True

    def match_first(self, token):
        return False


class TerminalTransition(AbstractTransitionType):
    def __init__(self, terminal: Token):
        self.terminal = terminal

    def match(self, token: Token):
        if token.type != self.terminal.type:
            return False
        if token.type == TokenType.KEYWORD or token.type == TokenType.SYMBOL:
            if token.value != self.terminal.value:
                return False
        update_current_token()
        return True

    def match_first(self, token):
        return is_in_token_set(token, [self.terminal])


class NonTerminalTransition(AbstractTransitionType):
    def __init__(self, non_terminal_transition_diagram: TransitionDiagram):
        self.non_terminal_transition_diagram = non_terminal_transition_diagram

    def match(self, token):
        return token == self.non_terminal

    def match_first(self, token):
        if is_in_token_set(token, self.non_terminal_transition_diagram.first.tokens):
            return True
        if is_in_token_set(token, self.non_terminal_transition_diagram.follow.tokens) \
                and self.non_terminal_transition_diagram.first.has_epsilon:
            return True
        return False


class Transition:
    def __init__(self, transition_type: AbstractTransitionType, next_state):
        pass
