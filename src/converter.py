import re
from parser.auxiliaryset import First, Follow
from parser.transitiondiagram import EpsilonTransition, NonTerminalTransition, State, TerminalTransition, TransitionDiagram
from share.token import Token, TokenType


class CfgToTransitionDiagramConverter:

    def __init__(self, cfg):
        self.cfg = '''E -> T X $
        T -> ( E ) | int Y
        X -> + E | EPSILON
        Y -> * T | EPSILON'''

        self.firsts = {
            'E': First([self.__terminal_to_token('int'), self.__terminal_to_token('(')]),
            'T': First([self.__terminal_to_token('int'), self.__terminal_to_token('(')]),
            'X': First([self.__terminal_to_token('+')], True),
            'Y': First([self.__terminal_to_token('*')], True)
        }

        self.follows = {
            'E': Follow([self.__terminal_to_token(')'), self.__terminal_to_token('$')]),
            'T': Follow([self.__terminal_to_token('+'), self.__terminal_to_token(')'), self.__terminal_to_token('$')]),
            'Y': Follow([self.__terminal_to_token('+'), self.__terminal_to_token(')'), self.__terminal_to_token('$')]),
            'X': Follow([self.__terminal_to_token(')'), self.__terminal_to_token('$')])
        }

        self.rules = {}
        self.transition_diagrams_by_name = {}
        self.start_symbol = None
        self.__extract_rules()
        self.__init_transition_diagrams()

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

    def __extract_rules(self):
        rule_pattern = re.compile(r'(\w+)\s*->\s*(.*)')
        rules_matched = rule_pattern.findall(self.cfg)
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
                start_state.transitions.append(
                    self.__get_transition(diagram_next_state, rhs[0]))

        return self.transition_diagrams_by_name[self.start_symbol]
