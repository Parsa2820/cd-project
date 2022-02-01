from intercodegen.intercodeutils.tac import ThreeAddressCode


class ProgramBlock:
    def __init__(self):
        self.program_block = []
        self.last = 0

    def set(self, i, threeAddressCode: ThreeAddressCode):
        self.program_block[i] = threeAddressCode

    def increment(self):
        self.last += 1

    def set_current_and_increment(self, threeAddressCode):
        self.set(self.last, threeAddressCode)
        self.increment()

    def get_current_address(self):
        return self.last

    def __str__(self):
        return '\n'.join([f'{ln}\t{tac}' for ln, tac in enumerate(self.program_block)])
