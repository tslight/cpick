import curses
from curses.textpad import Textbox
from .screen import Screen


class Draw(Screen):
    def __init__(self, screen, items):
        Screen.__init__(self, screen)
        self.items = items
        self.indicator = '-->'
        self.checkbox = '[ ]'
        self.checked = '[x]'
        self.scroll = 2  # when to start scrolling
        self.start, self.curline, self.curidx = (0,)*3
        self.total = len(self.items)
        self.maxlines = self.win_y - self.footer_y
        self.pages = self.total / self.maxlines  # total pages

    def draw_header(self):
        msg = ('PICK ITEMS FROM THIS LIST:')
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

    def draw_body(self):
        self.win.erase()  # clear causes flickering in some terminals
        stop = self.start + self.maxlines
        self.curidx = self.start + self.curline
        for linum, item in enumerate(self.items[self.start:stop]):
            index = self.start + linum
            if linum == self.curline and index in self.picked:
                pad, color = self.indicator, self.black_yellow()
            elif linum == self.curline and index in self.matches:
                pad, color = self.indicator, self.black_green()
            elif index in self.picked:
                pad, color = self.checked, self.yellow_black()
            elif index in self.matches:
                pad, color = self.checkbox, self.green_black()
            elif linum == self.curline:
                pad, color = self.indicator, self.black_blue()
            else:
                pad, color = self.checkbox, self.white_black()
            line = pad + ' ' + item
            line = line + ' ' * (self.win_x - len(line))
            self.win.addstr(linum, 0, line, color)
        self.win.refresh()

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
