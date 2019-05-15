'''
Curses List Picker
'''
from fnmatch import fnmatch
from pathlib import Path
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

    def up_win(self):
        if self.pos > 0:
            self.pos -= 1

    def down_win(self):
        if self.pos < self.lc - self.y + 2:
            self.pos += 1

    def pgdn_win(self):
        self.pos += self.y - 1
        if self.pos >= self.lc - self.y + 2:
            self.pos = self.lc - self.y + 2

    def pgup_win(self):
        self.pos -= self.y - 1
        if self.pos < 0:
            self.pos = 0

    def top_win(self):
        self.pos = 0

    def bottom_win(self):
        self.pos = self.total - self.maxlines

    ###########################################################################
    #                              LINE MOVEMENTS                             #
    ###########################################################################

    def down_line(self):
        if self.curline >= self.total - 1:
            self.top_line()
        elif self.curline >= self.pos + self.maxlines:
            self.pos += 1  # scroll screen
            self.curline += 1
        else:
            self.curline += 1  # scroll cursor

    def up_line(self):
        if self.curline < 1:
            self.bottom_line()
        if self.curline <= self.pos:
            self.pos -= 1
            self.curline -= 1
        else:
            self.curline -= 1

    def pgdn_line(self):
        self.pos += self.maxlines
        self.curline += self.maxlines
        if self.pos >= self.total - self.maxlines:
            self.bottom_line()

    def pgup_line(self):
        self.pos -= self.maxlines
        self.curline -= self.maxlines
        if self.pos <= 0:
            self.top_line()

    def top_line(self):
        self.pos, self.curline = (0,)*2

    def bottom_line(self):
        self.pos = self.total - self.maxlines
        self.curline = self.total

    def recenter_line(self):
        middle = int(self.maxlines / 2)
        curline = self.curline - self.pos
        if curline > middle and self.pos < self.total - self.maxlines:
            self.pos += curline - middle
            self.curline += curline - middle
        elif curline < middle and self.pos > self.maxlines:
            self.pos -= curline - middle
            self.curline -= curline - middle

    ###########################################################################
    #                                  OTHER                                  #
    ###########################################################################

    def reset(self):
        self.picked = []
        self.matches = []

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

    def pick(self, index, matches):
        if index not in matches:
            matches.append(index)

    def undo(self):
        if self.picked:
            del self.picked[-1]

    def toggle(self, index, matches):
        if index in matches:
            matches.remove(index)
        else:
            matches.append(index)

    def toggle_all(self):
        if len(self.picked) == len(self.items):
            self.picked = []
        else:
            self.picked = [i for i, o in enumerate(self.items)]

    def match(self, msg, matches, method):
        search = self.draw_textbox(msg).strip().split()
        for index, item in enumerate(self.items):
            for pattern in search:
                try:
                    if match(pattern, item):
                        method(index, matches)
                except error:
                    if fnmatch(item, pattern) or pattern == item:
                        method(index, matches)
        self.range(search, matches, method)
        if matches:
            self.goto_next(matches)

    def range(self, ranges, matches, method):
        start, stop = (0,) * 2
        for numbers in ranges:
            if match('^\\d+\\.\\.\\d+$', numbers):
                start, stop = numbers.split('..')
            elif match('^\\d+\\-\\d+$', numbers):
                start, stop = numbers.split('-')
            elif match('^\\d+\\.\\.$', numbers):
                start, stop = numbers.split('..')[0], self.total
            elif match('^\\d+\\-$', numbers):
                start, stop = numbers.split('-')[0], self.total
            elif match('^\\.\\.\\d+$', numbers):
                start, stop = 1, numbers.split('..')[1]
            elif match('^\\-\\d+$', numbers):
                start, stop = 1, numbers.split('-')[1]
            elif match('^\\d+$', numbers):
                start, stop = (numbers,) * 2
            if start and stop:
                for index in range(int(start) - 1, int(stop)):
                    method(index, matches)

    def save(self):
        path = self.draw_textbox("Save to: ").strip()
        home = str(Path.home())
        path = home + "/" + path
        out = None
        try:
            # removes need to use f.close
            with open(path, 'a+') as f:
                for pick in self.picked:
                    f.write(self.items[pick] + '\n')
        except FileNotFoundError:
            out = "Can't find " + path
        except IsADirectoryError:
            out = path + " is a directory."
        except UnboundLocalError:  # bit of a hack but fuck it
            out = "Not saving fortune."
        except Exception:
            out = "Something went wrong..."
        else:
            out = "Saved fortune to " + path
        finally:
            return out

    def quit(self):
        '''
        Signal to pick() that it's time to return the state of self.picked.
        '''
        return 'quit'
