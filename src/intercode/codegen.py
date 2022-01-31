from ast import increment_lineno
from scope import Scope
from share.symbol import VarDetails, FunctionDetails
from intercode.programblock import ProgramBlock, ThreeAddressCode

class CodeGenerator:
    
    semantic_stack = []
    size_by_type = {'int': 4, 'void': 0}
    symbol_table = None
    address = 0

    scope = Scope()
    
    def get_semantic_action(action_symbol):
        action_symbol = action_symbol[1:]
        try:
            return getattr(CodeGenerator, action_symbol)
        except AttributeError:
            raise Exception(f'Semantic action {action_symbol} not found.')
    
    def pushIdDec(token, symbol_table):
        symbol = symbol_table.get_symbol(token.value)
        CodeGenerator.semantic_stack.append(symbol)

    def single(token, symbol_table):
        symbol = CodeGenerator.semantic_stack.pop()
        type = CodeGenerator.semantic_stack.pop()
        varDetails = VarDetails(type)
        varDetails.add_to_scope(CodeGenerator.scope.scope, CodeGenerator.address)
        symbol.SymbolDetails = varDetails
        if type == 'int':
            CodeGenerator.address += CodeGenerator.size_by_type[type]
        else:
            # TODO: this is error, single should not be void
            pass

    def array(token, symbol_table):
        symbol = CodeGenerator.semantic_stack.pop()
        type = CodeGenerator.semantic_stack.pop()
        varDetails = VarDetails(type)
        varDetails.add_to_scope(CodeGenerator.scope.scope, CodeGenerator.address)
        symbol.SymbolDetails = varDetails
        if type == 'int':
            CodeGenerator.address += CodeGenerator.size_by_type[type] * token.value
        else:
            # TODO: this is error, array should not be void
            pass

    def funDef(token, symbol_table):
        symbol = CodeGenerator.semantic_stack.pop()
        type = CodeGenerator.semantic_stack.pop()
        functionDetails = FunctionDetails(type)
        functionDetails.add_to_scope(CodeGenerator.scope)
        CodeGenerator.semantic_stack.append(symbol)
        CodeGenerator.semantic_stack.append(0)

        

    def lastParams(token, symbol_table):
        CodeGenerator.incrementParamCounter(token, symbol_table)
        
        pass

    def pushIdTypeInt(token, symbol_table):
        CodeGenerator.semantic_stack.push('int')
        

    def pushIdTypeVoid(token, symbol_table):
        CodeGenerator.semantic_stack.push('void')
        
    

        

    def incrementParamCounter(token, symbol_table):
        param_id = CodeGenerator.semantic_stack.pop()
        param_type = CodeGenerator.semantic_stack.pop()
        count = CodeGenerator.semantic_stack.pop()
        function_symbol = CodeGenerator.semantic_stack.pop()
        function_symbol.functionDetails.add_param()
        pass

    def paramArr(token, symbol_table):
        pass

    def breakLoop(token, symbol_table):
        pass

    def saveEmptyAddr(token, symbol_table):
        pass

    def writeJmpFalseSavedAddr(token, symbol_table):
        pass

    def writeJmpFalseSavedAddrSaveEmptyAddr(token, symbol_table):
        pass

    def writeJmpSavedAddr(token, symbol_table):
        pass

    def saveAddr(token, symbol_table):
        pass

    def jmpFalseSavedAddr(token, symbol_table):
        pass

    def returnVoid(token, symbol_table):
        pass

    def returnNonVoid(token, symbol_table):
        pass

    def assign(token, symbol_table):
        pass

    def arrayIndex(token, symbol_table):
        pass

    def compare(token, symbol_table):
        pass

    def lessthan(token, symbol_table):
        pass

    def equal(token, symbol_table):
        pass

    def add(token, symbol_table):
        pass
    
    def plus(token, symbol_table):
        pass

    def minus(token, symbol_table):
        pass

    def multiply(token, symbol_table):
        pass

    def pushNum(token, symbol_table):
        pass

    def call(token, symbol_table):
        pass