from .color import Color
from .action import Action


class Picker(Color, Action):
    def __init__(self, screen, options):
        Color.__init__(self)
        Action.__init__(self)
        self.screen = screen
        self.options = options
        self.y, self.x = self.screen.getmaxyx()

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

        '''
        self.screen.erase()
        x, y = 0, 1  # starting screen co-ordinates
        max_rows = self.y - (y + 1)  # leave space at top and bottom of screen
        curline = self.index + 1  # screen lines don't index from 0
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
                ord('t'): self.toggle,
                ord(' '): lambda: self.toggle() or self.dn(),
                ord('u'): lambda: self.up() or self.toggle(),
                ord('a'): self.toggle_all,
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
