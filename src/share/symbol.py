class Symbol:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.detail = None

    def __str__(self):
        if self.detail is not None:
            return f'{self.id}.\t{self.name}: {self.detail.__dict__}'
        return f'{self.id}.\t{self.name}'

    def set_detail(self, symbol_detail):
        self.detail = symbol_detail


class SymbolDetails:
    def __init__(self):
        self.address_by_scope = {}

    def add_to_scope(self, scope, address):
        self.address_by_scope.update({scope: address})

    def delete_from_scope(self, scope):
        self.address_by_scope.pop(scope)


class FunctionDetails(SymbolDetails):
    def __init__(self, return_type):
        super().__init__()
        self.return_type = return_type
        self.params_count = 0
        self.param = []
        self.local = []

    def add_param(self, param_type, param_symbol):
        self.param.append((param_type, param_symbol))
        self.params_count += 1

    def add_local(self, local_symbol):
        self.local.append(local_symbol)


class VarDetails(SymbolDetails):
    def __init__(self, type):
        super().__init__()
        self.type = type
