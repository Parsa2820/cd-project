import shutil
import clear


def zip(clear_files=True):
    if clear_files:
        clear.clear()
    print('Zipping...')
    shutil.make_archive('../src', 'zip', '../src')
    print('Done!')


if __name__ == '__main__':
    zip()
