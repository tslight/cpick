"""
Curses List Picker
"""
from fnmatch import fnmatch
from os.path import abspath, expanduser
from re import match, error
from .draw import Draw


class Action(Draw):
    """
    What to draw on the screen.
    """

    def __init__(self, stdscr, items):
        super().__init__(stdscr, items)
        self.picked = []
        self.matches = []

    ###########################################################################
    #                             PAD MOVEMENT                                #
    ###########################################################################

    def up_pad(self):
        if self.pminrow > 0:
            self.pminrow -= 1

    def down_pad(self):
        if self.pminrow < self.pmaxrow - self.smaxrow:
            self.pminrow += 1

    def pgdn_pad(self):
        self.pminrow += self.smaxrow
        if self.pminrow >= self.pmaxrow - self.smaxrow:
            self.pminrow = self.pmaxrow - self.smaxrow

    def pgup_pad(self):
        self.pminrow -= self.maxy - 1
        if self.pminrow < 0:
            self.pminrow = 0

    def top_pad(self):
        self.pminrow = 0

    def bottom_pad(self):
        self.pminrow = self.pmaxrow - self.smaxrow

    ###########################################################################
    #                   CHECK ROW IN CONTEXT OF SCREEN & PAD                  #
    ###########################################################################

    def __is_pad_top(self):
        """
        If the current row is less than the pads maximum number of rows, times
        the current column, minus the maximum number of rows, we are beyond
        the top of the current column.
        """
        return self.currow <= (self.pmaxrow * self.curcol) - self.pmaxrow

    def __is_pad_bottom(self):
        """
        If the current row is greater than the pad's maximum number of rows
        times the current column, then we have gone beyond the bottom of the
        current column's pad. Minus 2 to account for header and footer.
        """
        return self.currow > (self.pmaxrow * self.curcol) - 2

    def __is_scr_top(self):
        """
        If the current row is less than the pads minimum row shown on the
        screen (a.k.a) the top of the row.
        """
        return (
            self.currow <= self.pminrow
            or self.currow <= (self.pmaxrow * (self.curcol - 1)) + self.pminrow
        )

    def __is_scr_bottom(self):
        return (
            self.currow
            >= (self.pmaxrow * (self.curcol - 1)) + self.pminrow + self.smaxrow - 1
        )

    ###########################################################################
    #                              ROW MOVEMENT                               #
    ###########################################################################

    def left_col(self):
        if self.curcol > 1:
            self.curcol -= 1
            self.currow -= self.pmaxrow

    def right_col(self):
        if self.curcol < self.columns:
            self.curcol += 1
            self.currow += self.pmaxrow

    def down_row(self):
        if self.currow >= self.total - 1:
            self.first_item()
            return

        if self.__is_pad_bottom():
            self.top_pad()
            self.curcol += 1

        if self.__is_scr_bottom():
            self.pminrow += 1

        self.currow += 1  # scroll cursor

    def up_row(self):
        if self.currow < 1:
            self.last_item()
            return

        if self.__is_pad_top():
            self.bottom_pad()
            self.curcol -= 1

        if self.__is_scr_top():
            self.pminrow -= 1

        self.currow -= 1

    def pgdn_row(self):
        if self.pminrow >= self.pmaxrow - self.smaxrow:
            self.top_pad()
            self.curcol += 1
        else:
            self.pminrow += self.smaxrow

        self.currow += self.smaxrow

        if self.currow >= self.total - 1:
            self.first_item()

    def pgup_row(self):
        if self.pminrow <= 0:
            self.bottom_pad()
            self.curcol -= 1
        else:
            self.pminrow -= self.smaxrow

        self.currow -= self.smaxrow

        if self.currow < 0:
            self.last_item()

    def first_item(self):
        self.pminrow, self.currow = (0,) * 2
        self.curcol = 1

    def last_item(self):
        self.pminrow = self.pmaxrow - self.smaxrow
        self.currow = self.total - 1
        self.curcol = self.columns

    def recenter_row(self):
        smiddle = int(self.smaxrow / 2)
        pmiddle = self.pminrow + smiddle
        if self.currow > self.pmaxrow - smiddle:
            self.bottom_pad()
        elif self.currow < smiddle:
            self.top_pad()
        elif self.currow > pmiddle:
            self.pminrow += self.currow - pmiddle
        elif self.currow < pmiddle:
            self.pminrow -= pmiddle - self.currow

    ###########################################################################
    #                               ROW JUMPING                              #
    ###########################################################################

    def __goto_next(self, items):
        if items:
            for i in items:
                if self.currow < i:
                    self.__goto_number(i)
                    return
            self.first_item()
            self.__goto_next(items)

    def __goto_prev(self, items):
        if items:
            for i in reversed(items):
                if self.currow > i:
                    self.__goto_number(i)
                    return
            self.last_item()
            self.__goto_prev(items)

    def __goto_number(self, number):
        self.currow = number

        for _ in range(self.columns):
            if self.__is_pad_top():
                self.curcol -= 1
            elif self.__is_pad_bottom():
                self.curcol += 1

        if self.__is_pad_top() and self.__is_scr_top():
            self.bottom_pad()
        elif self.__is_pad_bottom() and self.__is_scr_bottom:
            self.top_pad()

        for _ in range(self.screens):
            if self.__is_scr_top():
                self.pgup_pad()
            elif self.__is_scr_bottom():
                self.pgdn_pad()

    def goto(self, prompt="Enter an item number: "):
        try:
            number = int(self.draw_textbox(prompt)) - 1
            if number < 0 or number > self.total:
                raise ValueError
            self.__goto_number(number)
        except ValueError:
            return "INVALID ITEM NUMBER!"

    ###########################################################################
    #                         PICK, TOGGLE AND SEARCH                         #
    ###########################################################################

    def __pick(self, index, matches):
        if index not in matches:
            matches.append(index)

    def __toggle(self, index, matches):
        if index in matches:
            matches.remove(index)
        else:
            matches.append(index)

    def __match(self, msg, matches, method):
        search = self.draw_textbox(msg).strip().split()
        for index, item in enumerate(self.items):
            for pattern in search:
                try:
                    if match(pattern, item):
                        method(index, matches)
                except error:
                    if fnmatch(item, pattern) or pattern == item:
                        method(index, matches)
        self.__range(search, matches, method)
        if matches:
            self.__goto_next(matches)

    def __range(self, ranges, matches, method):
        start, stop = (0,) * 2
        for numbers in ranges:
            if match("^\\d+\\.\\.\\d+$", numbers):
                start, stop = numbers.split("..")
            elif match("^\\d+\\-\\d+$", numbers):
                start, stop = numbers.split("-")
            elif match("^\\d+\\.\\.$", numbers):
                start, stop = numbers.split("..")[0], self.total
            elif match("^\\d+\\-$", numbers):
                start, stop = numbers.split("-")[0], self.total
            elif match("^\\.\\.\\d+$", numbers):
                start, stop = 1, numbers.split("..")[1]
            elif match("^\\-\\d+$", numbers):
                start, stop = 1, numbers.split("-")[1]
            elif match("^\\d+$", numbers):
                start, stop = (numbers,) * 2
            if start and stop:
                for index in range(int(start) - 1, int(stop)):
                    method(index, matches)

    def find(self):
        self.__match("Find: ", self.matches, self.__pick)

    def next_find(self):
        self.__goto_next(self.matches)

    def prev_find(self):
        self.__goto_prev(self.matches)

    def pick(self):
        self.__pick(self.currow, self.picked)
        self.down_row()

    def next_pick(self):
        self.__goto_next(self.picked)

    def prev_pick(self):
        self.__goto_prev(self.picked)

    def pick_pattern(self):
        self.__match("Pick: ", self.picked, self.__pick)

    def toggle(self):
        self.__toggle(self.currow, self.picked)

    def toggle_all(self):
        if len(self.picked) == len(self.items):
            self.picked = []
        else:
            self.picked = [i for i, o in enumerate(self.items)]

    def toggle_down(self):
        self.toggle()
        self.down_row()

    def toggle_up(self):
        self.toggle()
        self.up_row()

    def toggle_pattern(self):
        self.__match("Toggle: ", self.picked, self.__toggle)

    def undo(self):
        if self.picked:
            del self.picked[-1]

    def undo_up(self):
        if self.picked:
            self.__goto_prev(self.picked)
            self.undo()

    ###########################################################################
    #                            SAVE, RESET & QUIT                           #
    ###########################################################################

    def save(self):
        path = self.draw_textbox("Save to: ").strip()
        path = abspath(expanduser(path))
        out = None
        try:
            # removes need to use f.close
            with open(path, "a+") as f:
                for pick in self.picked:
                    f.write(self.items[pick] + "\n")
        except FileNotFoundError:
            out = "Can't find " + path
        except IsADirectoryError:
            out = path + " is a directory."
        except UnboundLocalError:  # bit of a hack but fuck it
            out = "Not saving items."
        except Exception:
            out = "Something went wrong..."
        else:
            out = "Saved items to " + path
        finally:
            return out

    def reset(self):
        self.picked = []
        self.matches = []

    def quit(self):
        """
        Signal to pick() that it's time to return the state of self.picked.
        """
        return "quit"
