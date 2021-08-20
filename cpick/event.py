"""
Curses List Picker
"""
from os import environ
from sys import maxsize
from .keys import Keys


class Event(Keys):
    """
    Entry point event loops.
    """

    def __init__(
        self,
        stdscr,
        items,
        limit=maxsize,
        numbers=False,
        header="PICK ITEMS FROM THIS LIST:",
        footer="Press [?] to view keybindings",
    ):
        super().__init__(stdscr, items)
        self.limit, self.numbers = limit, numbers
        self.header, self.footer = header, footer

    def __view(self, contents):
        if not contents:
            contents = ["", "Nothing to see here..."]

        # save state before reinitialising the body... this is very ugly...
        items, pminrow = self.items, self.pminrow
        currow, curcol = self.currow, self.curcol
        self.items, self.pminrow = contents, 0

        self.body_init()
        self.refresh()

        while True:
            self.draw_body(contents, numbers=False, pick=False)
            self.draw_header("Press [UP] [DOWN] [PGUP] [PGDN] to scroll.")
            self.draw_footer("Press [q] or [ESC] to return to picker.")
            self.refresh()
            key = self.stdscr.getch()
            if self.pad_action(key) == "quit":
                break

        # restore the content state
        self.items = items
        self.body_init()
        # restore our previous position in the page... yes this is naff!
        self.pminrow, self.currow, self.curcol = pminrow, currow, curcol
        self.refresh()

    def view_picks(self):
        self.__view([self.items[p] for p in self.picked])

    def view_help(self):
        self.__view(self.help)

    def get_picks(self):
        """
        Main event loop that draws the screen, waits for input, and executes an
        action based on that input. If the method executed returns true, we
        return our objects' picked attribute.
        """
        header, footer, out = self.header, self.footer, None
        while True:
            self.draw_body(self.items, numbers=self.numbers)
            self.draw_header(header)
            self.draw_footer(footer)
            self.refresh()
            key = self.stdscr.getch()
            if self.row_action(key) == "quit":
                return [self.items[pick] for pick in self.picked]
            if len(self.picked) > self.limit:
                if self.limit == 1:
                    del self.picked[: self.limit]
                else:
                    del self.picked[self.limit :]
                header, footer = ("MAXIMUM PICK LIMIT REACHED!",) * 2
            elif out:
                footer = out
            else:
                header, footer = self.header, self.footer
