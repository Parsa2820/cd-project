from anytree import Node as AnyTreeNode
from parser.parsetree.parsetree import ParseTree, ParseTreeNode

class ParseTreeAdopter:
    def __init__(self, parse_tree: ParseTree):
        self.anytree_root = AnyTreeNode(parse_tree.root.value)
        ParseTreeAdopter.__adopt_children(parse_tree.root, self.anytree_root)

    def __adopt_children(parse_tree_parent: ParseTreeNode, anytree_parent: AnyTreeNode):
        for child in parse_tree_parent.children:
            anytree_child_node = AnyTreeNode(child.value, parent=anytree_parent)
            ParseTreeAdopter.__adopt_children(child, anytree_child_node)
