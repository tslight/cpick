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
                 numbers=False,
                 header='PICK ITEMS FROM THIS LIST:',
                 footer='Press [?] to view keybindings'):
        Action.__init__(self, screen, items)
        self.limit, self.numbers = limit, numbers
        self.header, self.footer = header, footer
        self.desc, self.keys = get_keys()

        self.win_actions = {
            **dict.fromkeys(self.keys['resize'], self.resize),
            **dict.fromkeys(self.keys['down'], self.down_win),
            **dict.fromkeys(self.keys['up'], self.up_win),
            **dict.fromkeys(self.keys['pgdn'], self.pgdn_win),
            **dict.fromkeys(self.keys['pgup'], self.pgup_win),
            **dict.fromkeys(self.keys['top'], self.top_win),
            **dict.fromkeys(self.keys['bottom'], self.bottom_win),
            **dict.fromkeys(self.keys['quit'], self.quit),
        }

        self.line_actions = {  # https://stackoverflow.com/a/45928598
            **dict.fromkeys(self.keys['resize'],
                            self.resize),
            **dict.fromkeys(self.keys['down'],
                            self.down_line),
            **dict.fromkeys(self.keys['up'],
                            self.up_line),
            **dict.fromkeys(self.keys['top'],
                            self.top_line),
            **dict.fromkeys(self.keys['bottom'],
                            self.bottom_line),
            **dict.fromkeys(self.keys['pgdn'],
                            self.pgdn_line),
            **dict.fromkeys(self.keys['pgup'],
                            self.pgup_line),
            **dict.fromkeys(self.keys['goto'],
                            self.goto),
            **dict.fromkeys(self.keys['find'],
                            lambda:
                            self.match("Find: ", self.matches, self.pick)),
            **dict.fromkeys(self.keys['next_find'],
                            lambda:
                            self.goto_next(self.matches)),
            **dict.fromkeys(self.keys['prev_find'],
                            lambda:
                            self.goto_prev(self.matches)),
            **dict.fromkeys(self.keys['next_pick'],
                            lambda:
                            self.goto_next(self.picked)),
            **dict.fromkeys(self.keys['prev_pick'],
                            lambda:
                            self.goto_prev(self.picked)),
            **dict.fromkeys(self.keys['reset'],
                            self.reset),
            **dict.fromkeys(self.keys['recenter'],
                            self.recenter_line),
            **dict.fromkeys(self.keys['pick'],
                            lambda:
                            self.pick(
                                self.curline, self.picked) or self.down_line()
                            ),
            **dict.fromkeys(self.keys['pick_pattern'],
                            lambda:
                            self.match("Pick: ", self.picked, self.pick)),
            **dict.fromkeys(self.keys['undo'],
                            self.undo),
            **dict.fromkeys(self.keys['undo_up'],
                            lambda:
                            self.undo() or self.goto_prev(self.picked)),
            **dict.fromkeys(self.keys['toggle'],
                            lambda:
                            self.toggle(self.curline, self.picked)),
            **dict.fromkeys(self.keys['toggle_down'],
                            lambda:
                            self.toggle(self.curline,
                                        self.picked) or self.down_line()),
            **dict.fromkeys(self.keys['toggle_up'],
                            lambda:
                            self.toggle(self.curline,
                                        self.picked) or self.up_line()),
            **dict.fromkeys(self.keys['toggle_all'],
                            self.toggle_all),
            **dict.fromkeys(self.keys['toggle_pattern'],
                            lambda:
                            self.match("Toggle: ", self.picked, self.toggle)),
            **dict.fromkeys(self.keys['view_picks'],
                            lambda:
                            self.view(
                                contents=[
                                    self.items[pick] for pick in self.picked
                                ])),
            **dict.fromkeys(self.keys['view_help'],
                            lambda:
                            self.view(self.desc)),
            **dict.fromkeys(self.keys['save'],
                            self.save),
            **dict.fromkeys(self.keys['quit'],
                            self.quit),
        }

    def view(self, contents):
        pminrow, self.pminrow = self.pminrow, 0
        self.screen.erase()
        if not contents:
            contents = ['', 'Nothing to see here...']
        self.draw_body(contents, pick=False)
        self.draw_header("Press [UP] [DOWN] [PGUP] [PGDN] to scroll.")
        self.draw_footer("Press [q] or [ESC] to return to picker.")
        while True:
            self.refresh()
            key = self.body.getch()
            try:
                if self.win_actions[key]() == "quit":
                    break
            except KeyError:
                pass
        self.pminrow = pminrow

    def get_picks(self):
        '''
        Main event loop that draws the screen, waits for input, and executes an
        action based on that input. If the method executed returns true, we
        return our objects' picked attribute.
        '''
        header, footer, out = self.header, self.footer, None
        while True:
            self.draw_body(self.items, numbers=self.numbers)
            self.draw_header(header)
            self.draw_footer(footer)
            self.refresh()
            key = self.body.getch()
            try:
                out = self.line_actions[key]()
                if out == 'quit':
                    return [self.items[pick] for pick in self.picked]
            except KeyError:
                pass
            if len(self.picked) > self.limit:
                if self.limit == 1:
                    del self.picked[:self.limit]
                else:
                    del self.picked[self.limit:]
                header, footer = ("MAXIMUM PICK LIMIT REACHED!",) * 2
            elif out:
                footer = out
            else:
                header, footer = self.header, self.footer
