class ThreeAddressCode:
    def __init__(self, op, addr1, addr2, addr3):
        self.op = op
        self.addr1 = addr1
        self.addr2 = addr2
        self.addr3 = addr3


class ProgramBlock:
    def __init__(self):
        self.program_block = []
        self.last = 0

    def set(self, i, threeAddressCode: ThreeAddressCode):
        self.program_block[i] = threeAddressCode

    def increment(self):
        self.last += 1

    def get_current(self):
        return self.last
