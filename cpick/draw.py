import curses
from curses.textpad import Textbox
from .screen import Screen


class Draw(Screen):
    def __init__(self, screen):
        Screen.__init__(self, screen)
        self.indicator = '-->'
        self.checkbox = '[ ]'
        self.checked = '[x]'
        self.scroll = 2  # when to start scrolling

    def draw_header(self):
        msg = ("PICK ITEMS FROM THIS LIST:")
        color = self.magenta_black()
        try:
            self.header.addstr(0, 0, msg, color)
            self.header.clrtoeol()  # more frugal than erase. no flicker.
        except curses.error:
            pass
        self.header.refresh()

    def draw_lines(self):
        '''
        Generator function that yields tuples of each option with an
        indicator prepended to the string or an empty string of the same
        length and a curses color set.
        '''
        for index, option in enumerate(self.options):
            if index == self.index and self.options[index] in self.picked:
                pad = self.indicator
                color = self.black_yellow()
            elif self.options[index] in self.picked:
                pad = self.checked
                color = self.yellow_black()
            elif index == self.index:
                pad = self.indicator
                color = self.black_blue()
            else:
                pad = self.checkbox
                color = self.white_black()
            yield ('{} {}'.format(pad, option), color)

    def draw_body(self):
        '''
        Draw options list to the screen. If options length is greater
        than the size of the terminal, only draw a slice. Support
        scrolling through calculating the current lines position
        relative to the maximum rows available to the screen.
        '''
        self.win.erase()  # clear causes flickering in some terminals
        self.curline = self.index + 1
        self.limit = self.win_y - 1
        self.start, self.stop = 0, self.limit

        if self.curline - self.start > self.limit - self.scroll:
            self.start = self.curline - self.limit + self.scroll
            self.stop = self.start + self.limit

        lines = list(self.draw_lines())[self.start:self.stop]

        for index, line in enumerate(lines):
            option, attr = line
            option = option + ' ' * (self.win_x - len(option))
            self.win.addstr(index, 0, option, attr)

        self.win.refresh()
        self.draw_header()
        self.draw_footer()

    def draw_footer(self):
        msg = ('Press [?] to view keybindings')
        color = self.magenta_black()
        try:
            self.footer.addstr(0, 0, msg, color)
            self.footer.clrtoeol()  # more frugal than erase. no flicker.
        except curses.error:
            pass
        self.footer.refresh()

    def draw_help(self):
        msg = [
            '[k] : Move up one line.',
            '[j] : Move down one line.',
            '[f] : Jump down a page of lines.',
            '[b] : Jump up a page of lines.',
            '[g] : Jump to first line.',
            '[G] : Jump to last line.',
            '[s] : Select an item and go down a line.',
            '[u] : Unselect an item and go up a line.',
            '[/] : Find items via glob pattern matching.',
            '[n] : Jump to next glob match.',
            '[p] : Jump to previous glob match.',
            '[t] : Toggle an items selection.',
            '[a] : Toggle selection of all items.',
            '[:] : Toggle selection via glob pattern matching.',
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

    def draw_textbox(self, prompt):
        length = len(prompt)
        color = self.magenta_black()
        self.footer.erase()
        self.footer.addstr(prompt)
        self.footer.chgat(0, 0, length, color)
        curses.curs_set(1)
        self.footer.refresh()
        tb = self.footer.subwin(self.y - 1, length)
        box = Textbox(tb)
        box.edit()
        curses.curs_set(0)
        result = box.gather()
        self.footer.erase()
        return result
