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
        self.maxy, self.maxx = self.screen.getmaxyx()
        self.color_init()
        self.head_init()
        self.foot_init()
        self.body_init()
        self.refresh()
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
        self.head = curses.newwin(0, self.maxx, 0, 0)
        self.head_maxy, self.head_maxx = self.head.getmaxyx()

    def foot_init(self):
        '''
        Initialise footer window to take up bottom line of screen.
        '''
        self.foot = curses.newwin(0, self.maxx, self.maxy - 1, 0)
        self.foot_maxy, self.foot_maxx = self.foot.getmaxyx()

    def body_init(self):
        '''
        Initialise pad window for help page.
        '''
        self.body = curses.newpad(self.maxy - 1, self.maxx)
        self.body.keypad(True)
        self.body.scrollok(True)
        self.body.idlok(True)
        self.body_maxy, self.body_maxx = self.body.getmaxyx()
        self.curline = 0
        self.maxline = len(self.items)
        self.pminrow = 0  # pad row to start displaying contents at
        self.pmincol = 0  # pad col to start displaying contents at
        self.sminrow = 1  # screen row to start display of pad at
        self.smincol = 0  # screen col to start display of pad at
        self.smaxrow = self.maxy - 2  # screen row stop
        self.smaxcol = self.body_maxx  # screen col stop

    def refresh(self):
        '''
        Call refresh on all widgets.
        '''
        self.screen.refresh()
        self.head.refresh()
        self.body.refresh(self.pminrow,
                          self.pmincol,
                          self.sminrow,
                          self.smincol,
                          self.smaxrow,
                          self.smaxcol)
        self.foot.refresh()

    def resize(self):
        '''
        Handle terminal resizing.
        '''
        self.screen.erase()
        self.maxy, self.maxx = self.screen.getmaxyx()

        self.head.resize(1, self.maxx)
        self.head_maxy, self.head_maxx = self.head.getmaxyx()

        self.foot.mvwin(self.maxy - 1, 0)
        self.foot.resize(1, self.maxx)
        self.foot_maxy, self.foot_maxx = self.foot.getmaxyx()

        self.body.resize(self.maxline + self.foot_maxy, self.maxx)
        self.body_maxy, self.body_maxx = self.body.getmaxyx()
        self.smaxrow = self.maxy - 2
        self.smaxcol = self.body_maxx  # screen col stop

        self.refresh()
