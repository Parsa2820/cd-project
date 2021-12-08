from scanner.scanner import Scanner
from share.token import Token, TokenType
from share.symboltable import SymbolTable
from auxiliaryset import First, Follow


def update_current_token():
    TransitionDiagram.current_token = TransitionDiagram.scanner.next_token()


class TransitionDiagram:
    scanner: Scanner = None
    current_token: Token = None

    def __init__(self, states, scanner, init_state, first, follow):
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
                pass # we were here
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
        if not self.__token_equal_terminal(token):
            return False
        update_current_token()
        return True

    def match_first(self, token):
        return self.__token_equal_terminal(token)

    def __token_equal_terminal(self, token):
        if token.type != self.terminal.type:
            return False
        if token.type == TokenType.KEYWORD or token.type == TokenType.SYMBOL:
            if token.value != self.terminal.value:
                return False
        return True


class NonTerminalTransition(AbstractTransitionType):
    def __init__(self, transition_diagram: TransitionDiagram):
        self.transition_diagram = transition_diagram

    def match(self, token):
        return token == self.non_terminal

    def match_first(self, token):
        if self.transition_diagram.first.include(token):
            return True
        if self.transition_diagram.follow.include(token) and self.transition_diagram.first.has_epsilon:
            return True
        return False
