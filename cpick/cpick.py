import curses


class Picker:
    def __init__(self, screen, options):
        self.screen = screen
        self.options = options
        self.index = 0
        self.picked = []
        self.y, self.x = self.screen.getmaxyx()
        curses.use_default_colors()  # https://stackoverflow.com/a/44015131
        curses.init_pair(1, curses.COLOR_WHITE, -1)
        curses.init_pair(2, curses.COLOR_YELLOW, -1)
        curses.init_pair(3, 1, curses.COLOR_BLUE)
        curses.init_pair(4, 1, curses.COLOR_YELLOW)
        curses.curs_set(0)  # hide the cursor

    def up(self):
        self.index -= 1

    def dn(self):
        self.index += 1

    def pgdn(self):
        self.index += self.y - 3

    def pgup(self):
        self.index -= self.y - 3

    def top(self):
        self.index = 0

    def btm(self):
        self.index = len(self.options) - 1

    def wrap(self):
        if self.index < 0:
            self.btm()
        if self.index >= len(self.options):
            self.top()

    def pick(self):
        if self.options[self.index] in self.picked:
            self.picked.remove(self.options[self.index])
        else:
            self.picked.append(self.options[self.index])
        self.dn()

    def get_lines(self):
        indicator = '-->'
        for index, option in enumerate(self.options):
            if index == self.index and self.options[index] in self.picked:
                pad = indicator
                color = curses.color_pair(4)
            elif self.options[index] in self.picked:
                pad = ' ' * len(indicator)
                color = curses.color_pair(2)
            elif index == self.index:
                pad = indicator
                color = curses.color_pair(3)
            else:
                pad = ' ' * len(indicator)
                color = curses.color_pair(1)
            yield ('{} {}'.format(pad, option), color)

    def draw(self):
        self.screen.clear()
        x, y = 0, 1
        max_rows = self.y - (y + 1)
        curline = self.index + 1
        start, stop = 0, max_rows

        if curline - start > max_rows:
            start = curline - max_rows
            stop = start + max_rows

        lines = list(self.get_lines())[start:stop]
        for line in lines:
            option, attr = line
            option = option + ' ' * (self.x - len(option))
            self.screen.addstr(y, x, option, attr)
            y += 1
        self.screen.refresh()

    def quit(self):
        '''
        Signal to get_picked that it's time to return the state of self.picked.
        '''
        return True

    def ignore(self):
        '''
        Skip unbound key presses in main event method.
        '''
        return False

    def get_action(self):
        '''
        Uses a dictionary to map characters to methods. Get a character entered
        and return it's value from the dictionary. If we get a key error from
        this operation, return a method that returns False instead (equivalent
        to pass).
        '''
        ch = self.screen.getch()
        try:
            return {
                ord('j'): self.dn,
                ord('k'): self.up,
                ord('g'): self.top,
                ord('G'): self.btm,
                ord('f'): self.pgdn,
                ord('b'): self.pgup,
                ord(' '): self.pick,
                ord('q'): self.quit,
            }[ch]
        except KeyError:
            return self.ignore

    def get_picked(self):
        '''
        Main event loop that draws the screen, waits for input, and executes an
        action based on that input. If the method executed returns true, we
        return our objects' picked attribute.
        '''
        while True:
            self.draw()
            action = self.get_action()
            if action():
                return self.picked
            self.wrap()
