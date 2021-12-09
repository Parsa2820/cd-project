from abc import abstractmethod
from .parsetree.adopter import ParseTreeAdopter
from .transitiondiagram import *
import anytree
from anytree import RenderTree
import parser.transitiondiagram


class ParserBase:
    def __init__(self, scanner):
        TransitionDiagram.scanner = scanner
        TransitionDiagram.current_token = scanner.get_next_token()
        self.start_symbol_name = None
        self.start_symbol_transition_diagram = None
        self.__set_grammar()

    def __set_grammar(self):
        pass

    def parse(self):
        root = anytree.Node(self.start_symbol_name)
        parse_tree = ParseTree(root)
        self.start_symbol_transition_diagram.parse(root)
        return parse_tree


class SimpleArithmeticParser(ParserBase):
    def __set_grammar(self):
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
        t0 = State(0, [TerminalTransition(t4, Token(TokenType.SYMBOL, '(')),
                   TerminalTransition(t4, Token(TokenType.KEYWORD, 'int'))])
        t.init_state = t0
        x2 = State(2, [], True)
        x1 = State(1, [NonTerminalTransition(x2, e)])
        x0 = State(0, [TerminalTransition(
            x2, Token(TokenType.SYMBOL, '+')), EpsilonTransition(x2)])
        x.init_state = x0
        y2 = State(2, [], True)
        y1 = State(1, [NonTerminalTransition(y2, t)])
        y0 = State(0, [TerminalTransition(
            y2, Token(TokenType.SYMBOL, '*')), EpsilonTransition(y2)])
        y.init_state = y0
        self.start_symbol_name = 'E'
        self.start_symbol_transition_diagram = e


class ParserTest:
    def __init__(self, scanner):
        TransitionDiagram.scanner = scanner
        TransitionDiagram.current_token = scanner.get_next_token()
        tstates = []
        state3 = State(3, [], True)
        tstates.append(state3)
        state2 = State(2, [])
        tstates.append(state2)
        state1 = State(1, [TerminalTransition(
            state2, Token(TokenType.SYMBOL, '*'))])
        tstates.append(state1)
        transitions = []
        transitions.append(TerminalTransition(
            state3, Token(TokenType.KEYWORD, 'int')))
        state5 = State(5, [TerminalTransition(
            state3, Token(TokenType.SYMBOL, ')'))])
        state4 = State(4, [])
        transitions.append(TerminalTransition(
            state4, Token(TokenType.KEYWORD, 'int')))
        state0 = State(0, transitions)
        tstates.extend([state5, state0, state4])
        firstE = First(
            [Token(TokenType.SYMBOL, '('), Token(TokenType.KEYWORD, 'int')])
        firstT = First(
            [Token(TokenType.SYMBOL, '('), Token(TokenType.KEYWORD, 'int')])
        followE = Follow([Token(TokenType.SYMBOL, ')'),
                         Token(TokenType.SYMBOL, '$')])
        followT = Follow([Token(TokenType.SYMBOL, ')'), Token(
            TokenType.SYMBOL, '$'), Token(TokenType.SYMBOL, '+')])
        t_transition_diagram = TransitionDiagram(state0, firstT, followT, 'T')
        state2.transitions.append(
            NonTerminalTransition(state3, t_transition_diagram))
        estate3 = State(3, [], True)
        estate2 = State(2, [], )
        estate1 = State(1, [TerminalTransition(
            estate2, Token(TokenType.SYMBOL, '+'))])
        etransitions = []
        etransitions.append(NonTerminalTransition(
            estate1, t_transition_diagram))
        etransitions.append(NonTerminalTransition(
            estate3, t_transition_diagram))
        estate0 = State(0, etransitions)
        e_transition_diagram = TransitionDiagram(estate0, firstE, followE, 'E')
        state4.transitions.append(
            NonTerminalTransition(state5, e_transition_diagram))
        estate2.transitions.append(
            NonTerminalTransition(estate3, e_transition_diagram))
        dickol = ParseTreeNode('E')
        e_transition_diagram.parse(dickol)
        print(RenderTree(ParseTreeAdopter(
            ParseTree(dickol)), style=anytree.AsciiStyle()))
