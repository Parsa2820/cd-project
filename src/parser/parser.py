from parser.auxiliaryset import Follow, First
from parser.cfgutils.fileconverter import FileConverter
from parser.parsetree.parsetree import ParseTree, ParseTreeNode
from parser.transitiondiagram import *
from parser.cfgutils.converter import CfgToTransitionDiagramConverter

dollar_terminal = Token(TokenType.SYMBOL, '$')
ID_terminal = Token(TokenType.ID, '')
semi_column_terminal = Token(TokenType.SYMBOL, ';')
bracket_open_terminal = Token(TokenType.SYMBOL, '[')
bracket_close_terminal = Token(TokenType.SYMBOL, ']')
pr_open_terminal = Token(TokenType.SYMBOL, '(')
pr_close_terminal = Token(TokenType.SYMBOL, ')')
NUM_terminal = Token(TokenType.NUM, '')
int_terminal = Token(TokenType.KEYWORD, 'int')
void_terminal = Token(TokenType.KEYWORD, 'void')
comma_terminal = Token(TokenType.SYMBOL, ',')
cr_open_terminal = Token(TokenType.SYMBOL, '{')
cr_close_terminal = Token(TokenType.SYMBOL, '}')
break_terminal = Token(TokenType.KEYWORD, 'break')
if_terminal = Token(TokenType.KEYWORD, 'if')
end_if_terminal = Token(TokenType.KEYWORD, 'endif')
else_terminal = Token(TokenType.KEYWORD, 'else')
repeat_terminal = Token(TokenType.KEYWORD, 'repeat')
until_terminal = Token(TokenType.KEYWORD, 'until')
return_terminal = Token(TokenType.KEYWORD, 'return')
assign_terminal = Token(TokenType.SYMBOL, '=')
less_terminal = Token(TokenType.SYMBOL, '<')
equal_terminal = Token(TokenType.SYMBOL, '==')
plus_terminal = Token(TokenType.SYMBOL, '+')
minus_terminal = Token(TokenType.SYMBOL, '-')
mul_terminal = Token(TokenType.SYMBOL, '*')


class ParserBase:
    def __init__(self, scanner, grammar_setter):
        TransitionDiagram.scanner = scanner
        TransitionDiagram.update_current_token()
        self.start_symbol_name = None
        self.start_symbol_transition_diagram = None
        grammar_setter()

    def parse(self):
        root = ParseTreeNode(self.start_symbol_name)
        parse_tree = ParseTree(root)
        self.start_symbol_transition_diagram.parse(root)
        return parse_tree


class CMinusParser(ParserBase):

    def __init__(self, scanner):
        super().__init__(scanner, self.__grammar_setter)

    def __grammar_setter(self):
        # IMPLEMENT ME
        pass
        # self.start_symbol_name = 'Program'
        # self.start_symbol_transition_diagram = program

    transition_diagrams = {''}

    @staticmethod
    def __get_program():
        program = TransitionDiagram(None, First([dollar_terminal, int_terminal, void_terminal]), Follow([]), 'PROGRAM')
        state2 = State(2, [], True)
        state1 = State(1, [TerminalTransition(state2, dollar_terminal)])
        state0 = State(0, [NonTerminalTransition(state1, CMinusParser.__get_declaration_list)])
        program.init_state = state0
        return program

    @staticmethod
    def __get_declaration_list():
        declaration_list = TransitionDiagram(None, First([int_terminal, void_terminal], True),
                                             Follow([dollar_terminal, ID_terminal,
                                                     semi_column_terminal, NUM_terminal, pr_open_terminal,
                                                     cr_open_terminal, cr_close_terminal, break_terminal, if_terminal,
                                                     repeat_terminal, return_terminal]), 'DECLARATION-LIST')
        state2 = State(2, [], True)
        state1 = State(1, [NonTerminalTransition(state2, declaration_list)])
        state0 = State(0,
                       [EpsilonTransition(state2), NonTerminalTransition(state1, CMinusParser.__get_declaration_list)])
        declaration_list.init_state = state0
        return declaration_list

    @staticmethod
    def __get_declaration():
        declaration = TransitionDiagram(None, First([int_terminal, void_terminal]),
                                        Follow([dollar_terminal, ID_terminal,
                                                semi_column_terminal, NUM_terminal, pr_open_terminal, int_terminal,
                                                void_terminal,
                                                cr_open_terminal, cr_close_terminal, break_terminal, if_terminal,
                                                repeat_terminal, return_terminal]), 'DECLARATION')
        state2 = State(2, [], True)
        state1 = State(1, [NonTerminalTransition(state2, CMinusParser.__get_declaration_prime)])
        state0 = State(0, [NonTerminalTransition(state1, CMinusParser.__get_declaration_initial)])
        declaration.init_state = state0
        return declaration

    @staticmethod
    def __get_declaration_initial():
        declaration_initial = TransitionDiagram(None, First([int_terminal, void_terminal]), Follow(
            [semi_column_terminal, bracket_open_terminal, pr_close_terminal, pr_open_terminal, comma_terminal]),
                                                'DECLARATION-INITIAL')
        state2 = State(2, [], True)
        state1 = State(1, [TerminalTransition(state2, ID_terminal)])
        state0 = State(0, [NonTerminalTransition(state1, CMinusParser.__get_type_specifier)])
        declaration_initial.init_state = state0
        return declaration_initial

    @staticmethod
    def __get_declaration_prime():
        declaration_prime = TransitionDiagram(None,
                                              First([semi_column_terminal, bracket_open_terminal, pr_open_terminal]),
                                              Follow([dollar_terminal, ID_terminal,
                                                      semi_column_terminal, NUM_terminal, pr_open_terminal,
                                                      int_terminal,
                                                      void_terminal,
                                                      cr_open_terminal, cr_close_terminal, break_terminal, if_terminal,
                                                      repeat_terminal, return_terminal]), 'DECLARATION-PRIME')

        state1 = State(1, [], True)
        state0 = State(0, [NonTerminalTransition(state1, CMinusParser.__get_fun_declaration_prime),
                           NonTerminalTransition(state1, CMinusParser.__get_var_declaration_prime)])
        declaration_prime.init_state = state0
        return declaration_prime

    @staticmethod
    def __get_type_specifier():
        type_specifier = TransitionDiagram(None, First([int_terminal, void_terminal]), Follow([ID_terminal]),
                                           'Type-Specifier')
        state1 = State(1, [], True)
        state0 = State(0, [TerminalTransition(state1, int_terminal), TerminalTransition(state1, void_terminal)])
        type_specifier.init_state = state0
        return type_specifier

    @staticmethod
    def __get_var_declaration_prime():
        var_declaration_prime = TransitionDiagram(None, First([semi_column_terminal, bracket_open_terminal]),
                                                  Follow([dollar_terminal, ID_terminal,
                                                          semi_column_terminal, NUM_terminal, pr_open_terminal,
                                                          int_terminal,
                                                          void_terminal,
                                                          cr_open_terminal, cr_close_terminal, break_terminal,
                                                          if_terminal,
                                                          repeat_terminal, return_terminal]), 'VAR-DECLARATION-PRIME')
        state4 = State(4, [], True)
        state3 = State(3, [TerminalTransition(state4, semi_column_terminal)])
        state2 = State(2, [TerminalTransition(state3, bracket_close_terminal)])
        state1 = State(1, [TerminalTransition(state2, NUM_terminal)])
        state0 = State(0, [TerminalTransition(state1, bracket_open_terminal),
                           TerminalTransition(state4, semi_column_terminal)])
        var_declaration_prime.init_state = state0
        return var_declaration_prime

    @staticmethod
    def __get_fun_declaration_prime():
        fun_declaration_prime = TransitionDiagram(None, First([pr_open_terminal]), Follow([dollar_terminal, ID_terminal,
                                                                                           semi_column_terminal,
                                                                                           NUM_terminal,
                                                                                           pr_open_terminal,
                                                                                           int_terminal,
                                                                                           void_terminal,
                                                                                           cr_open_terminal,
                                                                                           cr_close_terminal,
                                                                                           break_terminal,
                                                                                           if_terminal,
                                                                                           repeat_terminal,
                                                                                           return_terminal]),
                                                  'FUN-DECLARATION-PRIME')
        state4 = State(4, [], True)
        state3 = State(3, [NonTerminalTransition(state4, CMinusParser.__get_compound_stmt)])
        state2 = State(2, [TerminalTransition(state3, pr_close_terminal)])
        state1 = State(1, [NonTerminalTransition(state2, CMinusParser.__get_params)])
        state0 = State(0, [TerminalTransition(state1, pr_open_terminal)])
        fun_declaration_prime.init_state = state0
        return fun_declaration_prime

    @staticmethod
    def __get_params():
        params = TransitionDiagram(None, First([int_terminal, void_terminal]), Follow([pr_close_terminal]), 'PARAMS')
        state4 = State(4, [], True)
        state3 = State(3, [NonTerminalTransition(state4, CMinusParser.__get_params_list)])
        state2 = State(2, [NonTerminalTransition(state3, CMinusParser.__get_param_prime)])
        state1 = State(1, [TerminalTransition(state2, ID_terminal)])
        state0 = State(0, [TerminalTransition(state1, int_terminal), TerminalTransition(state4, void_terminal)])
        params.init_state = state0
        return params

    @staticmethod
    def __get_params_list():
        params_list = TransitionDiagram(None, First([comma_terminal], True), Follow([pr_close_terminal]), 'PARAM-LIST')
        state3 = State(3, [], True)
        state2 = State(2, [NonTerminalTransition(state3, params_list)])
        state1 = State(1, [NonTerminalTransition(state2, CMinusParser.__get_param)])
        state0 = State(0, [TerminalTransition(state1, comma_terminal), EpsilonTransition(state2)])
        params_list.init_state = state0
        return params_list

    @staticmethod
    def __get_param():
        param = TransitionDiagram(None, First([int_terminal, void_terminal]),
                                  Follow([pr_close_terminal, comma_terminal]), 'PARAM')
        return param

    @staticmethod
    def __get_param_prime():
        param_prime = TransitionDiagram(None, First([bracket_open_terminal], True),
                                        Follow([comma_terminal, pr_close_terminal]), 'PARAM-PRIME')
        state2 = State(2, [], True)
        state1 = State(1, [TerminalTransition(state2, bracket_close_terminal)])
        state0 = State(0, [TerminalTransition(state1, bracket_open_terminal), EpsilonTransition(state2)])
        param_prime.init_state = state0
        return param_prime

    @staticmethod
    def __get_compound_stmt():
        compound_stmt = TransitionDiagram(None, First([cr_open_terminal]), Follow(
            [dollar_terminal, ID_terminal, semi_column_terminal, NUM_terminal, pr_open_terminal, int_terminal,
             void_terminal, cr_open_terminal, cr_close_terminal, break_terminal, if_terminal, end_if_terminal,
             else_terminal, repeat_terminal, until_terminal, return_terminal], 'COMPOUND-STMT'))
        return compound_stmt


class SimpleArithmeticParser(ParserBase):
    def __init__(self, scanner):
        super().__init__(scanner, self.__grammar_setter)

    def __grammar_setter(self):
        d:TransitionDiagram = CfgToTransitionDiagramConverter('', '', '').get_grammar_diagram()
        self.start_symbol_name = d.name
        self.start_symbol_transition_diagram = d
        return
        e = TransitionDiagram(None,
                              First([Token(TokenType.KEYWORD, 'int'),
                                     Token(TokenType.SYMBOL, '(')]),
                              Follow([Token(TokenType.SYMBOL, ')'),
                                      Token(TokenType.SYMBOL, '$')]),
                              'E')
        t = TransitionDiagram(None,
                              First([Token(TokenType.KEYWORD, 'int'),
                                     Token(TokenType.SYMBOL, '(')]),
                              Follow([Token(
                                  TokenType.SYMBOL, '+'), Token(TokenType.SYMBOL, ')'), Token(TokenType.SYMBOL, '$')]),
                              'T')
        x = TransitionDiagram(None,
                              First([Token(TokenType.SYMBOL, '+')], True),
                              Follow([Token(TokenType.SYMBOL, ')'),
                                      Token(TokenType.SYMBOL, '$')]),
                              'X')
        y = TransitionDiagram(None,
                              First([Token(TokenType.SYMBOL, '*')], True),
                              Follow([Token(
                                  TokenType.SYMBOL, '+'), Token(TokenType.SYMBOL, ')'), Token(TokenType.SYMBOL, '$')]),
                              'Y')
        e2 = State(2, [], True)
        e1 = State(1, [NonTerminalTransition(e2, x)])
        e0 = State(0, [NonTerminalTransition(e1, t)])
        e.init_state = e0
        t4 = State(4, [], True)
        t3 = State(3, [NonTerminalTransition(t4, y)])
        t2 = State(2, [TerminalTransition(t4, Token(TokenType.SYMBOL, ')'))])
        t1 = State(1, [NonTerminalTransition(t2, e)])
        t0 = State(0, [TerminalTransition(t1, Token(TokenType.SYMBOL, '(')),
                       TerminalTransition(t3, Token(TokenType.KEYWORD, 'int'))])
        t.init_state = t0
        x2 = State(2, [], True)
        x1 = State(1, [NonTerminalTransition(x2, e)])
        x0 = State(0, [TerminalTransition(
            x1, Token(TokenType.SYMBOL, '+')), EpsilonTransition(x2)])
        x.init_state = x0
        y2 = State(2, [], True)
        y1 = State(1, [NonTerminalTransition(y2, t)])
        y0 = State(0, [TerminalTransition(
            y1, Token(TokenType.SYMBOL, '*')), EpsilonTransition(y2)])
        y.init_state = y0
        self.start_symbol_name = 'E'
        self.start_symbol_transition_diagram = e



class FileCfgParser(ParserBase):
    def __init__(self, scanner, base_path):
        self.base_path = base_path
        super().__init__(scanner, self.__grammar_setter)

    def __grammar_setter(self):
        start_diagram = FileConverter(self.base_path).get_grammar_diagram()
        self.start_symbol_name = start_diagram.name
        self.start_symbol_transition_diagram = start_diagram