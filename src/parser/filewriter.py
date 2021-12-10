import os
from anytree.render import RenderTree
from src.parser.parsetree.adopter import ParseTreeAdopter


class ParserFileWriter:
    PARSE_TREE_FILE_NAME = 'parse_tree.txt'
    SYNTAX_ERRORS_FILE_NAME = 'syntax_errors.txt'
    NO_SYNTAX_ERRORS_MESSAGE = 'There is no syntax error.'

    def __init__(self, parse_tree, base_path):
        self.parse_tree = parse_tree
        self.base_path = base_path

    def write(self):
        self.__write_parse_tree()
        self.__write_syntax_errors()

    def __write_parse_tree(self):
        parse_tree_lines = []
        anytree = ParseTreeAdopter(self.parse_tree)
        for pre, _, node in RenderTree(anytree.anytree_root):
            parse_tree_lines.append(f'{pre}{node.name}')
        path = self.__get_file_path(ParserFileWriter.PARSE_TREE_FILE_NAME)
        with open(path, 'w', encoding='utf-8') as parse_tree_file:
            parse_tree_file.write('\n'.join(parse_tree_lines))
            parse_tree_file.write('\n')

    def __write_syntax_errors(self):
        path = self.__get_file_path(ParserFileWriter.SYNTAX_ERRORS_FILE_NAME)
        with open(path, 'w', encoding='utf-8') as syntax_errors_file:
            syntax_errors_file.write(self.NO_SYNTAX_ERRORS_MESSAGE)
            syntax_errors_file.write('\n')

    def __get_file_path(self, file_name):
        return os.path.join(self.base_path, file_name)
