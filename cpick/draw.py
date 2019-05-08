import curses
from curses.textpad import Textbox
from .screen import Screen


class Draw(Screen):
    def __init__(self, screen, options):
        Screen.__init__(self, screen)
        self.options = options
        self.indicator = '-->'
        self.checkbox = '[ ]'
        self.checked = '[x]'
        self.scroll = 2  # when to start scrolling
        self.start = 0
        self.stop = len(self.options)
        self.limit = self.win_y - 1
        self.index = 0
        self.page = self.stop // self.limit

    def draw_header(self):
        msg = ("PICK ITEMS FROM THIS LIST:")
        try:
            self.header.addstr(0, 0, msg, self.magenta_black())
            self.header.clrtoeol()  # more frugal than erase. no flicker.
        except curses.error:
            pass
        self.header.refresh()

    def draw_footer(self):
        msg = ('Press [?] to view keybindings')
        try:
            self.footer.addstr(0, 0, msg, self.magenta_black())
            self.footer.clrtoeol()  # more frugal than erase. no flicker.
        except curses.error:
            pass
        self.footer.refresh()

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

    def draw(self):
        '''
        Draw options list to the screen. If options length is greater
        than the size of the terminal, only draw a slice. Support
        scrolling through calculating the current lines position
        relative to the maximum rows available to the screen.
        '''
        self.win.erase()  # clear causes flickering in some terminals

        lines = list(self.draw_lines())[self.start:self.start + self.limit]

        for index, line in enumerate(lines):
            option, attr = line
            option = option + ' ' * (self.win_x - len(option))
            self.win.addstr(index, 0, option, attr)

        self.win.refresh()
        self.draw_header()
        self.draw_footer()

    def draw_help(self):
        msg = [
            '[k][UP]       : Move up one line.',
            '[j][DOWN]     : Move down one line.',
            '[f][PGDN]     : Jump down a page of lines.',
            '[b][PGUP]     : Jump up a page of lines.',
            '[g][HOME]     : Jump to first line.',
            '[G][END]      : Jump to last line.',
            '[s][SPC]      : Select an item and go down a line.',
            '[u][U]        : Unselect an item and go up a line.',
            '[/]           : Find items via glob pattern matching.',
            '[n][N]        : Jump to next glob match.',
            '[p][P]        : Jump to previous glob match.',
            '[t][T]        : Toggle an items selection.',
            '[a][A]        : Toggle selection of all items.',
            '[:][;]        : Toggle selection via glob pattern matching.',
            '[?][F1]       : View this help page.',
            '[q][ESC][RET] : Quit and display all marked paths.',
            '',
            'Press any key to return.'
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
        self.footer.erase()
        self.footer.addstr(0, 0, prompt, self.magenta_black())
        curses.curs_set(1)
        self.footer.refresh()
        tb = self.footer.subwin(self.y - 1, len(prompt))
        box = Textbox(tb)
        box.edit()
        curses.curs_set(0)
        result = box.gather()
        self.footer.erase()
        return result
