'''
Curses List Picker
'''
import curses


class Screen:
    '''
    Base class that configures curses, makes setting color attributes less
    clunky and sets up the initial window layout with a header window, a footer
    window and two main body windows - one a pad for statically scrolling and
    one a normal window for dynamic scrolling.
    '''

    def __init__(self, screen, items):
        self.screen = screen
        self.items = items
        self.y, self.x = self.screen.getmaxyx()
        self.scroll = 2  # when to start scrolling
        self.start, self.curline, self.curidx = (0,)*3
        self.total = len(self.items)
        self.maxwidth = len(max(self.items, key=len)) + 20
        self.maxcolumns = int(self.x / self.maxwidth)
        self.color_init()
        self.head_init()
        self.foot_init()
        self.pad_init()
        self.refresh()
        self.maxlines = self.y - self.foot_y - 1
        self.pages = self.total / self.maxlines  # total pages
        self.win_init()
        curses.curs_set(0)  # hide the cursor

    def color_init(self):
        '''
        Initialise curses color pairs. Iterate over primary 8 bit colors adding
        colors in the form foreground_background 3 times once with all 8 colors
        in the foreground and the default terminal background as the background
        once with white as the foreground and each color as background and once
        with black as the foreground and each color as the background.
        '''
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

    def head_init(self):
        '''
        Initialise header window to take up top line of screen.
        '''
        self.head = curses.newwin(0, self.x, 0, 0)
        self.head_y, self.head_x = self.head.getmaxyx()

    def foot_init(self):
        '''
        Initialise footer window to take up bottom line of screen.
        '''
        self.foot = curses.newwin(0, self.x, self.y - 1, 0)
        self.foot_y, self.foot_x = self.foot.getmaxyx()

    def win_init(self):
        '''
        Initialise main window that takes up the rest of the screen.
        '''
        self.windows = []
        self.columns = 1
        total = self.total
        for n in range(self.maxcolumns):
            if total > self.maxlines:
                total = total - self.maxlines
                self.columns += 1
        for col in range(self.columns):
            win = curses.newpad(self.y - 1, self.maxwidth)
            self.windows.append(win)

    def pad_init(self):
        '''
        Initialise pad window for help page.
        '''
        self.pad = curses.newpad(self.y - 1, self.x)
        self.lc, self.pos = (0,)*2

    def refresh(self):
        '''
        Call refresh on all curses components.
        '''
        self.screen.refresh()
        self.head.refresh()
        self.pad.refresh(self.pos, 0, 1, 0, self.y - 1, self.x - 2)
        # self.win.refresh()
        self.foot.refresh()

    def resize(self):
        '''
        Handle terminal resizing.
        '''
        self.screen.erase()
        self.y, self.x = self.screen.getmaxyx()
        self.head.resize(1, self.x)
        self.win.resize(self.y - 1, self.x)
        self.win_y, self.win_x = self.win.getmaxyx()
        if self.lc:
            self.pad.resize(self.lc + 2, self.x)
            self.maxlines = self.win_y - self.foot_y
            self.foot.mvwin(self.y - 1, 0)
            self.foot.resize(1, self.x)
            self.refresh()
