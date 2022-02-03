from ast import Pass
from intercodegen.intercodeutils.regcon import RegisterConstants
from share.symbol import Symbol, VarDetails, FunctionDetails
from intercodegen.intercodeutils.pb import ProgramBlock
from intercodegen.intercodeutils.tac import *
from intercodegen.memman import MemoryManager
from share.symboltable import SymbolTable
from share.token import Token, TokenType


class CodeGenerator:
    RETURN_ADDRESS = IndirectAddress(RegisterConstants.RETURN_ADDRESS)
    RETURN_VALUE_ADDRESS = DirectAddress(RegisterConstants.RETURN_VALUE)

    semantic_stack = []
    break_stacks = []
    size_by_type = {'int': 4, 'void': 0}
    symbol_table: SymbolTable = None
    program_block: ProgramBlock = None
    memory_manager: MemoryManager = None
    fun_symbol: Symbol = None
    record_id_by_function_name = {}
    is_called_by_function_name = {}

    def initialize_output_function():
        function_name = 'output'
        input_name = '@x'
        CodeGenerator.symbol_table.extend(function_name)
        CodeGenerator.symbol_table.extend(input_name)
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
        CodeGenerator.returnVoid(None)
        CodeGenerator.funEnd(None)

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
            addr = CodeGenerator.memory_manager.get_address()
        else:
            # TODO: this is error, single should not be void
            pass
        varDetails.add_to_scope(
            CodeGenerator.memory_manager.current_function_record_id, addr)
        symbol.set_detail(varDetails)
        if CodeGenerator.fun_symbol != None:
            CodeGenerator.fun_symbol.detail.add_local(symbol)

    def array(token):
        symbol = CodeGenerator.semantic_stack.pop()
        type = CodeGenerator.semantic_stack.pop()
        varDetails = VarDetails(type)
        symbol.set_detail(varDetails)
        addr = 0
        if type == 'int':
            addr = CodeGenerator.memory_manager.get_address(size=int(token.value))
        else:
            # TODO: this is error, array should not be void
            pass
        varDetails.add_to_scope(
            CodeGenerator.memory_manager.current_function_record_id, addr)

    def funDef(token):
        symbol = CodeGenerator.semantic_stack.pop()
        CodeGenerator.__check_main(symbol)
        type = CodeGenerator.semantic_stack.pop()
        functionDetails = FunctionDetails(type)
        scope = CodeGenerator.memory_manager.current_function_record_id
        address = CodeGenerator.program_block.get_current_address()
        functionDetails.add_to_scope(scope, address)
        symbol.detail = functionDetails
        CodeGenerator.fun_symbol = symbol
        CodeGenerator.semantic_stack.append(symbol)
        CodeGenerator.memory_manager.add_scope()
        record_id = CodeGenerator.memory_manager.current_function_record_id
        CodeGenerator.record_id_by_function_name.update(
            {symbol.name: record_id})
        CodeGenerator.is_called_by_function_name.update({symbol.name: False})

    def __check_main(symbol):
        if symbol.name != 'main':
            return
        main_address = CodeGenerator.program_block.get_current_address()
        rhs = DirectAddress(main_address)
        tac = ThreeAddressCode(Instruction.JP, rhs)
        CodeGenerator.program_block.set(RegisterConstants.MAIN_JP, tac)

    def incrementParamCounter(token):
        likely_symbol = CodeGenerator.semantic_stack.pop()
        if likely_symbol == 'void':
            return
        param_type = CodeGenerator.semantic_stack.pop()
        function_symbol = CodeGenerator.semantic_stack.pop()
        function_symbol.detail.add_param(param_type, likely_symbol)
        if likely_symbol.detail is None:
            likely_symbol.detail = VarDetails(param_type)
        param_address = CodeGenerator.memory_manager.get_address()
        likely_symbol.detail.add_to_scope(
            CodeGenerator.memory_manager.current_function_record_id, param_address)
        CodeGenerator.semantic_stack.append(function_symbol)

    def lastParam(token):
        CodeGenerator.incrementParamCounter(token)
        # current_address = CodeGenerator.program_block.get_current_address()
        # addr1 = ImmediateAddress(current_address + 1)  # +1 for assign instruction
        # addr2 = DirectAddress(CodeGenerator.fun_symbol.detail.address_by_scope[0])
        # tac = ThreeAddressCode(Instruction.ASSIGN, addr1, addr2)
        # CodeGenerator.program_block.set_current_and_increment(tac)

    def pushIdTypeInt(token):
        CodeGenerator.semantic_stack.append('int')

    def pushIdTypeVoid(token):
        CodeGenerator.semantic_stack.append('void')

    def noParam(token):
        CodeGenerator.pushIdTypeVoid(token)

    def paramArr(token):
        symbol = CodeGenerator.semantic_stack.pop()
        CodeGenerator.semantic_stack.pop()
        CodeGenerator.semantic_stack.append('arr')
        CodeGenerator.semantic_stack.append(symbol)

    def funEnd(token):
        if CodeGenerator.fun_symbol == None:
            return
        CodeGenerator.memory_manager.remove_scope()
        CodeGenerator.fun_symbol = None

    def breakLoop(token):
        empty_address = CodeGenerator.program_block.get_current_address()
        CodeGenerator.program_block.set_current_and_increment(None)
        CodeGenerator.break_stacks[-1].append(empty_address)

    def saveEmptyAddr(token):
        empty_address = CodeGenerator.program_block.get_current_address()
        CodeGenerator.program_block.set_current_and_increment(None)
        CodeGenerator.semantic_stack.append(empty_address)

    def writeJmpFalseSavedAddr(token):
        saved_address = CodeGenerator.semantic_stack.pop()
        predicate = CodeGenerator.semantic_stack.pop()
        current_address = CodeGenerator.program_block.get_current_address()
        tac = ThreeAddressCode(Instruction.JPF, predicate, current_address + 1)
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

    def returnVoid(token):
        CodeGenerator.semantic_stack.append(ImmediateAddress(0))
        CodeGenerator.returnNonVoid(None)

    def returnNonVoid(token):
        return_value = CodeGenerator.semantic_stack.pop()
        tac = ThreeAddressCode(
            Instruction.ASSIGN, return_value, CodeGenerator.RETURN_VALUE_ADDRESS)
        CodeGenerator.program_block.set_current_and_increment(tac)
        tac = ThreeAddressCode(Instruction.JP, CodeGenerator.RETURN_ADDRESS)
        CodeGenerator.program_block.set_current_and_increment(tac)

    def assign(token):
        rhs = CodeGenerator.semantic_stack.pop()
        lhs = CodeGenerator.semantic_stack.pop()
        tac = ThreeAddressCode(Instruction.ASSIGN, rhs, lhs)
        CodeGenerator.program_block.set_current_and_increment(tac)
        CodeGenerator.semantic_stack.append(rhs)

    def arrayIndex(token):
        expression_address = CodeGenerator.semantic_stack.pop()
        symbol_address = CodeGenerator.semantic_stack.pop()
        op1 = ImmediateAddress(RegisterConstants.BYTE_SIZE)
        op2 = DirectAddress(expression_address)
        op3 = DirectAddress(CodeGenerator.memory_manager.get_address())
        tac = ThreeAddressCode(Instruction.MULT, op1, op2, op3)
        CodeGenerator.program_block.set_current_and_increment(tac)
        op1 = ImmediateAddress(symbol_address)
        tac = ThreeAddressCode(Instruction.ADD, op1, op3, op3)
        CodeGenerator.program_block.set_current_and_increment(tac)
        CodeGenerator.semantic_stack.append(IndirectAddress(op3))

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
        tmp = CodeGenerator.memory_manager.get_address()
        tac = ThreeAddressCode(Instruction.ASSIGN, ImmediateAddress(token.value), DirectAddress(tmp))
        CodeGenerator.program_block.set_current_and_increment(tac)
        CodeGenerator.semantic_stack.append(tmp)

    def pushId(token):
        symbol = CodeGenerator.symbol_table.get_symbol(token.value)
        global_scope = 0
        if CodeGenerator.memory_manager.current_function_record_id in symbol.detail.address_by_scope:
            symbol_address = symbol.detail.address_by_scope[
                CodeGenerator.memory_manager.current_function_record_id]
        else:
            symbol_address = symbol.detail.address_by_scope[global_scope]
        # TODO id not found semantic error should be implemented
        CodeGenerator.semantic_stack.append(symbol_address)
        if isinstance(symbol.detail, FunctionDetails):
            CodeGenerator.fun_symbol = symbol

    def call(token):
        CodeGenerator.__push_before_call(token)
        param_count = CodeGenerator.fun_symbol.detail.params_count
        arg_val_list = []
        for _ in range(0, param_count):
            arg_val = CodeGenerator.semantic_stack.pop()
            arg_val_list.insert(0, arg_val)
        CodeGenerator.semantic_stack.pop()
        CodeGenerator.__set_params(CodeGenerator.fun_symbol, arg_val_list)
        CodeGenerator.__jp_to_function(CodeGenerator.fun_symbol)
        tmp = CodeGenerator.memory_manager.get_address()
        tac = ThreeAddressCode(
            Instruction.ASSIGN, CodeGenerator.RETURN_VALUE_ADDRESS, tmp)
        CodeGenerator.program_block.set_current_and_increment(tac)
        CodeGenerator.semantic_stack.append(tmp)
        CodeGenerator.__pop_after_call(token)

    def __set_params(func: Symbol, values):
        for index, param in enumerate(func.detail.param):
            # TODO check param and input type
            symbol = func.detail.param[index][1]
            record_id = CodeGenerator.record_id_by_function_name[func.name]
            address_symbol = symbol.detail.address_by_scope[record_id]
            if param[0] == 'int':
                rhs = DirectAddress(values[index])
            elif param[0] == 'arr':
                rhs = ImmediateAddress(values[index])
            lhs = DirectAddress(address_symbol)
            tac = ThreeAddressCode(Instruction.ASSIGN, rhs, lhs)
            CodeGenerator.program_block.set_current_and_increment(tac)

    def __jp_to_function(func: Symbol):
        push_len = 2 * (len(func.detail.param) + len(func.detail.local) + 1)
        ret_addr = CodeGenerator.program_block.get_current_address() + 2
        rhs = ImmediateAddress(ret_addr)
        lhs = DirectAddress(RegisterConstants.RETURN_ADDRESS)
        tac = ThreeAddressCode(Instruction.ASSIGN, rhs, lhs)
        CodeGenerator.program_block.set_current_and_increment(tac)
        func_address = func.detail.address_by_scope[0]
        rhs = DirectAddress(func_address)
        tac = ThreeAddressCode(Instruction.JP, rhs, )
        CodeGenerator.program_block.set_current_and_increment(tac)

    def __get_start_addr_and_size():
        detail: FunctionDetails = CodeGenerator.fun_symbol.detail
        record_id = CodeGenerator.record_id_by_function_name[CodeGenerator.fun_symbol.name]
        first: VarDetails = None
        if len(detail.param) > 0:
            first = detail.param[0][1].detail
        elif len(detail.local) > 0:
            first = detail.local[0].detail
        else:
            return
        start_addr = first.address_by_scope[record_id]
        size = len(detail.param) + len(detail.local)
        return start_addr, size

    def __push_before_call(token):
        start_addr, size = CodeGenerator.__get_start_addr_and_size()
        CodeGenerator.program_block.bulk_push_direct(start_addr, size)
        direct_return_address = DirectAddress(RegisterConstants.RETURN_ADDRESS)
        CodeGenerator.program_block.push_to_runtime_stack(direct_return_address)

    def __pop_after_call(token):
        direct_return_address = DirectAddress(RegisterConstants.RETURN_ADDRESS)
        CodeGenerator.program_block.pop_from_runtime_stack(direct_return_address)
        start_addr, size = CodeGenerator.__get_start_addr_and_size()
        CodeGenerator.program_block.bulk_pop_direct(start_addr, size)

    def popExp(token):
        CodeGenerator.semantic_stack.pop()
