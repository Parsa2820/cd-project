import os


class CodeGeneratorFileWriter:
    THREE_ADDRESS_CODE_FILE_NAME = 'output.txt'
    SEMANTIC_ERRORS_FILE_NAME = 'semantic_errors.txt'
    NO_SEMANTIC_ERRORS_MESSAGE = 'The input program is semantically correct.'
    NO_SEMANTIC_ERRORS_TAC = 'The code has not been generated.'

    def __init__(self, program_block, base_path, semantic_errors):
        self.program_block = program_block
        self.base_path = base_path
        self.semantic_errors = semantic_errors

    def write(self):
        self.__write_program_block()
        self.__write_semantic_errors()

    def __write_program_block(self):
        path = self.__get_file_path(
            CodeGeneratorFileWriter.THREE_ADDRESS_CODE_FILE_NAME)
        with open(path, 'w', encoding='utf-8') as three_address_code_file:
            if len(self.semantic_errors) != 0:
                three_address_code_file.write(CodeGeneratorFileWriter.NO_SEMANTIC_ERRORS_TAC)
            else:
                three_address_code_file.write(str(self.program_block))

        path = self.__get_file_path('../docs/phase3/interpreter/output.txt')
        with open(path, 'w', encoding='utf-8') as three_address_code_file:
            if len(self.semantic_errors) != 0:
                three_address_code_file.write(CodeGeneratorFileWriter.NO_SEMANTIC_ERRORS_TAC)
            else:
                three_address_code_file.write(str(self.program_block))

    def __write_semantic_errors(self):
        semantic_errors_lines = []
        if len(self.semantic_errors) == 0:
            semantic_errors_lines.append(
                CodeGeneratorFileWriter.NO_SEMANTIC_ERRORS_MESSAGE)
        else:
            for error in self.semantic_errors:
                semantic_errors_lines.append(str(error))
        path = self.__get_file_path(
            CodeGeneratorFileWriter.SEMANTIC_ERRORS_FILE_NAME)
        with open(path, 'w') as semantic_error_file:
            semantic_error_file.write('\n'.join(semantic_errors_lines))
            semantic_error_file.write('\n')

    def __get_file_path(self, file_name):
        return os.path.join(self.base_path, file_name)
