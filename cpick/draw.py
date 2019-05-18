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
        Screen.__init__(self, screen, items)
        self.indicator = '-->'
        self.checkbox = '[ ]'
        self.checked = '[x]'

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

    def draw_body(self, msg, pick=True, numbers=False):
        self.maxline = len(msg)
        self.body.erase()
        self.body.resize(self.maxline + self.foot_maxy, self.maxx)
        for index, item in enumerate(msg):
            if pick:
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
                if numbers:
                    maxlen = len(str(self.maxline + 1))
                    length = len(str(index + 1))
                    if length <= maxlen:
                        pad = ' ' * (maxlen - length)
                        number = str(index + 1) + ')' + pad
                    line = number + indicator + ' ' + item
                else:
                    line = indicator + ' ' + item
            else:
                line, color = item, self.white_black
            line = line + ' ' * (self.body_maxx - len(line))
            self.body.addstr(index, 0, line, color)

    def draw_textbox(self, prompt):
        self.foot.erase()
        self.foot.addstr(0, 0, prompt, self.magenta_black)
        curses.curs_set(1)
        self.foot.refresh()
        tb = self.foot.subwin(self.maxy - 1, len(prompt))
        box = Textbox(tb)
        box.edit()
        curses.curs_set(0)
        result = box.gather()
        self.foot.erase()
        return result
