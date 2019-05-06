from argparse import ArgumentParser
from curses import wrapper
from .cpick import Picker


def get_args():
    parser = ArgumentParser(description='Curses list picker.')
    parser.add_argument("options", nargs='+', help="Options for the picker.")
    return parser.parse_args()


def pick(screen):
    args = get_args()
    picker = Picker(screen, args.options)
    return picker.get_picked()


def main():
    picked = wrapper(pick)
    if picked:
        print(*picked, sep='\n')


if __name__ == '__main__':
    main()
