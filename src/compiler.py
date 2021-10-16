from scanner import dfa, scanner

if __name__ == '__main__':
    with open("input.txt", "r") as program_file:
        program = program_file.read()
        program += chr(26)
        program_scanner = scanner.Scanner(str(program))
        program_scanner.get_next_token()

'''
if (2 == 2) {
printf("f");
}

'''
