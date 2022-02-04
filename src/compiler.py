'''
Parsa Mohammadian - 98102284
Arian Yazdanparast - 98110095
'''

import os
from intercodegen.codegen import CodeGenerator
from intercodegen.intercodeutils.pb import ProgramBlock
from intercodegen.memman import MemoryManager

from intercodegen.filewriter import CodeGeneratorFileWriter
from _parser.filewriter import ParserFileWriter
from _parser.parser import *
from scanner.scanner import Scanner
from share.symboltable import SymbolTable


INPUT_FILE_NAME = 'input.txt'


def read_all_file(path):
    with open(path, 'r') as file:
        text = file.read()
    text += chr(26)
    return text


def run_parser():
    base_path = os.path.dirname(os.path.realpath(__file__))
    program = read_all_file(os.path.join(base_path, INPUT_FILE_NAME))
    symbol_table = SymbolTable()
    scanner = Scanner(program, symbol_table)
    CodeGenerator.memory_manager = MemoryManager()
    pb = ProgramBlock()
    CodeGenerator.program_block = pb
    CodeGenerator.symbol_table = symbol_table
    parser = FileCfgParser(scanner, base_path)
    tree, errors, semantic_errors = parser.parse()
    parser_file_writer = ParserFileWriter(tree, base_path, errors)
    parser_file_writer.write()
    file_writer = CodeGeneratorFileWriter(pb, base_path, semantic_errors)
    file_writer.write()
    print(CodeGenerator.record_id_by_function_name)
    print(CodeGenerator.symbol_table)


if __name__ == '__main__':
    run_parser()
