'''
Curses List Picker
'''
import cgitb
import curses
from curses.textpad import Textbox
from .screen import Screen
cgitb.enable(format='text')


class Draw(Screen):
    '''
    How to draw on the screen.
    '''

    def __init__(self, screen, items):
        Screen.__init__(self, screen)
        self.items = items
        self.indicator = '-->'
        self.checkbox = '[ ]'
        self.checked = '[x]'
        self.scroll = 2  # when to start scrolling
        self.start, self.curline, self.curidx = (0,)*3
        self.total = len(self.items)
        self.maxlines = self.win_y - self.foot_y
        self.pages = self.total / self.maxlines  # total pages

    def draw_header(self, msg):
        try:
            self.head.addstr(0, 0, msg, self.magenta_black)
            self.head.clrtoeol()  # more frugal than erase. no flicker.
        except curses.error:
            pass

    def draw_footer(self, msg):
        try:
            self.foot.addstr(0, 0, msg, self.magenta_black)
            self.foot.clrtoeol()  # more frugal than erase. no flicker.
        except curses.error:
            pass

    def draw_body(self, show_numbers=False):
        self.win.erase()  # clear causes flickering in some terminals
        self.pad.resize(self.total + 2, self.x)
        number = ''
        self.curidx = self.start + self.curline
        for linum, item in enumerate(self.items):
            index = self.start + linum
            if linum == self.curline and index in self.picked:
                indicator, color = self.indicator, self.black_yellow
            elif linum == self.curline and index in self.matches:
                indicator, color = self.indicator, self.black_green
            elif index in self.picked:
                indicator, color = self.checked, self.yellow_black
            elif index in self.matches:
                indicator, color = self.checkbox, self.green_black
            elif linum == self.curline:
                indicator, color = self.indicator, self.black_blue
            else:
                indicator, color = self.checkbox, self.white_black
            if show_numbers:
                maxlen = len(str(self.total + 1))
                length = len(str(index + 1))
                if length < maxlen:
                    pad = ' ' * (maxlen - length)
                    number = str(index + 1) + ')' + pad
            line = number + indicator + ' ' + item
            line = line + ' ' * (self.win_x - len(line))
            self.win.addstr(linum, 0, line, color)
        self.win.refresh(self.pos, 0, 1, 0, self.y - 1, self.x - 2)

    def draw_pad(self, msg):
        self.lc = len(msg)
        self.screen.erase()
        self.pad.clrtoeol()
        self.pad.resize(self.lc + 2, self.x)
        for index, line in enumerate(msg):
            if index == self.curline and index in self.picked:
                indicator, color = self.indicator, self.black_yellow
            elif index == self.curline and index in self.matches:
                indicator, color = self.indicator, self.black_green
            elif index in self.picked:
                indicator, color = self.checked, self.yellow_black
            elif index in self.matches:
                indicator, color = self.checkbox, self.green_black
            elif index == self.curline:
                indicator, color = self.indicator, self.black_blue
            else:
                indicator, color = self.checkbox, self.white_black
            line = indicator + ' ' + line
            self.pad.addstr(index, 0, line, color)
        self.pad.scrollok(1)
        self.pad.idlok(1)

    def draw_textbox(self, prompt):
        self.foot.erase()
        self.foot.addstr(0, 0, prompt, self.magenta_black)
        curses.curs_set(1)
        self.foot.refresh()
        tb = self.foot.subwin(self.y - 1, len(prompt))
        box = Textbox(tb)
        box.edit()
        curses.curs_set(0)
        result = box.gather()
        self.foot.erase()
        return result
