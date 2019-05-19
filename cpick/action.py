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

    ###########################################################################
    #                             WINDOW MOVEMENT                             #
    ###########################################################################

    def up_win(self):
        if self.pminrow > 0:
            self.pminrow -= 1

    def down_win(self):
        if self.pminrow < self.maxline - self.smaxrow:
            self.pminrow += 1

    def pgdn_win(self):
        self.pminrow += self.smaxrow
        if self.pminrow >= self.maxline - self.smaxrow:
            self.pminrow = self.maxline - self.smaxrow

    def pgup_win(self):
        self.pminrow -= self.maxy - 1
        if self.pminrow < 0:
            self.pminrow = 0

    def top_win(self):
        self.pminrow = 0

    def bottom_win(self):
        self.pminrow = self.maxline - self.smaxrow

    ###########################################################################
    #                              LINE MOVEMENT                              #
    ###########################################################################

    def down_line(self):
        if self.curline >= self.maxline - 1:
            self.top_line()
        elif self.curline >= self.pminrow + self.smaxrow - 1:
            self.pminrow += 1  # scroll screen
            self.curline += 1
        else:
            self.curline += 1  # scroll cursor

    def up_line(self):
        if self.curline < 1:
            self.bottom_line()
        elif self.curline <= self.pminrow:
            self.pminrow -= 1
            self.curline -= 1
        else:
            self.curline -= 1

    def pgdn_line(self):
        self.pminrow += self.smaxrow
        self.curline += self.smaxrow
        if self.pminrow >= self.maxline - self.smaxrow:
            self.bottom_line()

    def pgup_line(self):
        self.pminrow -= self.smaxrow
        self.curline -= self.smaxrow
        if self.pminrow <= 0:
            self.top_line()

    def top_line(self):
        self.pminrow, self.curline = (0,)*2

    def bottom_line(self):
        self.pminrow = self.maxline - self.smaxrow
        self.curline = self.maxline - 1

    def recenter_line(self):
        smiddle = int(self.smaxrow / 2)
        pmiddle = self.pminrow + smiddle
        if self.curline > self.maxline - smiddle:
            self.bottom_win()
        elif self.curline < smiddle:
            self.top_win()
        elif self.curline > pmiddle:
            self.pminrow += self.curline - pmiddle
        elif self.curline < pmiddle:
            self.pminrow -= pmiddle - self.curline

    ###########################################################################
    #                               LINE JUMPING                              #
    ###########################################################################

    def goto_number(self, number):
        if (number >= self.maxline - self.smaxrow):
            self.bottom_win()
        elif (number < self.smaxrow):
            self.top_win()
        elif (number >= (self.pminrow + self.smaxrow)):
            self.pgdn_win()
        elif (number <= self.pminrow):
            self.pgup_win()
        self.curline = number

    def goto(self, prompt="Enter a line number: "):
        try:
            number = int(self.draw_textbox(prompt)) - 1
            if number < 0 or number > self.maxline:
                raise ValueError
            self.goto_number(number)
        except ValueError:
            return 'INVALID INDEX NUMBER!'

    def goto_next(self, items):
        if items:
            for i in items:
                if self.curline < i:
                    self.goto_number(i)
                    return
            self.top_line()
            self.goto_next(items)

    def goto_prev(self, items):
        if items:
            for i in reversed(items):
                if self.curline > i:
                    self.goto_number(i)
                    return
            self.bottom_line()
            self.goto_prev(items)

    ###########################################################################
    #                         PICK, TOGGLE AND SEARCH                         #
    ###########################################################################

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
                start, stop = numbers.split('..')[0], self.maxline
            elif match('^\\d+\\-$', numbers):
                start, stop = numbers.split('-')[0], self.maxline
            elif match('^\\.\\.\\d+$', numbers):
                start, stop = 1, numbers.split('..')[1]
            elif match('^\\-\\d+$', numbers):
                start, stop = 1, numbers.split('-')[1]
            elif match('^\\d+$', numbers):
                start, stop = (numbers,) * 2
            if start and stop:
                for index in range(int(start) - 1, int(stop)):
                    method(index, matches)

    ###########################################################################
    #                            SAVE, RESET & QUIT                           #
    ###########################################################################

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

    def reset(self):
        self.picked = []
        self.matches = []

    def quit(self):
        '''
        Signal to pick() that it's time to return the state of self.picked.
        '''
        return 'quit'
