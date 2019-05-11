'''
Curses List Picker
'''
from os import environ
from sys import maxsize
from .action import Action
from .keys import get_keys
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
        self.desc, self.keys = get_keys()

        self.pad_actions = {
            **dict.fromkeys(self.keys['resize'], self.resize),
            **dict.fromkeys(self.keys['dn'], self.pad_dn),
            **dict.fromkeys(self.keys['up'], self.pad_up),
            **dict.fromkeys(self.keys['pgdn'], self.pad_pgdn),
            **dict.fromkeys(self.keys['pgup'], self.pad_pgup),
            **dict.fromkeys(self.keys['quit'], self.quit),
        }

        self.actions = {  # https://stackoverflow.com/a/45928598
            **dict.fromkeys(self.keys['resize'],
                            self.resize),
            **dict.fromkeys(self.keys['dn'],
                            self.dn),
            **dict.fromkeys(self.keys['up'],
                            self.up),
            **dict.fromkeys(self.keys['top'],
                            self.top),
            **dict.fromkeys(self.keys['btm'],
                            self.btm),
            **dict.fromkeys(self.keys['pgdn'],
                            self.pgdn),
            **dict.fromkeys(self.keys['pgup'],
                            self.pgup),
            **dict.fromkeys(self.keys['goto'],
                            self.goto),
            **dict.fromkeys(self.keys['find'],
                            lambda: self.match("Find: ",
                                               self.matches,
                                               self.pick)),
            **dict.fromkeys(self.keys['next_find'],
                            lambda: self.goto_next(self.matches)),
            **dict.fromkeys(self.keys['prev_find'],
                            lambda: self.goto_prev(self.matches)),
            **dict.fromkeys(self.keys['next_pick'],
                            lambda: self.goto_next(self.picked)),
            **dict.fromkeys(self.keys['prev_pick'],
                            lambda: self.goto_prev(self.picked)),
            **dict.fromkeys(self.keys['reset'],
                            self.reset),
            **dict.fromkeys(self.keys['recenter'],
                            self.recenter),
            **dict.fromkeys(self.keys['pick'],
                            lambda: self.pick(self.curidx) or self.dn()),
            **dict.fromkeys(self.keys['pick_pattern'],
                            lambda: self.match("Pick: ",
                                               self.picked,
                                               self.pick)),
            **dict.fromkeys(self.keys['undo'],
                            self.undo),
            **dict.fromkeys(self.keys['undo_up'],
                            lambda: self.undo() or self.goto_prev(self.picked)),
            **dict.fromkeys(self.keys['toggle'],
                            lambda: self.toggle(self.curidx)),
            **dict.fromkeys(self.keys['toggle_dn'],
                            lambda: self.toggle(self.curidx) or self.dn()),
            **dict.fromkeys(self.keys['toggle_up'],
                            lambda: self.toggle(self.curidx) or self.up()),
            **dict.fromkeys(self.keys['toggle_all'],
                            self.toggle_all),
            **dict.fromkeys(self.keys['toggle_pattern'],
                            lambda: self.match("Toggle: ",
                                               self.picked,
                                               self.toggle)),
            **dict.fromkeys(self.keys['help'],
                            self.get_help),
            **dict.fromkeys(self.keys['quit'],
                            self.quit),
        }

    def get_help(self):
        self.draw_pad(self.desc)
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

    def get_picks(self):
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
                header, footer = ("MAXIMUM PICK LIMIT REACHED!",) * 2
            else:
                header, footer = self.header, self.footer
