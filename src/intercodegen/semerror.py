class SemanticError(Exception):
    def __init__(self, message):
        self.message = message
        self.line = -1

    def __str__(self):
        return f'#{self.line} : Semantic Error! {self.message}.'