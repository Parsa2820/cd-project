import os

import anytree

from parser.parser import SimpleArithmeticParser
from parser.parsetree.adopter import ParseTreeAdopter
from scanner.scanner import Scanner
from scanner.filewriter import ScannerFileWriter
from share.symboltable import SymbolTable
from anytree import RenderTree, Node

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
    tree = parser.parse()
    # print(repr(tree))
    anytree_root = ParseTreeAdopter(tree).anytree_root
    # print(RenderTree(anytree_root, style=anytree.AsciiStyle()))
    utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)
    for pre, fill, node in RenderTree(anytree_root):
        print(f'{pre}{node.name}', file=utf8stdout)
    # filewriter = ScannerFileWriter(scanner, base_path)
    # filewriter.write()


if __name__ == '__main__':
    run_parser()
