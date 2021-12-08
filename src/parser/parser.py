from .parsetree.adopter import ParseTreeAdopter
from .transitiondiagram import *
import anytree
from anytree import RenderTree
import transitiondiagram


class Parser:
    def __init__(self, scanner):
        TransitionDiagram.scanner = scanner
        TransitionDiagram.current_token = scanner.get_next_token()
        program = Parser.__program_transition_diagram()

    @staticmethod
    def __program_transition_diagram():
        states = []
        state2 = State(2, [], True)
        states.append(state2)
        state1 = State(1, [TerminalTransition(state2, Token(TokenType.SYMBOL, '$'))])
        states.append(state1)
        # state0 =
        states.append()
        states.append(State(0, []))
        return None


class ParserTest:
    def __init__(self, scanner):
        TransitionDiagram.scanner = scanner
        TransitionDiagram.current_token = scanner.get_next_token()
        tstates = []
        state3 = State(3, [], True)
        tstates.append(state3)
        state2 = State(2, [])
        tstates.append(state2)
        state1 = State(1, [TerminalTransition(state2, Token(TokenType.SYMBOL, '*'))])
        tstates.append(state1)
        transitions = []
        transitions.append(TerminalTransition(state3, Token(TokenType.NUM, '')))
        state5 = State(5, [TerminalTransition(state3, Token(TokenType.SYMBOL, ')'))])
        state4 = State(4, [])
        transitions.append(state4, TerminalTransition(state4, Token(TokenType.NUM, '')))
        state0 = State(0, transitions)
        tstates.extend([state5, state0, state4])
        firstE = First([Token(TokenType.SYMBOL, '('), Token(TokenType.KEYWORD, 'int')])
        firstT = First([Token(TokenType.SYMBOL, '('), Token(TokenType.KEYWORD, 'int')])
        followE = Follow([Token(TokenType.SYMBOL, ')'), Token(TokenType.SYMBOL, '$')])
        followT = Follow([Token(TokenType.SYMBOL, ')'), Token(TokenType.SYMBOL, '$'), Token(TokenType.SYMBOL, '+')])
        t_transition_diagram = TransitionDiagram(state0, firstT, followT, 'T')
        state2.transitions.append(NonTerminalTransition(state3, t_transition_diagram))
        estate3 = State(3, [], True)
        estate2 = State(2, [], )
        estate1 = State(1, [TerminalTransition(estate2, Token(TokenType.SYMBOL, '+'))])
        etransitions = []
        etransitions.append(NonTerminalTransition(estate1, t_transition_diagram))
        etransitions.append(NonTerminalTransition(estate3, t_transition_diagram))
        estate0 = State(0, etransitions)
        e_transition_diagram = TransitionDiagram(estate0, firstE, followE, 'E')
        state4.transitions.append(NonTerminalTransition(state5, e_transition_diagram))
        estate2.transitions.append(NonTerminalTransition(estate3, e_transition_diagram))
        dickol = ParseTreeNode('E')
        e_transition_diagram.parse(dickol)
        print(RenderTree(ParseTreeAdopter(ParseTree(dickol)), style=anytree.AsciiStyle()))
