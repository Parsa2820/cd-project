from symtable import Symbol, SymbolTable
from scope import Scope
from share.symbol import VarDetails, FunctionDetails
from intercodegen.intercodeutils.pb import ProgramBlock
from intercodegen.intercodeutils.tac import *
from intercodegen.memman import MemoryManager



class CodeGenerator:
    
    semantic_stack = []
    size_by_type = {'int': 4, 'void': 0}
    symbol_table: SymbolTable = None
    program_block: ProgramBlock = None
    memory_manager: MemoryManager = None
    address = 0
    fun_id: Symbol = None

    scope = Scope()

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
        varDetails.add_to_scope(
            CodeGenerator.scope.scope, CodeGenerator.address)
        symbol.set_detail(varDetails)
        if type == 'int':
            CodeGenerator.address += CodeGenerator.size_by_type[type]
        else:
            # TODO: this is error, single should not be void
            pass

    def array(token):
        symbol = CodeGenerator.semantic_stack.pop()
        type = CodeGenerator.semantic_stack.pop()
        varDetails = VarDetails(type)
        varDetails.add_to_scope(
            CodeGenerator.scope.scope, CodeGenerator.address)
        symbol.set_detail(varDetails)
        if type == 'int':
            CodeGenerator.address += CodeGenerator.size_by_type[type] * token.value
        else:
            # TODO: this is error, array should not be void
            pass

    def funDef(token):
        symbol = CodeGenerator.semantic_stack.pop()
        type = CodeGenerator.semantic_stack.pop()
        functionDetails = FunctionDetails(type)
        functionDetails.add_to_scope(CodeGenerator.scope)
        CodeGenerator.semantic_stack.append(symbol)
        CodeGenerator.semantic_stack.append(0)

    def lastParam(token):
        CodeGenerator.incrementParamCounter(token)
        pb_addr = CodeGenerator.program_block.get_current_address()
        add1 = ImmediateAddress(pb_addr + 1) #+1 for assign instruction
        add2 = DirectAddress(CodeGenerator.address)
        tac = ThreeAddressCode(Instruction.ASSIGN, add1, add2)
        CodeGenerator.program_block.set_current_and_increment(tac)
        CodeGenerator.address += CodeGenerator.size_by_type['int']

    def pushIdTypeInt(token):
        CodeGenerator.semantic_stack.append('int')

    def pushIdTypeVoid(token):
        CodeGenerator.semantic_stack.append('void')

    def incrementParamCounter(token):
        param_id = CodeGenerator.semantic_stack.pop()
        param_type = CodeGenerator.semantic_stack.pop()
        function_symbol = CodeGenerator.semantic_stack.pop()
        function_symbol.functionDetails.add_param((param_type, param_id))
        CodeGenerator.semantic_stack.append(function_symbol)
        

    def paramArr(token):
        symbol = CodeGenerator.semantic_stack.pop()
        CodeGenerator.semantic_stack.append('arr')
        CodeGenerator.semantic_stack.append(symbol)
        

    def funEnd(token):        
        pass

    def breakLoop(token):
        pass

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

    def saveAddr(token):
        address = CodeGenerator.program_block.get_current_address()
        CodeGenerator.semantic_stack.append(address)

    def jmpFalseSavedAddr(token):
        predicate = CodeGenerator.semantic_stack.pop()
        address = CodeGenerator.semantic_stack.pop()
        tac = ThreeAddressCode(Instruction.JPF, predicate, address)
        CodeGenerator.program_block.set_current_and_increment(tac)

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
        result_tmp = CodeGenerator.memory_manager.get_tmp()
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

    def pushID(token):
        symbol = CodeGenerator.symbol_table.get_symbols(token.value)
        global_scope = 0
        symbol_address = 0
        if CodeGenerator.memory_manager.scope in symbol.details:
            symbol_address =  symbol.details[CodeGenerator.memory_manager.scope]
        else: symbol_address = symbol.details[global_scope]
        # TODO id not found semantic error should be implemented
        CodeGenerator.semantic_stack.append(symbol_address)
        CodeGenerator.fun_id = symbol

    def call(token):
        CodeGenerator.memory_manager.add_scope()
        param_count = CodeGenerator.fun_id.details.params_count()
        arg_val_list = []
        for i in range(0,param_count):
            arg_val = CodeGenerator.semantic_stack.pop()
            arg_val_list.append(arg_val)
        arg_val_list.reverse()
        CodeGenerator.define_params(CodeGenerator.fun_id, arg_val_list)
        CodeGenerator.set_pb_pointer(CodeGenerator.fun_id)
        
    
    def define_params(func: Symbol, values):
        for index, param in enumerate(func.details.param):
            # TODO check param and input type
            curr_address = CodeGenerator.memory_manager.get_address('int')
            if param[0] == 'int':
                rhs = DirectAddress(values[index])
            else:  rhs = ImmediateAddress(values[index])
            lhs = DirectAddress(curr_address)
            tac = ThreeAddressCode(Instruction.ASSIGN, rhs, lhs)
            CodeGenerator.program_block.set_current_and_increment(tac)
            CodeGenerator.add_address_to_symbol(param[1], CodeGenerator.memory_manager.scope, curr_address)
        

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
            
