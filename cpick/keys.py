import curses


def get_keys():
    desc = [
        '[k][UP]       : Move up one line.',
        '[j][DOWN]     : Move down one line.',
        '[g][HOME]     : Jump to first line.',
        '[G][END]      : Jump to last line.',
        '[f][PGDN]     : Jump down a page of lines.',
        '[b][PGUP]     : Jump up a page of lines.',
        '[#]           : Jump to line number.',
        '[/]           : Find items via wilcards, regex or range.',
        '[n]           : Jump to next search result.',
        '[p]           : Jump to previous search result.',
        '[CTRL-n]      : Jump to next pick.',
        '[CTRL-p]      : Jump to previous pick.',
        '[r][F5]       : Reset search results and picks.',
        '[z][CTRL-l]   : Recenter current line on screen.',
        '[RET]         : Pick an item.',
        '[;]           : Pick via wildcards, regex or range.',
        '[u]           : Undo the last pick.',
        '[U]           : Undo the last pick and move to it\'s line.',
        '[t]           : Toggle an item.',
        '[SPC]         : Toggle item and go down a line.',
        '[CTRL-SPC]    : Toggle item and go up a line.',
        '[a]           : Toggle all items.',
        '[:]           : Toggle via wildcards, regex or range.',
        '[v]           : View all picks.',
        '[?][F1]       : View this help page.',
        '[q][ESC]      : Quit and display all marked paths.',
    ]

    keys = {
        'resize': [
            curses.KEY_RESIZE,
        ],
        'dn': [
            ord('j'),
            curses.KEY_DOWN,
        ],
        'up': [
            ord('k'),
            curses.KEY_UP,
        ],
        'top': [
            ord('g'),
            curses.KEY_HOME,
        ],
        'btm': [
            ord('G'),
            curses.KEY_END,
        ],
        'pgdn': [
            ord('f'),
            curses.KEY_NPAGE,
        ],
        'pgup': [
            ord('b'),
            curses.KEY_PPAGE,
        ],
        'goto': [
            ord('#'),
            curses.ascii.ctrl(ord('g')),
        ],
        'find': [
            ord('/'),
        ],
        'next_find': [
            ord('n'),
            curses.ascii.ctrl(ord('s')),
        ],
        'prev_find': [
            ord('p'),
            curses.ascii.ctrl(ord('r')),
        ],
        'next_pick': [
            curses.ascii.ctrl(ord('n')),
        ],
        'prev_pick': [
            curses.ascii.ctrl(ord('p')),
        ],
        'reset': [
            ord('r'),
            curses.KEY_F5,
        ],
        'recenter': [
            ord('z'),
            curses.ascii.ctrl(ord('l')),
        ],
        'pick': [
            ord('\n'),
        ],
        'pick_pattern': [
            ord(';'),
        ],
        'undo': [
            ord('u'),
        ],
        'undo_up': [
            ord('U'),
        ],
        'toggle': [
            ord('t'),
        ],
        'toggle_dn': [
            ord(' '),
        ],
        'toggle_up': [
            curses.ascii.ctrl(ord(' ')),
        ],
        'toggle_all': [
            ord('a'),
        ],
        'toggle_pattern': [
            ord(':'),
        ],
        'view_picks': [
            ord('v'),
        ],
        'view_help': [
            ord('?'),
            curses.KEY_F1,
        ],
        'quit': [
            ord('q'),
            curses.ascii.ESC,
        ],
    }

    return desc, keys
