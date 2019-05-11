# CURSES LIST PICKER

![img](./cpick.gif "Curses List Picker")

*Pick items from a list with a nice TUI.*

## INSTALLATION

`pip install cpick`

## CLI USAGE

``` text
usage: cpick [-h] [--header HEADER] [--footer FOOTER] items [items ...]

Curses list picker.

positional arguments:
  items                 Items for the picker.

optional arguments:
  -h, --help            show this help message and exit
  --header HEADER, -H HEADER
						A string to use as a header.
  --footer FOOTER, -F FOOTER
						A string to use as a footer.
```

## PYTHON USAGE

``` python
import curses
from cpick import pick

item = ['a', 'list', 'of', 'items']

picked = pick(items)

print(picked)
```

## INTERFACE

| **KEYS**          | **ACTION**                                   |
|:------------------|:---------------------------------------------|
| `k`, `UP`         | Move up one line.                            |
| `j`, `DOWN`       | Move down one line.                          |
| `f`, `PGDN`       | Jump down a page of lines.                   |
| `b`, `PGUP`       | Jump up a page of lines.                     |
| `g`, `HOME`       | Jump to first line.                          |
| `G`, `END`        | Jump to last line.                           |
| `#`               | Jump to an item index number                 |
| `/`               | Find items via globbing, regex or substring. |
| `n`               | Jump to next search result.                  |
| `N`               | Jump to previous search result.              |
| `p`               | Jump to next pick.                           |
| `P`               | Jump to previous pick.                       |
| `z`, `Z`          | Recenter current line on screen.             |
| `s`, `SPC`        | Pick an item and go down a line.             |
| `u`, `U`          | Unpick an item and go up a line.             |
| `t`, `T`          | Toggle item pick status.                     |
| `a`, `A`          | Toggle picking of all items.                 |
| `;`, `*`          | Toggle via globbing,  regex or substring.    |
| `:`, `!`          | Toggle via index number or range of indices. |
| `?`, `F1`         | View this help page.                         |
| `R`, `F5`         | Reset search results and picks.              |
| `q`, `ESC`, `RET` | Quit and display all marked paths.           |

## NOTES

Picking and searching can be done with globbing or regular expression pattern
matching or simply by searching for strings or substrings.

These can also be combined. You can enter multiple patterns at one `Find:` or
`Pick:` prompt.

However, be aware, that if two patterns are entered together that match the same
items they will cancel each other out, due to the toggling nature of the
resulting action.

This behavior is also true when selecting by `Range:`.

## EXAMPLES

Pick a number from 1 to 100.

`cpick {1..100}`

Pick a random word from the dictionary.

`cpick $(shuf -n 100 /usr/share/dict/words)`

Pick a path in the current directory.

`cpick $(ls)`
