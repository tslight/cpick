from fnmatch import fnmatch
from .draw import Draw


class Action(Draw):
    def __init__(self, screen):
        Draw.__init__(self, screen)
        self.index = 0
        self.picked = []
        self.matches = []

    def up(self):
        self.index -= 1

    def dn(self):
        self.index += 1

    def pgdn(self):
        self.index += self.y

    def pgup(self):
        self.index -= self.y

    def top(self):
        self.index = 0

    def btm(self):
        self.index = len(self.options) - 1

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
