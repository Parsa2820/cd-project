import re
from parser.auxiliaryset import First, Follow
from parser.transitiondiagram import EpsilonTransition, NonTerminalTransition, State, TerminalTransition, TransitionDiagram
from share.token import Token, TokenType
from intercode.codegen import CodeGenerator


class CfgToTransitionDiagramConverter:
    AUX_SET_PATTERN = re.compile(r'([^\s]+)\s*(.*)')
    AUX_SET_SEPARATOR = r'\s*@\s*'
    RULES_PATTERN = re.compile(r'([^\s]+)\s*->\s*(.*)')

    def __init__(self, cfg, firsts_string, follows_string):
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
            for x in re.split(CfgToTransitionDiagramConverter.AUX_SET_SEPARATOR, value):
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
                [self.__terminal_to_token(x) for x in re.split(CfgToTransitionDiagramConverter.AUX_SET_SEPARATOR, value)])

    def __extract_rhs(self, rhs_string):
        single = [x.strip() for x in re.split(r'\s*\|\s*', rhs_string)]
        return [re.split(r'\s+', s) for s in single]

    def __get_number_of_states(self, rhs_list):
        x = 2
        for rhs in rhs_list:
            x += len([item for item in rhs if not self.__is_action_symbol(item)]) - 1
        return x

    def __terminal_to_token(self, terminal):
        if terminal in ['$', ';', '[', ']', '(', ')', '{', '}', '<', '==', '+', '-', '*', ',', '=']:
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
        rule_pattern = CfgToTransitionDiagramConverter.RULES_PATTERN
        rules_matched = rule_pattern.findall(cfg)
        for lhs, rhs_list in rules_matched:
            self.rules[lhs] = self.__extract_rhs(rhs_list)

    def __init_transition_diagrams(self):
        for lhs in self.rules.keys():
            self.transition_diagrams_by_name[lhs] = TransitionDiagram(
                None, self.firsts[lhs], self.follows[lhs], lhs)
            if self.start_symbol is None:
                self.start_symbol = lhs

    def __is_action_symbol(self, symbol):
        return symbol.startswith('#')

    def get_grammar_diagram(self):
        for lhs, rhs_list in self.rules.items():
            number_of_states = self.__get_number_of_states(rhs_list)
            start_state = State(0, [])
            final_state = State(number_of_states-1, [], True)
            self.transition_diagrams_by_name[lhs].init_state = start_state
            for rhs in reversed(rhs_list):
                diagram_next_state = final_state
                starts_with_action_symbol = self.__is_action_symbol(rhs[0])
                first_non_action_symbol_index = 1 if starts_with_action_symbol else 0
                for symbol in reversed(rhs[first_non_action_symbol_index+1:]):
                    if self.__is_action_symbol(symbol):
                        diagram_next_state.transitions[0].semantic_action = CodeGenerator.get_semantic_action(symbol)
                        continue
                    diagram_next_state = self.__get_state(diagram_next_state, symbol)
                start_state_transition = self.__get_transition(diagram_next_state, rhs[first_non_action_symbol_index])
                if starts_with_action_symbol:
                    start_state_transition.semantic_action = CodeGenerator.get_semantic_action(rhs[0])
                start_state.transitions.insert(0, start_state_transition)

        return self.transition_diagrams_by_name[self.start_symbol]
