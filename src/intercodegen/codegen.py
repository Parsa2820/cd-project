from ast import increment_lineno
from scope import Scope
from share.symbol import VarDetails, FunctionDetails
from intercodegen.intercodeutils.pb import ProgramBlock
from intercodegen.intercodeutils.tac import *


class CodeGenerator:

    semantic_stack = []
    size_by_type = {'int': 4, 'void': 0}
    symbol_table = None
    program_block: ProgramBlock = None
    address = 0

    scope = Scope()

    def get_semantic_action(action_symbol):
        action_symbol = action_symbol[1:]
        try:
            return getattr(CodeGenerator, action_symbol)
        except AttributeError:
            raise Exception(f'Semantic action {action_symbol} not found.')

    def pushIdDec(token):
        symbol = symbol_table.get_symbol(token.value)
        CodeGenerator.semantic_stack.append(symbol)

    def single(token):
        symbol = CodeGenerator.semantic_stack.pop()
        type = CodeGenerator.semantic_stack.pop()
        varDetails = VarDetails(type)
        varDetails.add_to_scope(
            CodeGenerator.scope.scope, CodeGenerator.address)
        symbol.SymbolDetails = varDetails
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
        symbol.SymbolDetails = varDetails
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

    def lastParams(token):
        CodeGenerator.incrementParamCounter(token)

        pass

    def pushIdTypeInt(token):
        CodeGenerator.semantic_stack.push('int')

    def pushIdTypeVoid(token):
        CodeGenerator.semantic_stack.push('void')

    def incrementParamCounter(token):
        param_id = CodeGenerator.semantic_stack.pop()
        param_type = CodeGenerator.semantic_stack.pop()
        count = CodeGenerator.semantic_stack.pop()
        function_symbol = CodeGenerator.semantic_stack.pop()
        function_symbol.functionDetails.add_param()
        pass

    def paramArr(token):
        pass

    def breakLoop(token):
        pass

    def saveEmptyAddr(token):
        pass

    def writeJmpFalseSavedAddr(token):
        pass

    def writeJmpFalseSavedAddrSaveEmptyAddr(token):
        pass

    def writeJmpSavedAddr(token):
        pass

    def saveAddr(token):
        pass

    def jmpFalseSavedAddr(token):
        pass

    def returnVoid(token):
        pass

    def returnNonVoid(token):
        pass

    def assign(token):
        pass

    def arrayIndex(token):
        pass

    def apply():
        second_operand = CodeGenerator.semantic_stack.pop()
        instruction = CodeGenerator.semantic_stack.pop()
        first_operand = CodeGenerator.semantic_stack.pop()
        result_tmp = get_tmp()
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

    def call(token):
        pass


def get_tmp():
    raise NotImplementedError
