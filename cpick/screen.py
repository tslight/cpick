import curses
from .color import Color
from textwrap import dedent


class Screen(Color):
    def __init__(self, screen):
        Color.__init__(self)
        self.screen = screen
        self.y, self.x = self.screen.getmaxyx()
        self.header = curses.newwin(0, self.x, 0, 0)
        self.win = curses.newwin(self.y - 3, self.x, 2, 0)
        self.win_y, self.win_x = self.win.getmaxyx()
        self.footer = curses.newwin(0, self.x, self.y - 1, 0)
        self.screen.refresh()
        self.win.refresh()
        self.pad = curses.newpad(self.y, self.x)
        self.footer.refresh()
        self.header.refresh()
        self.lc, self.pos = (0,)*2

    def resize(self):
        self.screen.erase()
        self.y, self.x = self.screen.getmaxyx()
        self.header.resize(1, self.x)
        self.win.resize(self.y - 3, self.x)
        self.win_y, self.win_x = self.win.getmaxyx()
        if self.lc:
            self.pad.resize(self.lc + 2, self.x)
        self.footer.mvwin(self.y - 1, 0)
        self.footer.resize(1, self.x)
        self.screen.refresh()
        self.header.refresh()
        self.win.refresh()
        self.footer.refresh()

    def mkheader(self):
        msg = ("PICK ITEMS FROM THIS LIST:")
        color = self.magenta_black()
        try:
            self.header.addstr(0, 0, msg, color)
            self.header.clrtoeol()  # more frugal than erase. no flicker.
        except curses.error:
            pass
        self.header.refresh()

    def mkfooter(self):
        msg = ('Press [?] to view keybindings')
        color = self.magenta_black()
        try:
            self.footer.addstr(0, 0, msg, color)
            self.footer.clrtoeol()  # more frugal than erase. no flicker.
        except curses.error:
            pass
        self.footer.refresh()

    def mkhelp(self):
        msg = [
            '[k] : Move up one line.',
            '[j] : Move down one line.',
            '[f] : Jump down a page of lines.',
            '[b] : Jump up a page of lines.',
            '[g] : Jump to first line.',
            '[G] : Jump to last line.',
            '[s] : Select an item and go down a line.',
            '[u] : Unselect an item and go up a line.',
            '[t] : Toggle an items selection.',
            '[a] : Toggle selection of all items.',
            '[?] : View this help page.',
            '[q] : Quit and display all marked paths.',
        ]
        self.lc = len(msg)
        self.screen.erase()
        self.pad.erase()
        self.pad.resize(self.lc + 2, self.x)
        try:
            for index, line in enumerate(msg):
                self.pad.addstr(index + 1, 2, line)
            self.pad.scrollok(1)
            self.pad.idlok(1)
        except curses.error:
            pass
        self.screen.refresh()
        self.pad.refresh(self.pos, 0, 0, 0, self.y - 2, self.x - 2)
        self.screen.getch()
        self.screen.erase()
        self.screen.refresh()
