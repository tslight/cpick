'''
Curses List Picker
'''
import curses
from os import environ
from sys import maxsize
from .action import Action
environ.setdefault('ESCDELAY', '12')  # otherwise it takes an age!


class Event(Action):
    '''
    Instantiate mapping of keys to actions, which is used by modules'
    main getter method that instigates the main event loop.
    '''

    def __init__(self,
                 screen,
                 items,
                 limit=maxsize,
                 header='PICK ITEMS FROM THIS LIST:',
                 footer='Press [?] to view keybindings'):
        Action.__init__(self, screen, items)
        self.limit, self.header, self.footer = limit, header, footer
        self.helptxt = [
            '[k][UP]       : Move up one line.',
            '[j][DOWN]     : Move down one line.',
            '[f][PGDN]     : Jump down a page of lines.',
            '[b][PGUP]     : Jump up a page of lines.',
            '[g][HOME]     : Jump to first line.',
            '[G][END]      : Jump to last line.',
            '[#]           : Jump to line number.',
            '[/]           : Find items via glob pattern matching.',
            '[n]           : Jump to next search result.',
            '[N]           : Jump to previous search result.',
            '[p]           : Jump to next pick.',
            '[P]           : Jump to previous pick.',
            '[R][F5]       : Reset search results and picks.',
            '[z][Z]        : Recenter current line on screen.',
            '[s][SPC]      : Pick an item and go down a line.',
            '[u][U]        : Unpick an item and go up a line.',
            '[t][T]        : Toggle item pick status.',
            '[a][A]        : Toggle picking of all items.',
            '[;][*]        : Toggle via globbing, regex or substring.',
            '[:][!]        : Toggle via index number or range of indices.',
            '[?][F1]       : View this help page.',
            '[q][ESC][RET] : Quit and display all marked paths.',
        ]

        self.keys = {
            'dn': [ord('j'), curses.KEY_DOWN, ],
            'up': [ord('k'), curses.KEY_UP, ],
            'top': [ord('g'), curses.KEY_HOME, ],
            'btm': [ord('G'), curses.KEY_END, ],
            'pgdn': [ord('f'), curses.KEY_NPAGE, ],
            'pgup': [ord('b'), curses.KEY_PPAGE, ],
            'reset': [ord('R'), curses.KEY_F5, ],
            'recenter': [ord('z'), ord('Z'), ],
            'goto': [ord('#'), curses.KEY_F3, ],
            'toggle': [ord('t'), ord('T'), ],
            'toggle_dn': [ord('s'), ord(' '), ],
            'toggle_up': [ord('u'), ord('S'), ],
            'toggle_all': [ord('a'), ord('A'), ],
            'toggle_pattern': [ord(';'), ord('*'), ],
            'toggle_range': [ord(':'), ord('!'), ],
            'find': [ord('/'), curses.KEY_F2, ],
            'next_find': [ord('n'), ],
            'prev_find': [ord('N'), ],
            'next_pick': [ord('p'), ],
            'prev_pick': [ord('P'), ],
            'help': [ord('?'), curses.KEY_F1, ],
            'quit': [ord('q'), ord('\n'), curses.ascii.ESC, ],
        }

        self.actions = {  # https://stackoverflow.com/a/45928598
            curses.KEY_RESIZE: self.resize,
            **dict.fromkeys(self.keys['dn'], self.dn),
            **dict.fromkeys(self.keys['up'], self.up),
            **dict.fromkeys(self.keys['top'], self.top),
            **dict.fromkeys(self.keys['btm'], self.btm),
            **dict.fromkeys(self.keys['pgdn'], self.pgdn),
            **dict.fromkeys(self.keys['pgup'], self.pgup),
            **dict.fromkeys(self.keys['reset'], self.reset),
            **dict.fromkeys(self.keys['recenter'], self.recenter),
            **dict.fromkeys(self.keys['goto'], self.goto),
            **dict.fromkeys(self.keys['toggle'],
                            lambda: self.toggle(self.curidx)),
            **dict.fromkeys(self.keys['toggle_dn'],
                            lambda: self.toggle(self.curidx) or self.dn()),
            **dict.fromkeys(self.keys['toggle_up'],
                            lambda: self.toggle(self.curidx) or self.up()),
            **dict.fromkeys(self.keys['toggle_all'], self.toggle_all),
            **dict.fromkeys(self.keys['toggle_pattern'], self.toggle_pattern),
            **dict.fromkeys(self.keys['toggle_range'], self.toggle_range),
            **dict.fromkeys(self.keys['find'], self.find),
            **dict.fromkeys(self.keys['next_find'],
                            lambda: self.goto_next(self.matches)),
            **dict.fromkeys(self.keys['prev_find'],
                            lambda: self.goto_prev(self.matches)),
            **dict.fromkeys(self.keys['next_pick'],
                            lambda: self.goto_next(self.picked)),
            **dict.fromkeys(self.keys['prev_pick'],
                            lambda: self.goto_prev(self.picked)),
            **dict.fromkeys(self.keys['help'], self.help),
            **dict.fromkeys(self.keys['quit'], self.quit),
        }

        self.pad_actions = {
            curses.KEY_RESIZE: self.resize,
            **dict.fromkeys(self.keys['dn'], self.pad_dn),
            **dict.fromkeys(self.keys['up'], self.pad_up),
            **dict.fromkeys(self.keys['pgdn'], self.pad_pgdn),
            **dict.fromkeys(self.keys['pgup'], self.pad_pgup),
            **dict.fromkeys(self.keys['quit'], self.quit),
        }

    def help(self):
        self.draw_pad(self.helptxt)
        self.screen.refresh()
        self.draw_header("Press [UP] [DOWN] [PGUP] [PGDN] to scroll.")
        self.draw_footer("Press [q] or [ESC] to return to picker.")
        self.pad.refresh(self.pos, 0, 1, 0, self.y - 2, self.x - 2)
        while True:
            key = self.screen.getch()
            try:
                if self.pad_actions[key]():
                    break
            except KeyError:
                pass
            self.pad.refresh(self.pos, 0, 1, 0, self.y - 2, self.x - 2)
        self.screen.erase()
        self.screen.refresh()

    def pick(self):
        '''
        Main event loop that draws the screen, waits for input, and executes an
        action based on that input. If the method executed returns true, we
        return our objects' picked attribute.
        '''
        header, footer = self.header, self.footer
        while True:
            self.draw_header(header)
            self.draw_body()
            self.draw_footer(footer)
            key = self.win.getch()
            try:
                if self.actions[key]():
                    return [self.items[pick] for pick in self.picked]
            except KeyError:
                pass
            if len(self.picked) > self.limit:
                if self.limit == 1:
                    del self.picked[:self.limit]
                else:
                    del self.picked[self.limit:]
                header, footer = ("MAXIMUM PICK LIMIT REACHED!",)*2
            else:
                header, footer = self.header, self.footer
