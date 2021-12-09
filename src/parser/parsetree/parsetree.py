class ParseTreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.parent = None

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def __repr__(self):
        return self.value + '\n\t' + '\n\t'.join([repr(child) for child in self.children])


class ParseTree:
    def __init__(self, root):
        self.root = root

    def __repr__(self):
        return self.root.__repr__()
