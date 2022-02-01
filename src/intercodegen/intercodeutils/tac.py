import enum


class Instruction(enum.Enum):
    ADD = 1
    MULT = 2
    SUB = 3
    EQ = 4
    LT = 5
    ASSIGN = 6
    JPF = 7
    JP = 8
    PRINT = 9

    def __str__(self):
        return self.name


class Address:
    def __init__(self, value):
        self.value = value


class DirectAddress(Address):
    def __str__(self):
        return f'{self.value}'


class IndirectAddress(Address):
    def __str__(self):
        return f'@{self.value}'


class ImmediateAddress(Address):
    def __str__(self):
        return f'#{self.value}'


class ThreeAddressCode:
    def __init__(self, instruction: Instruction, addr1: Address, addr2: Address = None, addr3: Address = None):
        self.instruction = instruction
        self.addr1 = addr1
        self.addr2 = addr2
        self.addr3 = addr3

    def __str__(self):
        addr2 = '' if self.addr2 is None else f'{self.addr2}'
        addr3 = '' if self.addr3 is None else f'{self.addr3}'
        return f'({self.instruction}, {self.addr1}, {addr2}, {addr3})'
