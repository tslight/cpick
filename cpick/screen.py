import curses


class Screen:
    def __init__(self, screen):
        self.screen = screen
        self.y, self.x = self.screen.getmaxyx()
        self.header = curses.newwin(0, self.x, 0, 0)
        self.win = curses.newwin(self.y - 3, self.x, 2, 0)
        self.win_y, self.win_x = self.win.getmaxyx()
        self.footer = curses.newwin(0, self.x, self.y - 1, 0)
        self.screen.refresh()
        self.win.refresh()
        self.pad = curses.newpad(self.y, self.x)
        self.footer.refresh()
        self.header.refresh()
        self.lc, self.pos = (0,)*2
        self.curses_init()

    def curses_init(self):
        curses.use_default_colors()  # https://stackoverflow.com/a/44015131
        curses.init_pair(1, curses.COLOR_WHITE, -1)
        curses.init_pair(2, curses.COLOR_YELLOW, -1)
        curses.init_pair(3, curses.COLOR_MAGENTA, -1)
        curses.init_pair(4, 1, curses.COLOR_BLUE)
        curses.init_pair(5, 1, curses.COLOR_YELLOW)
        curses.init_pair(6, 1, curses.COLOR_MAGENTA)
        curses.curs_set(0)  # hide the cursor

    def white_black(self):
        return curses.color_pair(1)

    def yellow_black(self):
        return curses.color_pair(2)

    def magenta_black(self):
        return curses.color_pair(3)

    def black_blue(self):
        return curses.color_pair(4)

    def black_yellow(self):
        return curses.color_pair(5)

    def resize(self):
        self.screen.erase()
        self.y, self.x = self.screen.getmaxyx()
        self.header.resize(1, self.x)
        self.win.resize(self.y - 3, self.x)
        self.win_y, self.win_x = self.win.getmaxyx()
        if self.lc:
            self.pad.resize(self.lc + 2, self.x)
        self.footer.mvwin(self.y - 1, 0)
        self.footer.resize(1, self.x)
        self.screen.refresh()
        self.header.refresh()
        self.win.refresh()
        self.footer.refresh()
