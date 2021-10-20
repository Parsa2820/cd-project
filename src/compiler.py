from scanner.scanner import Scanner
from scanner.filewriter import ScannerFileWriter


def read_all_file():
    with open("input.txt", "r") as program_file:
        program = program_file.read()
    program += chr(26)
    return program


def run_parser():
    program = read_all_file()
    scanner = Scanner(program)
    filewriter = ScannerFileWriter(scanner)
    filewriter.write()


if __name__ == '__main__':
    run_parser()
