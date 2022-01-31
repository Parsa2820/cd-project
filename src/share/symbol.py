class Symbol:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.details = {}

    def __str__(self):
        return f'{self.id}.\t{self.name}'




class SymbolDetails:
    def __init__(self):
        self.address_by_scope = {}

    def add_to_scope(self, scope, address):
        self.address_by_scope.update({scope: address})

    def delete_from_scope(self, scope):
        self.address_by_scope.pop(scope)

class FunctionDetails(SymbolDetails):
    def __init__(self, params_count, params_types):
        self.params_count = params_count
        self.params_types = params_types


class VarDetails(SymbolDetails):
    def __init__(self, type):
        self.type = type
