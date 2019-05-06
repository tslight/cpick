class Action:
    def __init__(self):
        self.index = 0
        self.picked = []

    def up(self):
        self.index -= 1

    def dn(self):
        self.index += 1

    def pgdn(self):
        self.index += self.y - 3

    def pgup(self):
        self.index -= self.y - 3

    def top(self):
        self.index = 0

    def btm(self):
        self.index = len(self.options) - 1

    def wrap(self):
        if self.index < 0:
            self.btm()
        if self.index >= len(self.options):
            self.top()

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

    def quit(self):
        '''
        Signal to get_picked that it's time to return the state of self.picked.
        '''
        return True

    def ignore(self):
        '''
        Skip unbound key presses in main event method.
        '''
        return False
