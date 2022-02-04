from intercodegen.semerror import SemanticError
from scanner.scanner import Scanner
from share.token import Token, TokenType
from _parser.auxiliaryset import First, Follow
from _parser.parsetree.parsetree import ParseTreeNode


class TransitionDiagram:
    scanner: Scanner = None
    current_token: Token = None
    errors = []
    semantic_errors = []

    def __init__(self, init_state, first: First, follow: Follow, name: str):
        self.init_state = init_state
        self.first = first
        self.follow = follow
        self.name = name

    @staticmethod
    def update_current_token():
        token = TransitionDiagram.scanner.get_next_token()
        while token is None or token.type in [TokenType.COMMENT, TokenType.WHITESPACE]:
            token = TransitionDiagram.scanner.get_next_token()
        TransitionDiagram.current_token = token

    def parse(self, parent: ParseTreeNode):
        current_state = self.init_state
        while not current_state.is_final:
            current_state = current_state.transmit(
                TransitionDiagram.current_token, parent)
        return True

class State:
    def __init__(self, number, transitions, is_final=False):
        self.number = number
        self.transitions = transitions
        self.is_final = is_final

    def transmit(self, token, parent):
        for transition in self.transitions:
            match_result = False
            try:
                match_result = transition.match(token, parent)
            except SemanticError as e:
                e.line = transition.error_line_number
                TransitionDiagram.semantic_errors.append(e)
            if transition.match_first(token) and match_result:
                return transition.destination_state
        transition = self.transitions[0]
        if self.__check_dollar(token):
            raise Exception('Unexpected EOF')
        TransitionDiagram.errors.append(transition.get_error_message(token))
        if transition.match_follow(token):
            return transition.destination_state
        return self

    def __check_dollar(self, token):
        if token.value == '$':
            TransitionDiagram.errors.append(
                f'#{TransitionDiagram.scanner.line_number} : syntax error, Unexpected EOF')
            return True
        return False


class AbstractTransitionType:
    error_line_number = -1

    def __init__(self, destination_state: State):
        self.destination_state = destination_state
        self.semantic_action = lambda x: None

    def match(self, token, parent):
        pass

    def match_first(self, token):
        pass

    def match_follow(self, token):
        pass

    def get_error_message(self, token):
        pass

    def token_to_terminal(self, token):
        if token.type in [TokenType.SYMBOL, TokenType.KEYWORD]:
            return token.value
        return token.type.name


class EpsilonTransition(AbstractTransitionType):
    def match(self, token, parent):
        parent.add_child(ParseTreeNode('epsilon'))
        return True

    def match_first(self, token):
        return True

    def match_follow(self, token):
        return False


class TerminalTransition(AbstractTransitionType):
    def __init__(self, destination_state: State, terminal: Token):
        super().__init__(destination_state)
        self.terminal = terminal

    def match(self, token, parent):
        if not self.__token_equal_terminal(token):
            return False
        TransitionDiagram.update_current_token()
        AbstractTransitionType.error_line_number = TransitionDiagram.scanner.line_number
        node_value = str(token) if token.value != '$' else '$'
        parent.add_child(ParseTreeNode(node_value))
        self.semantic_action(token)
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

    def match_follow(self, token):
        return True

    def get_error_message(self, token):
        terminal = self.token_to_terminal(self.terminal)
        return f'#{AbstractTransitionType.error_line_number} : syntax error, missing {terminal}'


class NonTerminalTransition(AbstractTransitionType):
    def __init__(self, destination_state: State, transition_diagram: TransitionDiagram):
        super().__init__(destination_state)
        self.transition_diagram = transition_diagram

    def match(self, token, parent):
        current = ParseTreeNode(self.transition_diagram.name)
        current.parent = parent
        parent.add_child(current)
        result = self.transition_diagram.parse(current)
        if result:
            self.semantic_action(token)
            return True
        return False

    def match_first(self, token):
        if self.transition_diagram.first.include(token):
            return True
        if self.transition_diagram.first.has_epsilon and self.transition_diagram.follow.include(token):
            return True
        return False

    def match_follow(self, token):
        if self.transition_diagram.follow.include(token):
            return True
        return False

    def get_error_message(self, token):
        if self.match_follow(token) and not self.transition_diagram.first.has_epsilon:
            return f'#{AbstractTransitionType.error_line_number} : syntax error, missing {self.transition_diagram.name}'
        AbstractTransitionType.error_line_number = TransitionDiagram.scanner.line_number
        TransitionDiagram.update_current_token()
        return f'#{AbstractTransitionType.error_line_number} : syntax error, illegal {self.token_to_terminal(token)}'
