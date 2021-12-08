from scanner.scanner import Scanner
from share.token import Token, TokenType
from parser.auxiliaryset import First, Follow
from parser.parsetree.parsetree import ParseTree, ParseTreeNode


class TransitionDiagram:
    scanner: Scanner = None
    current_token: Token = None

    def __init__(self, init_state, first: First, follow: Follow, name: str):
        self.init_state = init_state
        self.first = first
        self.follow = follow
        self.name = name

    @staticmethod
    def update_current_token():
        TransitionDiagram.current_token = TransitionDiagram.scanner.get_next_token()

    def parse(self, parent: ParseTreeNode):
        current_state = self.init_state
        while not current_state.is_final:
            current_state = current_state.transmit(TransitionDiagram.current_token, parent)

        parent.add_child(ParseTreeNode(self.name))
        return True


class State:
    def __init__(self, number, transitions, is_final = False):
        self.number = number
        self.transitions = transitions
        self.is_final = is_final

    def transmit(self, token, parent):
        for transition in self.transitions:
            if transition.match_first(token) and transition.match(token, parent):
                return transition.destination_state
        # handle error when no transition matches
        raise Exception("No transition matches")


class AbstractTransitionType:
    def __init__(self, destination_state: State):
        self.destination_state = destination_state

    def match(self, token, parent):
        pass

    def match_first(self, token):
        pass


class EpsilonTransition(AbstractTransitionType):
    def match(self, token, parent):
        parent.add_child(ParseTreeNode('epsilon'))
        return True

    def match_first(self, token):
        # hesse khobi behesh nadarim
        # bayad epsilon akhar bashe dar barresi transionha 
        return True


class TerminalTransition(AbstractTransitionType):
    def __init__(self, destination_state: State, terminal: Token):
        super().__init__(destination_state)
        self.terminal = terminal

    def match(self, token, parent):
        if not self.__token_equal_terminal(token):
            return False
        TransitionDiagram.update_current_token()
        parent.add_child(ParseTreeNode(str(token)))
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
    def __init__(self, destination_state: State, transition_diagram: TransitionDiagram):
        super().__init__(destination_state)
        self.transition_diagram = transition_diagram

    def match(self, token, parent):
        current = ParseTreeNode(self.transition_diagram.name)
        current.parent = parent
        result = self.transition_diagram.parse(current)
        return result
        # if result:
        #     parent.add_child(current)
        #     return True
        # return False

    def match_first(self, token):
        if self.transition_diagram.first.include(token):
            return True
        if self.transition_diagram.first.has_epsilon and self.transition_diagram.follow.include(token):
            return True
        return False
