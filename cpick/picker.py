import curses
from .action import Action
from .screen import Screen


class Picker(Action, Screen):
    def __init__(self, screen, options):
        Action.__init__(self)
        Screen.__init__(self, screen)
        self.options = options

    def get_lines(self):
        '''
        Generator function that yields tuples of each option with an
        indicator prepended to the string or an empty string of the same
        length and a curses color set.
        '''
        indicator = '-->'
        for index, option in enumerate(self.options):
            if index == self.index and self.options[index] in self.picked:
                pad = indicator
                color = self.black_yellow()
            elif self.options[index] in self.picked:
                pad = ' ' * len(indicator)
                color = self.yellow_black()
            elif index == self.index:
                pad = indicator
                color = self.black_blue()
            else:
                pad = ' ' * len(indicator)
                color = self.white_black()
            yield ('{} {}'.format(pad, option), color)

    def draw(self):
        '''
        Draw options list to the screen. If options length is greater
        than the size of the terminal, only draw a slice. Support
        scrolling through calculating the current lines position
        relative to the maximum rows available to the screen
        '''
        self.win.erase()  # clear causes flickering in some terminals
        y, x = 0, 0   # starting screen co-ordinates
        # leave space at top and bottom of screen
        max_rows = self.win_y - 1
        curline = self.index + 1  # screen lines don't index from 0
        start, stop = 0, max_rows

        if curline - start > max_rows:
            start = curline - max_rows
            stop = start + max_rows

        lines = list(self.get_lines())[start:stop]
        for line in lines:
            option, attr = line
            option = option + ' ' * (self.win_x - len(option))
            self.win.addstr(y, x, option, attr)
            y += 1
        self.win.refresh()
        self.mkheader()
        self.mkfooter()

    def get_action(self):
        '''
        Uses a dictionary to map characters to methods. Get a character entered
        and return it's value from the dictionary. If we get a key error from
        this operation, return a method that returns False instead (equivalent
        to pass).
        '''
        ch = self.win.getch()
        try:
            return {
                ord('j'): self.dn,
                ord('k'): self.up,
                ord('g'): self.top,
                ord('G'): self.btm,
                ord('f'): self.pgdn,
                ord('b'): self.pgup,
                ord('t'): self.toggle,
                ord('s'): lambda: self.toggle() or self.dn(),
                ord('u'): lambda: self.up() or self.toggle(),
                ord('a'): self.toggle_all,
                ord('?'): self.mkhelp,
                ord('q'): self.quit,
                curses.KEY_RESIZE: self.resize,
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
