from argparse import ArgumentParser
from curses import wrapper
from columns import prtcols
from .event import Event


def get_args():
    parser = ArgumentParser(description='Curses list picker.')
    parser.add_argument("items", nargs='+', help="Items for the picker.")
    return parser.parse_args()


def pick(screen, items):
    picker = Event(screen, items)
    return picker.pick()


def main():
    args = get_args()
    picked = wrapper(pick, args.items)
    if picked:
        prtcols(picked, 6)


if __name__ == '__main__':
    main()
