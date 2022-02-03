from intercodegen.intercodeutils.tac import DirectAddress, ImmediateAddress, IndirectAddress, Instruction, ThreeAddressCode
from intercodegen.intercodeutils.regcon import RegisterConstants


class ProgramBlock:
    def __init__(self):
        self.program_block = [None, None]
        self.last = RegisterConstants.PB_START
        self.stack_pointer_indirect = IndirectAddress(
            RegisterConstants.STACK_POINTER)
        self.stack_pointer_direct = DirectAddress(
            RegisterConstants.STACK_POINTER)
        self.byte_size = ImmediateAddress(RegisterConstants.BYTE_SIZE)
        self.neg_byte_size = ImmediateAddress(-RegisterConstants.BYTE_SIZE)
        self.__init_stack_pointer()

    def __init_stack_pointer(self):
        tac = ThreeAddressCode(Instruction.ASSIGN,
                               ImmediateAddress(RegisterConstants.STACK_START),
                               self.stack_pointer_direct,)
        self.set(RegisterConstants.STACK_POINTER_INIT, tac)

    def set(self, i, threeAddressCode: ThreeAddressCode):
        self.program_block[i] = threeAddressCode

    def increment(self):
        self.last += 1

    def set_current_and_increment(self, threeAddressCode):
        self.program_block.append(None)
        self.set(self.last, threeAddressCode)
        self.increment()

    def get_current_address(self):
        return self.last

    def __str__(self):
        return '\n'.join([f'{ln}\t{tac}' for ln, tac in enumerate(self.program_block)])

    def push_to_runtime_stack(self, addr):
        tac = ThreeAddressCode(Instruction.ASSIGN, addr,
                               self.stack_pointer_indirect)
        self.set_current_and_increment(tac)
        tac = ThreeAddressCode(
            Instruction.ADD, self.stack_pointer_direct, self.byte_size)
        self.set_current_and_increment(tac)

    def pop_from_runtime_stack(self, addr):
        tac = ThreeAddressCode(
            Instruction.ADD, self.stack_pointer_direct, self.neg_byte_size)
        self.set_current_and_increment(tac)
        tac = ThreeAddressCode(
            Instruction.ASSIGN, self.stack_pointer_indirect, addr)
        self.set_current_and_increment(tac)

    def bulk_push_direct(self, start_addr, size):
        for i in range(size):
            step = RegisterConstants.BYTE_SIZE * i
            addr = DirectAddress(start_addr + step)
            self.push_to_runtime_stack(addr)

    def bulk_pop_direct(self, start_addr, size):
        for i in reversed(range(size)):
            step = RegisterConstants.BYTE_SIZE * i
            addr = DirectAddress(start_addr + step)
            self.pop_from_runtime_stack(addr)
