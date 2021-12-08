import os

from parser.parser import ParserTest
from scanner.scanner import Scanner
from scanner.filewriter import ScannerFileWriter
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
    ParserTest(scanner)
    # filewriter = ScannerFileWriter(scanner, base_path)
    # filewriter.write()


if __name__ == '__main__':
    run_parser()
