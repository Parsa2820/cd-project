from scanner import scanner


def get_all_tokens():
    with open("input.txt", "r") as program_file:
        program = program_file.read()
    program += chr(26)
    program_scanner = scanner.Scanner(str(program))
    token = program_scanner.get_next_token()
    token_file = open("tokens.txt", "w")
    while token:
        print(token)
        token_file.write(str(token) + "\n")
        token = program_scanner.get_next_token()
    token_file.close()


if __name__ == '__main__':
    get_all_tokens()
