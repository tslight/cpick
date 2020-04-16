import curses
from .action import Action


class Keys(Action):
    def __init__(self, stdscr, items):
        super().__init__(stdscr, items)
        self.help = [
            "[h][LEFT]     : Move left one column.",
            "[l][RIGHT]    : Move right one column.",
            "[k][UP]       : Move up one row.",
            "[j][DOWN]     : Move down one row.",
            "[f][PGDN]     : Jump down a page of rows.",
            "[b][PGUP]     : Jump up a page of rows.",
            "[g][HOME]     : Jump to first item.",
            "[G][END]      : Jump to last item.",
            "[#]           : Jump to an item number.",
            "[/]           : Find items via wildcards, regex or range.",
            "[n]           : Jump to next search result.",
            "[p]           : Jump to previous search result.",
            "[CTRL-n]      : Jump to next pick.",
            "[CTRL-p]      : Jump to previous pick.",
            "[r][F5]       : Reset search results and picks.",
            "[z][CTRL-l]   : Recenter current row on screen.",
            "[RET]         : Pick an item.",
            "[;]           : Pick via wildcards, regex or range.",
            "[u]           : Undo the last pick.",
            "[U][BACKSPACE]: Undo the last pick and move to it's row.",
            "[t]           : Toggle an item.",
            "[SPC]         : Toggle item and go down a row.",
            "[CTRL-SPC]    : Toggle item and go up a row.",
            "[a]           : Toggle all items.",
            "[:]           : Toggle via wildcards, regex or range.",
            "[v]           : View all picks.",
            "[?][F1]       : View this help page.",
            "[w][CTRL-s]   : Save picks to file.",
            "[q][ESC]      : Quit and display all marked paths.",
        ]

        self.keys = {
            "resize": [curses.KEY_RESIZE],
            "left": [ord("h"), curses.KEY_LEFT],
            "right": [ord("l"), curses.KEY_RIGHT],
            "down": [ord("j"), curses.KEY_DOWN],
            "up": [ord("k"), curses.KEY_UP],
            "pgdn": [ord("f"), curses.KEY_NPAGE],
            "pgup": [ord("b"), curses.KEY_PPAGE],
            "top": [ord("g"), curses.KEY_HOME],
            "bottom": [ord("G"), curses.KEY_END],
            "goto": [ord("#"), curses.ascii.ctrl(ord("g"))],
            "find": [ord("/")],
            "next_find": [ord("n"), curses.ascii.ctrl(ord("s"))],
            "prev_find": [ord("p"), curses.ascii.ctrl(ord("r"))],
            "next_pick": [curses.ascii.ctrl(ord("n"))],
            "prev_pick": [curses.ascii.ctrl(ord("p"))],
            "reset": [ord("r"), curses.KEY_F5],
            "recenter": [ord("z"), curses.ascii.ctrl(ord("l"))],
            "pick": [ord("\n")],
            "pick_pattern": [ord(";")],
            "undo": [ord("u")],
            "undo_up": [ord("U"), curses.KEY_BACKSPACE],
            "toggle": [ord("t")],
            "toggle_down": [ord(" ")],
            "toggle_up": [curses.ascii.ctrl(ord(" "))],
            "toggle_all": [ord("a")],
            "toggle_pattern": [ord(":")],
            "view_picks": [ord("v")],
            "view_help": [ord("?"), curses.KEY_F1],
            "save": [ord("w"), curses.ascii.ctrl(ord("s"))],
            "quit": [ord("q"), curses.ascii.ESC],
        }

        self.pad_actions = {
            "resize": self.resize,
            "down": self.down_pad,
            "up": self.up_pad,
            "pgdn": self.pgdn_pad,
            "pgup": self.pgup_pad,
            "top": self.top_pad,
            "bottom": self.bottom_pad,
            "quit": self.quit,
        }

        self.row_actions = {  # https://stackoverflow.com/a/45928598
            "resize": self.resize,
            "right": self.right_col,
            "left": self.left_col,
            "down": self.down_row,
            "up": self.up_row,
            "top": self.first_item,
            "bottom": self.last_item,
            "pgdn": self.pgdn_row,
            "pgup": self.pgup_row,
            "goto": self.goto,
            "find": lambda: self.match("Find: ", self.matches, self.pick),
            "next_find": lambda: self.goto_next(self.matches),
            "prev_find": lambda: self.goto_prev(self.matches),
            "next_pick": lambda: self.goto_next(self.picked),
            "prev_pick": lambda: self.goto_prev(self.picked),
            "reset": self.reset,
            "recenter": self.recenter_row,
            "pick": lambda: self.pick(self.currow, self.picked) or self.down_row(),
            "pick_pattern": lambda: self.match("Pick: ", self.picked, self.pick),
            "undo": self.undo,
            "undo_up": self.undo_up,
            "toggle": lambda: self.toggle(self.currow, self.picked),
            "toggle_down": lambda: self.toggle_down(self.currow, self.picked),
            "toggle_up": lambda: self.toggle(self.currow, self.picked) or self.up_row(),
            "toggle_all": self.toggle_all,
            "toggle_pattern": lambda: self.match("Toggle: ", self.picked, self.toggle),
            "view_picks": lambda: self.view([self.items[p] for p in self.picked]),
            "view_help": lambda: self.view(self.help),
            "save": self.save,
            "quit": self.quit,
        }

    def get_action(self, key):
        return [k for (k, v) in self.keys.items() if key in v][0]

    def row_action(self, key):
        return self.row_actions[self.get_action(key)]()

    def pad_action(self, key):
        return self.pad_actions[self.get_action(key)]()
