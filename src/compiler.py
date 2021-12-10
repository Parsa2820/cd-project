import os

from parser.filewriter import ParserFileWriter
from parser.parser import *
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
    parser = SimpleArithmeticParser(scanner)
    # parser = CMinusParser(scanner)
    tree = parser.parse()
    file_writer = ParserFileWriter(tree, base_path)
    file_writer.write()


if __name__ == '__main__':
    run_parser()
