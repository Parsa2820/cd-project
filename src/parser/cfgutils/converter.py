import re
from parser.auxiliaryset import First, Follow
from parser.transitiondiagram import EpsilonTransition, NonTerminalTransition, State, TerminalTransition, TransitionDiagram
from share.token import Token, TokenType


class CfgToTransitionDiagramConverter:
    AUX_SET_PATTERN = re.compile(r'(\w+)\s*(.*)')

    def __init__(self, cfg, firsts_string, follows_string):
        cfg = '''E -> T X $
        T -> ( E ) | int Y
        X -> + E | EPSILON
        Y -> * T | EPSILON'''

        firsts_string = '''T 	(, int
        X 	+, EPSILON
        Y 	*, EPSILON
        E 	(, int'''

        follows_string = '''E 	$, )
        T 	$, +
        X 	$
        Y 	$, +
        '''

        self.firsts = {}
        self.follows = {}
        self.rules = {}
        self.transition_diagrams_by_name = {}
        self.start_symbol = None
        self.__extract_firsts(firsts_string)
        self.__extract_follows(follows_string)
        self.__extract_rules(cfg)
        self.__init_transition_diagrams()

    def __extract_firsts(self, firsts_string):
        aux_set_matched = CfgToTransitionDiagramConverter.AUX_SET_PATTERN.findall(
            firsts_string)
        for key, value in aux_set_matched:
            has_epsilon = False
            first = []
            for x in re.split(r'\s*,\s*', value):
                if x == 'EPSILON':
                    has_epsilon = True
                else:
                    first.append(self.__terminal_to_token(x))
            self.firsts[key] = First(first, has_epsilon)

    def __extract_follows(self, follows_string):
        aux_set_matched = CfgToTransitionDiagramConverter.AUX_SET_PATTERN.findall(
            follows_string)
        for key, value in aux_set_matched:
            self.follows[key] = Follow(
                [self.__terminal_to_token(x) for x in re.split(r'\s*,\s*', value)])

    def __extract_rhs(self, rhs_string):
        single = re.split(r'\s*\|\s*', rhs_string)
        return [re.split(r'\s+', s) for s in single]

    def __get_number_of_states(self, rhs_list):
        x = 2
        for rhs in rhs_list:
            x += len(rhs) - 1
        return x

    def __terminal_to_token(self, terminal):
        if terminal in ['$', ';', '[', ']', '(', ')', '{', '}', '<', '==', '+', '-', '*', ',']:
            return Token(TokenType.SYMBOL, terminal)
        if terminal in ['if', 'endif', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']:
            return Token(TokenType.KEYWORD, terminal)
        if terminal == 'NUM':
            return Token(TokenType.NUM, 0)
        if terminal == 'ID':
            return Token(TokenType.ID, '')
        raise Exception('Unknown terminal: ' + terminal)

    def __get_transition(self, diagram_next_state, symbol):
        if symbol == 'EPSILON':
            return EpsilonTransition(diagram_next_state)
        elif symbol in self.rules.keys():
            return NonTerminalTransition(diagram_next_state, self.transition_diagrams_by_name[symbol])
        else:
            return TerminalTransition(diagram_next_state, self.__terminal_to_token(symbol))

    def __get_state(self, diagram_next_state, symbol):
        state_number = diagram_next_state.number - 1
        transition = self.__get_transition(diagram_next_state, symbol)
        return State(state_number, [transition])

    def __extract_rules(self, cfg):
        rule_pattern = re.compile(r'(\w+)\s*->\s*(.*)')
        rules_matched = rule_pattern.findall(cfg)
        for lhs, rhs_list in rules_matched:
            self.rules[lhs] = self.__extract_rhs(rhs_list)

    def __init_transition_diagrams(self):
        for lhs in self.rules.keys():
            self.transition_diagrams_by_name[lhs] = TransitionDiagram(
                None, self.firsts[lhs], self.follows[lhs], lhs)
            if self.start_symbol is None:
                self.start_symbol = lhs

    def get_grammar_diagram(self):
        for lhs, rhs_list in self.rules.items():
            number_of_states = self.__get_number_of_states(rhs_list)
            start_state = State(0, [])
            final_state = State(number_of_states-1, [], True)
            self.transition_diagrams_by_name[lhs].init_state = start_state
            for rhs in reversed(rhs_list):
                diagram_next_state = final_state
                for symbol in reversed(rhs[1:]):
                    diagram_next_state = self.__get_state(
                        diagram_next_state, symbol)
                start_state.transitions.insert(
                    0, self.__get_transition(diagram_next_state, rhs[0]))

        return self.transition_diagrams_by_name[self.start_symbol]
