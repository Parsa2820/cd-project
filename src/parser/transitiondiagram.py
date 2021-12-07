import enum
from scanner.scanner import Scanner
from share.token import Token, TokenType
from share.symboltable import SymbolTable


class TransitionDiagram:
    scanner: Scanner = None
    current_token: Token = None

    def __init__(self, states, scanner, init_state):
        self.states = states
        self.init_state = init_state

    def parse(self):
        current_state = self.init_state
        while not current_state.is_final:
            pass

    def update_current_token():
        TransitionDiagram.current_token = TransitionDiagram.scanner.next_token()


class State:
    def __init__(self, number, transitions, is_final):
        self.number = number
        self.transitions = transitions
        self.is_final = is_final

    def transmit(self, token):
        for transition in self.transitions:
            if check_first_set():
                return transition.next_state
        return None


class AbstractTransitionType:
    def match(self, token):
        pass


class EpsilonTransition(AbstractTransitionType):
    def match(self, token):
        return True


class TerminalTransition(AbstractTransitionType):
    def __init__(self, terminal: Token):
        self.terminal = terminal

    def match(self, token: Token):
        if token.type != self.terminal.type:
            return False
        if token.type == TokenType.KEYWORD or token.type == TokenType.SYMBOL:
            if token.value != self.terminal.value:
                return False
        TransitionDiagram.update_current_token()
        return True




class NonTerminalTransition(AbstractTransitionType):
    def __init__(self, non_terminal_transtion_diagram: TransitionDiagram):
        self.non_terminal_transtion_diagram = non_terminal_transtion_diagram

    def match(self, token):
        return token == self.non_terminal


class Transition:
    def __init__(self, transition_type: AbstractTransitionType, next_state):
        pass
