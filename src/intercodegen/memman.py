from intercodegen.scope import Scope


class MemoryManager:
    DATA_START_ADDRESS = 500
    SIZE_BY_TYPE = {'int': 4, 'void': 0}

    def __init__(self):
        self.address = MemoryManager.DATA_START_ADDRESS
        self.offset = 0
        self.scope = 0
        self.scope_size_stack = []
        self.return_address = []

    def get_address(self, type='int', size = 1):
        address = self.address + self.offset
        self.offset += MemoryManager.SIZE_BY_TYPE[type] * size
        return address

    def add_scope(self):
        self.scope += 1
        self.scope_size_stack.append(self.offset)
        self.address += self.offset
        self.offset = 0

    def remove_scope(self):
        self.offset = self.scope_size_stack.pop()
        self.address -= self.offset
        self.scope -= 1
    
    def add_return_address(self, return_address):
        self.return_address_by_scope.append(return_address)

        


