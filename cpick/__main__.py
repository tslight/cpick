from argparse import ArgumentParser
from curses import wrapper
from cpick import Picker


def get_args():
    """
    Return a list of valid arguments. If no argument is given, default to $PWD.
    """
    parser = ArgumentParser(description='Curses list picker.')
    parser.add_argument("options", nargs='+', help="Options for the picker.")
    return parser.parse_args()


def pick(screen, options):
    args = get_args()
    picker = Picker(screen, args.options)
    return picker.get_picked()


if __name__ == '__main__':
    picked = wrapper(pick)
    if picked:
        print(*picked, sep='\n')
