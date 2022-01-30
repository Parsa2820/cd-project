class CodeGenerator:
    
    semantic_stack = []

    def get_semantic_action(action_symbol):
        action_symbol = action_symbol[1:]
        # return getattr(CodeGenerator, action_symbol)
        return CodeGenerator.pushIdDec

    def pushIdDec(token, symbol_table):
        symbol = symbol_table.get_symbol(token.value)
        # symbol.
        pass

    