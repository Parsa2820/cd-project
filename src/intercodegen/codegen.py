from share.symbol import Symbol, VarDetails, FunctionDetails
from intercodegen.intercodeutils.pb import ProgramBlock
from intercodegen.intercodeutils.tac import *
from intercodegen.memman import MemoryManager
from share.symboltable import SymbolTable
from share.token import Token, TokenType


class CodeGenerator:

    semantic_stack = []
    break_stacks = []
    size_by_type = {'int': 4, 'void': 0}
    symbol_table: SymbolTable = None
    program_block: ProgramBlock = None
    memory_manager: MemoryManager = None
    address = 0
    fun_id: Symbol = None

    def get_semantic_action(action_symbol):
        action_symbol = action_symbol[1:]
        try:
            return getattr(CodeGenerator, action_symbol)
        except AttributeError:
            raise Exception(f'Semantic action {action_symbol} not found.')

    def pushIdDec(token):
        symbol = CodeGenerator.symbol_table.get_symbol(token.value)
        CodeGenerator.semantic_stack.append(symbol)

    def single(token):
        symbol = CodeGenerator.semantic_stack.pop()
        type = CodeGenerator.semantic_stack.pop()
        varDetails = VarDetails(type)
        addr = 0
        if type == 'int':
            addr = CodeGenerator.memory_manager.get_address('int')
        else:
            # TODO: this is error, single should not be void
            pass
        varDetails.add_to_scope(
            CodeGenerator.memory_manager.scope, addr)
        symbol.set_detail(varDetails)

    def array(token):
        symbol = CodeGenerator.semantic_stack.pop()
        type = CodeGenerator.semantic_stack.pop()
        varDetails = VarDetails(type)
        symbol.set_detail(varDetails)
        addr = 0
        if type == 'int':
            addr = CodeGenerator.memory_manager.get_address('int', token.value)
        else:
            # TODO: this is error, array should not be void
            pass
        varDetails.add_to_scope(
            CodeGenerator.memory_manager.scope, addr)

    def funDef(token):
        symbol = CodeGenerator.semantic_stack.pop()
        type = CodeGenerator.semantic_stack.pop()
        functionDetails = FunctionDetails(type)
        scope = CodeGenerator.memory_manager.scope
        address = CodeGenerator.memory_manager.get_address()
        functionDetails.add_to_scope(scope, address)
        symbol.detail = functionDetails
        CodeGenerator.semantic_stack.append(symbol)

    def lastParam(token):
        CodeGenerator.incrementParamCounter(token)
        pb_addr = CodeGenerator.program_block.get_current_address()
        add1 = ImmediateAddress(pb_addr + 1)  # +1 for assign instruction
        add2 = DirectAddress(CodeGenerator.address)
        tac = ThreeAddressCode(Instruction.ASSIGN, add1, add2)
        CodeGenerator.program_block.set_current_and_increment(tac)
        CodeGenerator.address += CodeGenerator.size_by_type['int']

    def pushIdTypeInt(token):
        CodeGenerator.semantic_stack.append('int')

    def pushIdTypeVoid(token):
        CodeGenerator.semantic_stack.append('void')

    def incrementParamCounter(token):
        likely_param_id = CodeGenerator.semantic_stack.pop()
        if likely_param_id == 'void':
            return
        param_type = CodeGenerator.semantic_stack.pop()
        function_symbol = CodeGenerator.semantic_stack.pop()
        function_symbol.detail.add_param(param_type, likely_param_id)
        CodeGenerator.semantic_stack.append(function_symbol)

    def noParam(token):
        CodeGenerator.semantic_stack.append('void')

    def paramArr(token):
        symbol = CodeGenerator.semantic_stack.pop()
        CodeGenerator.semantic_stack.append('arr')
        CodeGenerator.semantic_stack.append(symbol)

    def funEnd(token):
        pass

    def breakLoop(token):
        empty_address = CodeGenerator.program_block.get_current_address()
        CodeGenerator.program_block.set_current_and_increment(None)
        CodeGenerator.break_stacks[-1].append(empty_address)

    def saveEmptyAddr(token):
        empty_address = CodeGenerator.program_block.get_current_address()
        CodeGenerator.program_block.set_current_and_increment(None)
        CodeGenerator.semantic_stack.append(empty_address)

    def writeJmpFalseSavedAddr(token):
        predicate = CodeGenerator.semantic_stack.pop()
        saved_address = CodeGenerator.semantic_stack.pop()
        current_address = CodeGenerator.program_block.get_current_address()
        tac = ThreeAddressCode(Instruction.JPF, predicate, current_address)
        CodeGenerator.program_block.set(saved_address, tac)

    def writeJmpFalseSavedAddrSaveEmptyAddr(token):
        CodeGenerator.writeJmpFalseSavedAddr(token)
        CodeGenerator.saveEmptyAddr(token)

    def writeJmpSavedAddr(token):
        saved_address = CodeGenerator.semantic_stack.pop()
        current_address = CodeGenerator.program_block.get_current_address()
        tac = ThreeAddressCode(Instruction.JP, current_address)
        CodeGenerator.program_block.set(saved_address, tac)

    def saveAddrLoop(token):
        address = CodeGenerator.program_block.get_current_address()
        CodeGenerator.semantic_stack.append(address)
        CodeGenerator.break_stacks.append([])

    def jmpFalseSavedAddrLoop(token):
        predicate = CodeGenerator.semantic_stack.pop()
        address = CodeGenerator.semantic_stack.pop()
        tac = ThreeAddressCode(Instruction.JPF, predicate, address)
        CodeGenerator.program_block.set_current_and_increment(tac)
        current_address = CodeGenerator.program_block.get_current_address()
        break_tac = ThreeAddressCode(Instruction.JP, current_address)
        for break_address in CodeGenerator.break_stacks[-1]:
            CodeGenerator.program_block.set(break_address, break_tac)

    def returnVoid(token, ):
        rhs = CodeGenerator.memory_manager.return_address_by_scope[-1]
        lhs = 0
        tac = ThreeAddressCode(Instruction.ASSIGN, rhs, lhs)
        CodeGenerator.program_block.set_current_and_increment(tac)
        tac = ThreeAddressCode(Instruction.JP, 0,)
        CodeGenerator.program_block.set_current_and_increment(tac)

    def returnNonVoid(token, ):
        rhs = CodeGenerator.memory_manager.return_address_by_scope[-1]
        lhs = 0
        tac = ThreeAddressCode(Instruction.ASSIGN, rhs, lhs)
        CodeGenerator.program_block.set_current_and_increment(tac)
        tac = ThreeAddressCode(Instruction.JP, 0,)
        CodeGenerator.program_block.set_current_and_increment(tac)

    def assign(token):
        rhs = CodeGenerator.semantic_stack.pop()
        lhs = CodeGenerator.semantic_stack.pop()
        tac = ThreeAddressCode(Instruction.ASSIGN, rhs, lhs)
        CodeGenerator.program_block.set_current_and_increment(tac)

    def arrayIndex(token):
        pass

    def apply():
        second_operand = CodeGenerator.semantic_stack.pop()
        instruction = CodeGenerator.semantic_stack.pop()
        first_operand = CodeGenerator.semantic_stack.pop()
        result_tmp = CodeGenerator.memory_manager.get_address()
        tac = ThreeAddressCode(instruction, first_operand,
                               second_operand, result_tmp)
        CodeGenerator.program_block.set_current_and_increment(tac)
        CodeGenerator.semantic_stack.append(result_tmp)

    def compare(token):
        CodeGenerator.apply()

    def lessthan(token):
        CodeGenerator.semantic_stack.append(Instruction.LT)

    def equal(token):
        CodeGenerator.semantic_stack.append(Instruction.EQ)

    def add(token):
        CodeGenerator.apply()

    def plus(token):
        CodeGenerator.semantic_stack.append(Instruction.ADD)

    def minus(token):
        CodeGenerator.semantic_stack.append(Instruction.SUB)

    def multiply(token):
        second_operand = CodeGenerator.semantic_stack.pop()
        instruction = Instruction.MULT
        CodeGenerator.semantic_stack.append(instruction)
        CodeGenerator.semantic_stack.append(second_operand)
        CodeGenerator.apply()

    def pushNum(token):
        CodeGenerator.semantic_stack.append(ImmediateAddress(token.value))

    def pushId(token):
        symbol = CodeGenerator.symbol_table.get_symbol(token.value)
        global_scope = 0
        symbol_address = 0
        if CodeGenerator.memory_manager.scope in symbol.detail.address_by_scope:
            symbol_address = symbol.detail.address_by_scope[CodeGenerator.memory_manager.scope]
        else:
            symbol_address = symbol.detail.address_by_scope[global_scope]
        # TODO id not found semantic error should be implemented
        CodeGenerator.semantic_stack.append(symbol_address)
        CodeGenerator.fun_id = symbol

    def call(token):
        CodeGenerator.memory_manager.add_scope()
        param_count = CodeGenerator.fun_id.details.params_count()
        arg_val_list = []
        for i in range(0, param_count):
            arg_val = CodeGenerator.semantic_stack.pop()
            arg_val_list.append(arg_val)
        arg_val_list.reverse()
        CodeGenerator.define_params(CodeGenerator.fun_id, arg_val_list)
        CodeGenerator.set_pb_pointer(CodeGenerator.fun_id)

    def define_params(func: Symbol, values):
        for index, param in enumerate(func.details.param):
            # TODO check param and input type
            cur_address = CodeGenerator.memory_manager.get_address('int')
            if param[0] == 'int':
                rhs = DirectAddress(values[index])
            else:
                rhs = ImmediateAddress(values[index])
            lhs = DirectAddress(cur_address)
            tac = ThreeAddressCode(Instruction.ASSIGN, rhs, lhs)
            CodeGenerator.program_block.set_current_and_increment(tac)
            CodeGenerator.add_address_to_symbol(
                param[1], CodeGenerator.memory_manager.scope, cur_address)

    def add_address_to_symbol(symbol: Symbol, scope, adrress):
        if symbol.detail is None:
            symbol.set_detail(VarDetails('int'))
        symbol.detail.add_to_scope(scope, adrress)

    def set_pb_pointer(func: Symbol):
        func_address = func.details.address_by_scope[0][1]
        rhs = IndirectAddress(func_address)
        tac = ThreeAddressCode(Instruction.JP, rhs,)
        CodeGenerator.program_block.set_current_and_increment(tac)
        ret_addr = CodeGenerator.program_block.get_current_address()
        CodeGenerator.memory_manager.add_return_address(ret_addr)

    def initialize_output_function():
        function_name = 'output'
        input_name = '@x'
        CodeGenerator.symbol_table.extend(function_name)
        CodeGenerator.pushIdTypeVoid(None)
        CodeGenerator.pushIdDec(Token(TokenType.ID, function_name))
        CodeGenerator.funDef(None)
        CodeGenerator.pushIdTypeInt(None)
        CodeGenerator.pushIdDec(Token(TokenType.ID, input_name))
        CodeGenerator.lastParam(None)
        CodeGenerator.pushId(Token(TokenType.ID, input_name))
        input = CodeGenerator.semantic_stack.pop()
        tac = ThreeAddressCode(Instruction.PRINT, input)
        CodeGenerator.program_block.set_current_and_increment(tac)
        CodeGenerator.funEnd()