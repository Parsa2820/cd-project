class MemoryManager:
    DATA_START_ADDRESS = 500
    SIZE_BY_TYPE = {'int': 4, 'void': 0}

    def __init__(self):
        self.address = MemoryManager.DATA_START_ADDRESS
        # self.offset = 0
        self.current_function_record_id = 0
        self.last_function_record_id = 0
        # self.scope_size_stack = []
        # self.return_address = []

    def get_address(self, type='int', size=1):
        address = self.address
        self.address += MemoryManager.SIZE_BY_TYPE[type] * size
        return address

    def add_scope(self):
        self.current_function_record_id = self.last_function_record_id + 1
        self.last_function_record_id += 1

    def remove_scope(self):
        # self.offset = self.scope_size_stack.pop()
        # self.address -= self.offset
        self.current_function_record_id = 0


    # def add_return_address(self, return_address):
    #     self.return_address_by_scope.append(return_address)
