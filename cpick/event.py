'''
Curses List Picker
'''
import curses
from .action import Action
from os import environ
environ.setdefault('ESCDELAY', '12')  # otherwise it takes an age!


class Event(Action):
    '''
    Instantiate mapping of keys to actions, which is used by modules'
    main getter method that instigates the main event loop.
    '''

    def __init__(self, screen, items):
        Action.__init__(self, screen, items)
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
            'draw_help': [ord('?'), curses.KEY_F1, ],
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
            **dict.fromkeys(self.keys['draw_help'], self.draw_help),
            **dict.fromkeys(self.keys['quit'], self.quit),
        }

    def pick(self):
        '''
        Main event loop that draws the screen, waits for input, and executes an
        action based on that input. If the method executed returns true, we
        return our objects' picked attribute.
        '''
        while True:
            self.draw_header()
            self.draw_body()
            self.draw_footer()
            key = self.win.getch()
            try:
                if self.actions[key]():
                    return [self.items[pick] for pick in self.picked]
            except KeyError:
                pass
