from parser.auxiliaryset import Follow, First
from parser.cfgutils.fileconverter import FileConverter
from parser.parsetree.parsetree import ParseTree, ParseTreeNode
from parser.transitiondiagram import *
from parser.cfgutils.converter import CfgToTransitionDiagramConverter


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
        return parse_tree, TransitionDiagram.errors


class FileCfgParser(ParserBase):
    def __init__(self, scanner, base_path):
        self.base_path = base_path
        super().__init__(scanner, self.__grammar_setter)

    def __grammar_setter(self):
        start_diagram = FileConverter(self.base_path).get_grammar_diagram()
        self.start_symbol_name = start_diagram.name
        self.start_symbol_transition_diagram = start_diagram
