import curses
from .action import Action


class Picker(Action):
    def __init__(self, screen, options):
        Action.__init__(self, screen)
        self.options = options
        self.indicator = '-->'
        self.checkbox = '[ ]'
        self.checked = '[x]'
        self.scroll = 2  # when to start scrolling

    def get_lines(self):
        '''
        Generator function that yields tuples of each option with an
        indicator prepended to the string or an empty string of the same
        length and a curses color set.
        '''
        for index, option in enumerate(self.options):
            if index == self.index and self.options[index] in self.picked:
                pad = self.indicator
                color = self.black_yellow()
            elif self.options[index] in self.picked:
                pad = self.checked
                color = self.yellow_black()
            elif index == self.index:
                pad = self.indicator
                color = self.black_blue()
            else:
                pad = self.checkbox
                color = self.white_black()
            yield ('{} {}'.format(pad, option), color)

    def draw(self):
        '''
        Draw options list to the screen. If options length is greater
        than the size of the terminal, only draw a slice. Support
        scrolling through calculating the current lines position
        relative to the maximum rows available to the screen.
        '''
        self.win.erase()  # clear causes flickering in some terminals
        self.curline = self.index + 1
        self.limit = self.win_y - 1
        self.start, self.stop = 0, self.limit

        if self.curline - self.start > self.limit - self.scroll:
            self.start = self.curline - self.limit + self.scroll
            self.stop = self.start + self.limit

        lines = list(self.get_lines())[self.start:self.stop]

        for index, line in enumerate(lines):
            option, attr = line
            option = option + ' ' * (self.win_x - len(option))
            self.win.addstr(index, 0, option, attr)

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
                ord(':'): self.toggle_globs,
                ord('/'): self.find,
                ord('n'): self.findnext,
                ord('p'): self.findprev,
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
