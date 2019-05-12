from argparse import ArgumentParser
from curses import wrapper
from sys import maxsize
from columns import prtcols
from .event import Event


def get_args():
    parser = ArgumentParser(description='Curses list picker.')
    parser.add_argument('items', nargs='+', help='Items for the picker.')
    parser.add_argument('--limit', '-l', type=int,
                        default=maxsize,
                        help='Limit number of picks.')
    parser.add_argument('--numbers', '-n',
                        default=False,
                        action='store_true',
                        help='Show line numbers.')
    parser.add_argument('--header', '-H', type=str,
                        default='PICK ITEMS FROM THIS LIST:',
                        help='A string to use as a header.')
    parser.add_argument('--footer', '-F', type=str,
                        default='Press [?] to view keybindings',
                        help='A string to use as a footer.')
    return parser.parse_args()


def event(screen, **kwargs):
    picker = Event(screen, **kwargs)
    return picker.get_picks()


def pick(**kwargs):
    return wrapper(event, **kwargs)


def main():
    args = get_args()
    kwargs = {
        'items': args.items,
        'limit': args.limit,
        'numbers': args.numbers,
        'header': args.header,
        'footer': args.footer,
    }
    picked = pick(**kwargs)
    if picked:
        prtcols(picked, 6)


if __name__ == '__main__':
    main()
