from .auxiliaryset import Follow, First
from .parsetree.parsetree import ParseTree, ParseTreeNode
from .transitiondiagram import *


class ParserBase:
    def __init__(self, scanner, grammar_setter):
        TransitionDiagram.scanner = scanner
        TransitionDiagram.current_token = scanner.get_next_token()
        self.start_symbol_name = None
        self.start_symbol_transition_diagram = None
        grammar_setter()

    def parse(self):
        root = ParseTreeNode(self.start_symbol_name)
        parse_tree = ParseTree(root)
        self.start_symbol_transition_diagram.parse(root)
        return parse_tree


class CMinusParser(ParserBase):
    dollar_terminal = Token(TokenType.SYMBOL , '$')
    ID_terminal = Token(TokenType.ID , '')
    semi_column_terminal = Token(TokenType.SYMBOL , ';')
    cr_open_terminal = Token(TokenType.SYMBOL , '[')
    cr_close_terminal = Token(TokenType.SYMBOL, ']')
    pr_open_terminal = Token(TokenType.SYMBOL , '(')
    pr_close_terminal = Token(TokenType.SYMBOL , ')')
    NUM_terminal = Token(TokenType.NUM ,'')
    int_terminal = Token(TokenType.KEYWORD , 'int')
    void_terminal = Token(TokenType.KEYWORD, 'void')
    comma_terminal = Token(TokenType.SYMBOL , ',')
    bracket_open_terminal = Token(TokenType.SYMBOL , '{')
    bracket_close_terminal = Token(TokenType.SYMBOL , '}')
    break_terminal = Token(TokenType.KEYWORD , 'break')
    if_terminal = Token(TokenType.KEYWORD , 'if')
    end_if_terminal = Token(TokenType.KEYWORD , 'endif')
    else_terminal = Token(TokenType.KEYWORD , 'else')
    repeat_terminal = Token(TokenType.KEYWORD, 'repeat')
    until_terminal = Token(TokenType.KEYWORD , 'until')
    return_terminal = Token(TokenType.KEYWORD , 'return')
    assign_terminal = Token(TokenType.SYMBOL , '=')
    less_terminal = Token(TokenType.SYMBOL , '<')
    equal_terminal = Token(TokenType.SYMBOL , '==')
    plus_terminal = Token(TokenType.SYMBOL , '+')
    minus_terminal = Token(TokenType.SYMBOL, '-')
    mul_terminal = Token(TokenType.SYMBOL , '*')
    
    def __init__(self, scanner):
        super().__init__(scanner, self.__grammar_setter)

    def __grammar_setter(self):
        # IMPLEMENT ME
        pass
        # self.start_symbol_name = 'Program'
        # self.start_symbol_transition_diagram = program
    @staticmethod
    def __get_program():
        program =



class SimpleArithmeticParser(ParserBase):
    def __init__(self, scanner):
        super().__init__(scanner, self.__grammar_setter)

    def __grammar_setter(self):
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
