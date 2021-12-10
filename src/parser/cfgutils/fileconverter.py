import os
from compiler import read_all_file
from src.parser.cfgutils.converter import CfgToTransitionDiagramConverter


class FileConverter(CfgToTransitionDiagramConverter):
    DIR_NAME = 'parser/cfg'
    CFG_FILE_NAME = 'cfg.txt'
    FIRSTS_FILE_NAME = 'firsts.txt'
    FOLLOWS_FILE_NAME = 'follows.txt'

    def __init__(self, base_path):
        self.base_path = os.path.join(base_path, FileConverter.DIR_NAME)
        cfg = self.__read_all_file(
            self.__get_file_path(FileConverter.CFG_FILE_NAME))
        firsts_string = self.__read_all_file(
            self.__get_file_path(FileConverter.FIRSTS_FILE_NAME))
        follows_string = self.__read_all_file(
            self.__get_file_path(FileConverter.FOLLOWS_FILE_NAME))
        super().__init__(cfg, firsts_string, follows_string)

    def __read_all_file(self, path):
        with open(path, 'r') as file:
            text = file.read()
        return text

    def __get_file_path(self, file_name):
        return os.path.join(self.base_path, file_name)
