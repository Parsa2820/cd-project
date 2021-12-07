from parser.transitiondiagram import TransitionDiagram
import transitiondiagram

class Parser:
    def __init__(self, scanner):
        TransitionDiagram.scanner = scanner
        TransitionDiagram.current_token = scanner.get_next_token()
        