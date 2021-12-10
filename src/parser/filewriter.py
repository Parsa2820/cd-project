import os
from anytree.render import RenderTree
from src.parser.parsetree.adopter import ParseTreeAdopter


class ParserFileWriter:
    PARSE_TREE_FILE_NAME = 'parse_tree.txt'
    SYNTAX_ERRORS_FILE_NAME = 'syntax_errors.txt'
    NO_SYNTAX_ERRORS_MESSAGE = 'There is no syntax error.'

    def __init__(self, parse_tree, base_path, syntax_errors):
        self.parse_tree = parse_tree
        self.base_path = base_path
        self.syntax_errors = syntax_errors

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
        syntax_errors_lines = []
        if len(self.syntax_errors) == 0:
            syntax_errors_lines.append(
                ParserFileWriter.NO_SYNTAX_ERRORS_MESSAGE)
        else:
            for error in self.syntax_errors:
                syntax_errors_lines.append(error)

        path = self.__get_file_path(ParserFileWriter.SYNTAX_ERRORS_FILE_NAME)
        with open(path, 'w') as syntax_error_file:
            syntax_error_file.write('\n'.join(syntax_errors_lines))
            syntax_error_file.write('\n')

    def __get_file_path(self, file_name):
        return os.path.join(self.base_path, file_name)
