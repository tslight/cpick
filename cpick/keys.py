import curses
from .action import Action


class Keys(Action):
    """
    Translate keys to actions.
    """

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

        # The keys in this dictionary map onto methods in the Action class.
        self.rowkeys = {
            "resize": [curses.KEY_RESIZE],
            "left_col": [ord("h"), curses.KEY_LEFT],
            "right_col": [ord("l"), curses.KEY_RIGHT],
            "down_row": [ord("j"), curses.KEY_DOWN],
            "up_row": [ord("k"), curses.KEY_UP],
            "pgdn_row": [ord("f"), curses.KEY_NPAGE],
            "pgup_row": [ord("b"), curses.KEY_PPAGE],
            "first_item": [ord("g"), curses.KEY_HOME],
            "last_item": [ord("G"), curses.KEY_END],
            "goto": [ord("#"), curses.ascii.ctrl(ord("g"))],
            "find": [ord("/")],
            "next_find": [ord("n"), curses.ascii.ctrl(ord("s"))],
            "prev_find": [ord("p"), curses.ascii.ctrl(ord("r"))],
            "next_pick": [curses.ascii.ctrl(ord("n"))],
            "prev_pick": [curses.ascii.ctrl(ord("p"))],
            "reset": [ord("r"), curses.KEY_F5],
            "recenter_row": [ord("z"), curses.ascii.ctrl(ord("l"))],
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

        # The keys in this dictionary map onto methods in the Action class.
        self.padkeys = {
            "resize": [curses.KEY_RESIZE],
            "down_pad": [ord("j"), curses.KEY_DOWN],
            "up_pad": [ord("k"), curses.KEY_UP],
            "pgdn_pad": [ord("f"), curses.KEY_NPAGE],
            "pgup_pad": [ord("b"), curses.KEY_PPAGE],
            "top_pad": [ord("g"), curses.KEY_HOME],
            "bottom_pad": [ord("G"), curses.KEY_END],
            "quit": [ord("q"), curses.ascii.ESC],
        }

    def row_action(self, key):
        """
        Run a key from the rowkeys dictionary as a method.
        """
        try:
            action = [k for (k, v) in self.rowkeys.items() if key in v][0]
            return getattr(self, action)()
        except IndexError:
            pass

    def pad_action(self, key):
        """
        Run a key from the padkeys dictionary as a method.
        """
        try:
            action = [k for (k, v) in self.padkeys.items() if key in v][0]
            return getattr(self, action)()
        except IndexError:
            pass
