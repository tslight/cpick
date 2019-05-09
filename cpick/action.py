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
        if self.start > 0 and self.curline == 0:
            self.start -= 1  # scroll screen
        elif self.start > 0 or self.curline > 0:
            self.curline -= 1  # scroll cursor

    def dn(self):
        '''
        If the next line would hit the limit and we're not at the end of the
        list, scroll the screen. If the next line position is less than the
        limit and the end of the list is not in sight, scroll the cursor down.
        '''
        next_line = self.curline + 1
        if (next_line == self.maxlines and
                self.start + self.maxlines < self.total):
            self.start += 1  # scroll screen
        elif (next_line < self.maxlines and
              self.start + next_line < self.total):
            self.curline += 1  # scroll cursor

    def pgdn(self):
        '''
        If current page is less than total pages, increment start line by
        maximum line amount. Using min with the last possible stop position
        catches cases where self.start + self.maxlines exceeds self.total.
        '''
        page = (self.start + self.curline) / self.maxlines
        if page < self.pages:
            self.start = min(self.total - self.maxlines,
                             self.start + self.maxlines)

    def pgup(self):
        '''
        If current page is not the first page, start line is the either the
        first line or the current start line minus the maximum number of lines
        the page holds. Using max with 0, catches cases where self.start -
        self.maxlines returns a negative.
        '''
        page = (self.start + self.curline) / self.maxlines
        if page > 0:
            self.start = max(0, self.start - self.maxlines)

    def top(self):
        '''
        Jump to top by resetting start and curline attributes to 0.
        '''
        self.start, self.curline = (0,)*2

    def btm(self):
        self.start = self.total - self.maxlines
        self.curline = self.maxlines - 1

    def recenter(self):
        pass

    def goto_number(self, number):
        if (number <= 1):
            self.top()
            return
        elif (number >= self.total - 1):
            self.btm()
            return
        elif (number >= (self.start + self.maxlines)):
            self.start = number - self.curline
        elif (number <= self.start):
            self.start = number - self.curline
        self.curline = number - self.start

    def goto(self, prompt="Enter a line number: "):
        try:
            number = int(self.draw_textbox(prompt)) - 1
            self.goto_number(number)
        except ValueError:
            self.goto("Invalid input! Enter a number: ")

    def find(self):
        self.matches = []
        globs = self.draw_textbox("Find: ").strip().split()
        for index, option in enumerate(self.options):
            for glob in globs:
                if fnmatch(option, glob):
                    self.matches.append(index)
        if self.matches:
            self.findnext()

    def findnext(self):
        for m in self.matches:
            if self.start + self.curline < m:
                self.goto_number(m)
                break

    def findprev(self):
        for m in reversed(self.matches):
            if self.start + self.curline > m:
                self.goto_number(m)
                break

    def toggle(self):
        if self.options[self.curline] in self.picked:
            self.picked.remove(self.options[self.curline])
        else:
            self.picked.append(self.options[self.curline])

    def toggle_all(self):
        if self.picked == self.options:
            self.picked = []
        else:
            self.picked = self.options

    def toggle_globs(self):
        globs = self.draw_textbox("Pick: ").strip().split()
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
