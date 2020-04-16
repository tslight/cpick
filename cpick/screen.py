"""
Curses List Picker
"""
import curses


class Screen:
    """
    Base class for initialising and updating curses.
    """

    def __init__(self, stdscr, items):
        self.stdscr = stdscr
        self.items = items
        self.maxy, self.maxx = self.stdscr.getmaxyx()
        self.color_init()
        self.head_init()
        self.foot_init()
        self.body_init()
        self.refresh()
        curses.curs_set(0)  # hide the cursor

    def color_init(self):
        """
        Initialise curses color pairs. Iterate over primary 8 bit colors adding
        colors in the form foreground_background 3 times once with all 8 colors
        in the foreground and the default terminal background as the background
        once with white as the foreground and each color as background and once
        with black as the foreground and each color as the background.
        """
        curses.use_default_colors()  # https://stackoverflow.com/a/44015131
        for i in range(1, 8):
            curses.init_pair(i, i, -1)
            curses.init_pair(i + 7, curses.COLOR_WHITE, i)
            curses.init_pair(i + 14, curses.COLOR_BLACK, i)

        self.red_black = curses.color_pair(1)
        self.green_black = curses.color_pair(2)
        self.yellow_black = curses.color_pair(3)
        self.blue_black = curses.color_pair(4)
        self.magenta_black = curses.color_pair(5)
        self.cyan_black = curses.color_pair(6)
        self.white_black = curses.color_pair(7)
        self.white_red = curses.color_pair(8)
        self.white_green = curses.color_pair(9)
        self.white_yellow = curses.color_pair(10)
        self.white_blue = curses.color_pair(11)
        self.white_magenta = curses.color_pair(12)
        self.white_cyan = curses.color_pair(13)
        self.white_white = curses.color_pair(14)
        self.black_red = curses.color_pair(15)
        self.black_green = curses.color_pair(16)
        self.black_yellow = curses.color_pair(17)
        self.black_blue = curses.color_pair(18)
        self.black_magenta = curses.color_pair(19)
        self.black_cyan = curses.color_pair(20)
        self.black_white = curses.color_pair(21)

        self.red_black_bold = curses.color_pair(1) | curses.A_BOLD
        self.green_black_bold = curses.color_pair(2) | curses.A_BOLD
        self.yellow_black_bold = curses.color_pair(3) | curses.A_BOLD
        self.blue_black_bold = curses.color_pair(4) | curses.A_BOLD
        self.magenta_black_bold = curses.color_pair(5) | curses.A_BOLD
        self.cyan_black_bold = curses.color_pair(6) | curses.A_BOLD
        self.white_black_bold = curses.color_pair(7) | curses.A_BOLD
        self.white_red_bold = curses.color_pair(8) | curses.A_BOLD
        self.white_green_bold = curses.color_pair(9) | curses.A_BOLD
        self.white_yellow_bold = curses.color_pair(10) | curses.A_BOLD
        self.white_blue_bold = curses.color_pair(11) | curses.A_BOLD
        self.white_magenta_bold = curses.color_pair(12) | curses.A_BOLD
        self.white_cyan_bold = curses.color_pair(13) | curses.A_BOLD
        self.white_white_bold = curses.color_pair(14) | curses.A_BOLD
        self.black_red_bold = curses.color_pair(15) | curses.A_BOLD
        self.black_green_bold = curses.color_pair(16) | curses.A_BOLD
        self.black_yellow_bold = curses.color_pair(17) | curses.A_BOLD
        self.black_blue_bold = curses.color_pair(18) | curses.A_BOLD
        self.black_magenta_bold = curses.color_pair(19) | curses.A_BOLD
        self.black_cyan_bold = curses.color_pair(20) | curses.A_BOLD
        self.black_white_bold = curses.color_pair(21) | curses.A_BOLD

    def head_init(self):
        """
        Initialise header window to take up top row of screen.
        """
        self.head = curses.newwin(0, self.maxx, 0, 0)
        self.head_maxy, self.head_maxx = self.head.getmaxyx()

    def foot_init(self):
        """
        Initialise footer window to take up bottom row of screen.
        """
        self.foot = curses.newwin(0, self.maxx, self.maxy - 1, 0)
        self.foot_maxy, self.foot_maxx = self.foot.getmaxyx()

    def body_init(self):
        """
        Initialise as many columns of pad windows as we need.
        """
        self.pminrow = 0  # pad row to start displaying contents at
        self.pmincol = 0  # pad col to start displaying contents at
        self.sminrow = 1  # screen row to start display of pad at
        self.smincol = 0  # screen col to start display of pad at
        self.smaxrow = self.maxy - 2  # screen row stop (bottom righthand)
        self.smaxcol = self.maxx - 2  # screen col stop (bottom righthand)
        self.maxwidth = len(max(self.items, key=len)) + 10

        self.currow = 0
        self.curcol = 1
        self.total, total = (len(self.items),) * 2
        columns = int(self.smaxcol / self.maxwidth)

        self.columns = 1
        for col in range(columns - 1):
            if total > self.smaxrow:
                total -= self.smaxrow
                self.columns += 1

        self.pmaxrow = self.smaxrow
        while self.pmaxrow * self.columns < self.total:
            self.pmaxrow += 1
        # // always returns an int, not a float
        # self.pmaxrow = self.total // self.columns

        self.screens = self.pmaxrow // self.smaxrow

        self.pads = []
        for col in range(self.columns):
            column = curses.newpad(self.maxy - 1, self.maxwidth)
            column.keypad(True)
            column.scrollok(True)
            column.idlok(True)
            self.pads.append(column)

    def refresh(self):
        """
        Call refresh on all widgets.
        """
        self.stdscr.noutrefresh()
        self.head.noutrefresh()
        for index, column in enumerate(self.pads):
            self.smincol = index * self.maxwidth
            column.resize(self.pmaxrow + self.foot_maxy, self.maxx)
            column.noutrefresh(
                self.pminrow,
                self.pmincol,
                self.sminrow,
                self.smincol,
                self.smaxrow,
                self.smaxcol,
            )
        self.foot.noutrefresh()
        curses.doupdate()

    def resize(self):
        """
        Handle terminal resizing.
        """
        self.stdscr.erase()
        self.maxy, self.maxx = self.stdscr.getmaxyx()
        self.head.resize(1, self.maxx)
        self.head_maxy, self.head_maxx = self.head.getmaxyx()
        self.foot.mvwin(self.maxy - 1, 0)
        self.foot.resize(1, self.maxx)
        self.foot_maxy, self.foot_maxx = self.foot.getmaxyx()
        self.body_init()
        self.refresh()
