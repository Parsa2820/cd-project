import os


def clear():
    print('Clearing...')
    #delete_file("../src/input.txt")
    delete_file("../src/lexical_errors.txt")
    delete_file("../src/symbol_table.txt")
    delete_file("../src/tokens.txt")
    delete_file("../src/parse_tree.txt")
    delete_file("../src/syntax_errors.txt")
    delete_file("../src/output.txt")
    delete_file("../src/semantic_errors.txt")
    print('Cleared!')


def delete_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


if __name__ == "__main__":
    clear()
