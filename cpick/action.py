from fnmatch import fnmatch
from .draw import Draw


class Action(Draw):
    def __init__(self, screen, options):
        Draw.__init__(self, screen, options)
        self.picked = []
        self.matches = []

    def up(self):
        '''
        If start of screen is greater that zero and current line is 0, then
        scroll screen up. If start of screen is greater than zero or current
        line is greater than zero, then scroll cursor down.
        '''
        if self.start > 0 and self.index == 0:
            self.start -= 1  # scroll screen
        elif self.start > 0 or self.index > 0:
            self.index -= 1  # scroll cursor

    def dn(self):
        '''
        If the next line would hit the limit and we're not at the end of the
        list, scroll the screen. If the next line position is less than the
        limit and the end of the list is not in sight, scroll the cursor down.
        '''
        next_line = self.index + 1
        if (next_line == self.limit and
                self.start + self.limit < self.stop):
            self.start += 1  # scroll screen
        elif (next_line < self.limit and
              self.start + next_line < self.stop):
            self.index += 1  # scroll cursor

    def pgdn(self):
        # if current page is not a last page, page down is possible
        current_page = (self.start + self.index) / self.limit
        if current_page < self.page:
            self.start += self.limit

    def pgup(self):
        # if current page is not a first page, page up is possible top position
        # can not be negative, so if top position is going to be negative, we
        # should set it as 0
        current_page = (self.start + self.index) / self.limit
        if current_page > 0:
            self.start = max(0, self.start - self.limit)

    def top(self):
        self.index = 0

    def btm(self):
        self.index = len(self.options) - 1

    def recenter(self):
        pass

    def wrap(self):
        if self.index < 0:
            self.btm()
        if self.index >= len(self.options):
            self.top()

    def find(self):
        globs = self.draw_textbox("Find: ").strip().split()
        if globs:
            self.matches = []
            line = 0
            for option in self.options:
                for glob in globs:
                    if fnmatch(option, glob):
                        self.matches.append(line)
                line += 1
            if self.matches:
                self.findnext()

    def findnext(self):
        for m in range(len(self.matches)):
            if self.index == self.matches[len(self.matches) - 1]:
                self.index = self.matches[0]
                break
            elif self.index < self.matches[m]:
                self.index = self.matches[m]
                break

    def findprev(self):
        for m in range(len(self.matches)):
            if self.index <= self.matches[m]:
                self.index = self.matches[m-1]
                break

    def toggle(self):
        if self.options[self.index] in self.picked:
            self.picked.remove(self.options[self.index])
        else:
            self.picked.append(self.options[self.index])

    def toggle_all(self):
        if self.picked == self.options:
            self.picked = []
        else:
            self.picked = self.options

    def toggle_globs(self):
        globs = self.draw_textbox("Pick: ").strip().split()
        if globs:
            for option in self.options:
                for glob in globs:
                    if fnmatch(option, glob):
                        if option in self.picked:
                            self.picked.remove(option)
                        else:
                            self.picked.append(option)

    def quit(self):
        '''
        Signal to pick() that it's time to return the state of self.picked.
        '''
        return True
