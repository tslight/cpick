import curses
from .action import Action


class Event(Action):
    def __init__(self, screen, options):
        Action.__init__(self, screen)
        self.options = options

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
                ord('?'): self.draw_help,
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
            self.draw_body()
            action = self.get_action()
            if action():
                return self.picked
            self.wrap()
