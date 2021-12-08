from anytree import Node as AnyTreeNode
from parser.parsetree.parsetree import ParseTree

class ParseTreeAdopter(AnyTreeNode):
    def __init__(self, parse_tree: ParseTree):
        super.__init__(parse_tree.root.value)
        ParseTreeAdopter.__adopt_children(self)

    def __adopt_children(parent: AnyTreeNode):
        for child in parent.children:
            child_node = AnyTreeNode(child.value, parent=parent)
            ParseTreeAdopter.__adopt_children(child_node)
