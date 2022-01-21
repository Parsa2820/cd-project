class SemanticAction:
    def get_semantic_action(action_symbol):
        action_symbol = action_symbol[1:].lower()
        return getattr(SemanticAction, action_symbol)
