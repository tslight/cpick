'''
Curses List Picker
'''
from fnmatch import fnmatch
from re import match, error
from .draw import Draw


class Action(Draw):
    '''
    What to draw on the screen.
    '''

    def __init__(self, screen, items):
        Draw.__init__(self, screen, items)
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

    def top(self):
        '''
        Jump to top by resetting start and curline attributes to 0.
        '''
        self.start, self.curline = (0,)*2

    def btm(self):
        '''
        Jump to bottom by moving the start to the total - maxlines and current
        line to maxlines - 1.
        '''
        self.start = self.total - self.maxlines
        self.curline = self.maxlines - 1

    def pgdn(self):
        '''
        If current page is less than total pages, increment start line by
        maximum line amount. Using min with the last possible stop position
        catches cases where self.start + self.maxlines exceeds self.total.
        '''
        page = (self.start + self.curline) / self.maxlines
        if page < self.pages - 1:
            self.start = min(self.total - self.maxlines,
                             self.start + self.maxlines)
        else:
            self.btm()

    def pgup(self):
        '''
        If current page is not the first page, start line is the either the
        first line or the current start line minus the maximum number of lines
        the page holds. Using max with 0, catches cases where self.start -
        self.maxlines returns a negative.
        '''
        page = (self.start + self.curline) / self.maxlines
        if page > 1:
            self.start = max(0, self.start - self.maxlines)
        else:
            self.top()

    def reset(self):
        self.picked = []
        self.matches = []

    def recenter(self):
        middle = int(self.maxlines / 2) - 1
        if self.curline > middle and self.start < self.total - self.maxlines:
            self.start += self.curline - middle
            self.curline = middle
        elif self.curline < middle and self.start > self.maxlines:
            self.start -= self.curline + middle
            self.curline = middle

    def goto_next(self, items):
        if items:
            for i in items:
                if self.start + self.curline < i:
                    self.goto_number(i)
                    return
            self.top()
            self.goto_next(items)

    def goto_prev(self, items):
        if items:
            for i in reversed(items):
                if self.start + self.curline > i:
                    self.goto_number(i)
                    return
            self.btm()
            self.goto_prev(items)

    def goto_number(self, number):
        if (number <= 0):
            self.top()
            return
        elif (number >= self.total):
            self.btm()
            return
        elif (number > (self.total - self.maxlines)):
            self.start = self.total - self.maxlines
        elif (number < self.maxlines):
            self.start = 0
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
        search = self.draw_textbox("Find: ").strip().split()
        for index, item in enumerate(self.items):
            for pattern in search:
                try:
                    if match(pattern, item):
                        self.matches.append(index)
                except error:
                    if fnmatch(item, pattern) or pattern in item:
                        self.matches.append(index)
        if self.matches:
            self.goto_next(self.matches)

    def toggle(self, index):
        if index in self.picked:
            self.picked.remove(index)
        else:
            self.picked.append(index)

    def toggle_all(self):
        if len(self.picked) == len(self.items):
            self.picked = []
        else:
            self.picked = [i for i, o in enumerate(self.items)]

    def toggle_pattern(self):
        search = self.draw_textbox("Pick: ").strip().split()
        for index, item in enumerate(self.items):
            for pattern in search:
                try:
                    if match(pattern, item):
                        self.toggle(index)
                except error:
                    if fnmatch(item, pattern) or pattern in item:
                        self.toggle(index)
        if self.picked:
            self.goto_next(self.picked)

    def toggle_range(self):
        ranges = self.draw_textbox("Range: ").strip().split()
        for r in ranges:
            if match('^\d+\.\.\d+$', r):
                start, stop = r.split('..')
            elif match('^\d+\-\d+$', r):
                start, stop = r.split('-')
            elif match('^\d+\.\.$', r):
                start, stop = r.split('..')[0], self.total
            elif match('^\d+\-$', r):
                start, stop = r.split('-')[0], self.total
            elif match('^\.\.\d+$', r):
                start, stop = 1, r.split('..')[1]
            elif match('^\-\d+$', r):
                start, stop = 1, r.split('-')[1]
            elif match('^\d+$', r):
                start, stop = (r,)*2
            else:
                return
            for index in range(int(start) - 1, int(stop)):
                self.toggle(index)
        if self.picked:
            self.goto_next(self.picked)

    ###########################################################################
    #                           PAD MOVEMENT METHODS                          #
    ###########################################################################

    def pad_dn(self):
        if self.pos < self.lc - self.y + 1:
            self.pos += 1

    def pad_up(self):
        if self.pos > 0:
            self.pos -= 1

    def pad_pgdn(self):
        self.pos += self.y - 1
        if self.pos >= self.lc - self.y + 1:
            self.pos = self.lc - self.y + 1

    def pad_pgup(self):
        self.pos -= self.y - 1
        if self.pos < 0:
            self.pos = 0

    def quit(self):
        '''
        Signal to pick() that it's time to return the state of self.picked.
        '''
        return True
