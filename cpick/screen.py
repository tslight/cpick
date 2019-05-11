'''
Curses List Picker
'''
import curses


class Screen:
    '''
    Base class that configures curses & makes setting color attributes less
    clunky.
    '''

    def __init__(self, screen):
        self.screen = screen
        self.y, self.x = self.screen.getmaxyx()
        self.curses_init()
        self.head_init()
        self.win_init()
        self.foot_init()
        self.pad_init()
        self.refresh()

    def curses_init(self):
        '''
        Initialise colors and curses settings.
        '''
        curses.use_default_colors()  # https://stackoverflow.com/a/44015131
        curses.init_pair(1, curses.COLOR_WHITE, -1)
        curses.init_pair(2, curses.COLOR_YELLOW, -1)
        curses.init_pair(3, curses.COLOR_MAGENTA, -1)
        curses.init_pair(4, curses.COLOR_GREEN, -1)
        curses.init_pair(5, curses.COLOR_CYAN, -1)
        curses.init_pair(6, 1, curses.COLOR_BLUE)
        curses.init_pair(7, 1, curses.COLOR_YELLOW)
        curses.init_pair(8, 1, curses.COLOR_MAGENTA)
        curses.init_pair(9, 1, curses.COLOR_GREEN)
        curses.init_pair(10, 1, curses.COLOR_CYAN)
        curses.curs_set(0)  # hide the cursor

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
        self.win = curses.newwin(self.y - 3, self.x, 2, 0)
        self.win_y, self.win_x = self.win.getmaxyx()
        self.win.keypad(True)

    def pad_init(self):
        '''
        Initialise pad window for help page.
        '''
        self.pad = curses.newpad(self.y - 3, self.x)
        self.lc, self.pos = (0,)*2

    def refresh(self):
        '''
        Call refresh on all curses components.
        '''
        self.screen.refresh()
        self.head.refresh()
        self.win.refresh()
        self.foot.refresh()

    def resize(self):
        '''
        Handle terminal resizing.
        '''
        self.screen.erase()
        self.y, self.x = self.screen.getmaxyx()
        self.head.resize(1, self.x)
        self.win.resize(self.y - 3, self.x)
        self.win_y, self.win_x = self.win.getmaxyx()
        if self.lc:
            self.pad.resize(self.lc + 2, self.x)
        self.maxlines = self.win_y - self.foot_y
        self.foot.mvwin(self.y - 1, 0)
        self.foot.resize(1, self.x)
        self.screen.refresh()
        self.head.refresh()
        self.win.refresh()
        self.foot.refresh()

    def white_black(self):
        '''
        White foreground, black background.
        '''
        return curses.color_pair(1)

    def yellow_black(self):
        '''
        Yellow foreground, black background.
        '''
        return curses.color_pair(2)

    def magenta_black(self):
        '''
        Magenta foreground, black background.
        '''
        return curses.color_pair(3)

    def green_black(self):
        '''
        Green foreground, black background.
        '''
        return curses.color_pair(4)

    def cyan_black(self):
        '''
        Cyan foreground, black background.
        '''
        return curses.color_pair(5)

    def black_blue(self):
        '''
        Black foreground, blue background.
        '''
        return curses.color_pair(6)

    def black_yellow(self):
        '''
        Black foreground, yellow background.
        '''
        return curses.color_pair(7)

    def black_magenta(self):
        '''
        Black foreground, magenta background.
        '''
        return curses.color_pair(8)

    def black_green(self):
        '''
        Black foreground, green background.
        '''
        return curses.color_pair(9)

    def black_cyan(self):
        '''
        Black foreground, cyan background.
        '''
        return curses.color_pair(10)
