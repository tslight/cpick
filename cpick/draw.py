"""
Curses List Picker
"""
import cgitb
import curses
from curses.textpad import Textbox
from .screen import Screen

cgitb.enable(format="text")


class Draw(Screen):
    """
    How to draw on the screen.
    """

    def __init__(self, stdscr, items):
        super().__init__(stdscr, items)
        self.indicator = "-->"
        self.checkbox = "[ ]"
        self.checked = "[x]"

    def draw_header(self, msg):
        try:
            self.head.addstr(0, 0, msg, self.magenta_black)
            # self.head.bkgdset(self.black_magenta)
            self.head.clrtoeol()  # more frugal than erase. no flicker.
        except curses.error:
            pass

    def draw_footer(self, msg):
        try:
            self.foot.addstr(0, 0, msg, self.magenta_black)
            # self.foot.bkgdset(self.black_magenta)
            self.foot.clrtoeol()  # more frugal than erase. no flicker.
        except curses.error:
            pass

    def get_item_style(self, index):
        if index == self.currow and index in self.picked:
            return self.indicator, self.black_yellow
        elif index == self.currow and index in self.matches:
            return self.indicator, self.black_green
        elif index in self.picked:
            return self.checked, self.yellow_black
        elif index in self.matches:
            return self.checkbox, self.green_black
        elif index == self.currow:
            return self.indicator, self.white_blue_bold
        else:
            return self.checkbox, self.white_black

    def get_item_number(self, index, indicator, item):
        maxlen = len(str(self.total + 1))
        length = len(str(index + 1))
        if length <= maxlen:
            pad = " " * (maxlen - length)
            number = str(index + 1) + ")" + pad
        return number + indicator + " " + item

    def get_item(self, index, item, numbers):
        indicator, color = self.get_item_style(index)
        if numbers:
            return self.get_item_number(index, indicator, item), color
        else:
            return indicator + " " + item, color

    def draw_body(self, msg, pick=True, numbers=False):
        start, stop = 0, self.pmaxrow
        for column in self.pads:
            column.erase()
            for idx, item in enumerate(msg[start:stop]):
                index = start + idx
                if pick:
                    row, color = self.get_item(index, item, numbers)
                else:
                    row, color = item, self.white_black
                row = row + " " * (self.maxwidth - len(row))
                column.addstr(idx, 0, row, color)
            start += self.pmaxrow
            stop += self.pmaxrow

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
