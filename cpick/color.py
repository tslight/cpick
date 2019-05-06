import curses


class Color:
    def __init__(self):
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
