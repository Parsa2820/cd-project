class SemanticError(Exception):
    def __init__(self, message, is_illegal_type=False):
        self.message = message
        self.line = -1
        self.is_illegal_type = is_illegal_type

    def __str__(self):
        return f'#{self.line} : Semantic Error! {self.message}.'