class PredictiveAuxiliarySet:
    def __init__(self, tokens):
        self.tokens = tokens

    def include(self, input_token):
        for token in self.tokens:
            if token.type != input_token.type:
                continue
            elif token.type == TokenType.KEYWORD or token.type == TokenType.SYMBOL:
                if token.value == input_token.value:
                    return True
            else:
                return True
        return False


class First(PredictiveAuxiliarySet):
    def __init__(self, tokens, has_epsilon):
        super().__init__(tokens)
        self.has_epsilon = has_epsilon


class Follow(PredictiveAuxiliarySet):
    pass
