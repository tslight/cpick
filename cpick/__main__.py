from argparse import ArgumentParser
from curses import wrapper
from columns import prtcols
from .picker import Picker


def get_args():
    parser = ArgumentParser(description='Curses list picker.')
    parser.add_argument("options", nargs='+', help="Options for the picker.")
    return parser.parse_args()


def pick(screen, options):
    picker = Picker(screen, options)
    return picker.get_picked()


def main():
    args = get_args()
    picked = wrapper(pick, args.options)
    if picked:
        prtcols(picked, 6)


if __name__ == '__main__':
    main()
