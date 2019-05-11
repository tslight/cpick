# CURSES LIST PICKER

![img](./cpick.gif "Curses List Picker")

*Pick items from a list with a nice TUI.*

## INSTALLATION

`pip install cpick`

## CLI USAGE

``` text
usage: cpick [-h] [--limit LIMIT] [--header HEADER] [--footer FOOTER]
			 items [items ...]

Curses list picker.

positional arguments:
  items                 Items for the picker.

optional arguments:
  -h, --help            show this help message and exit
  --limit LIMIT, -l LIMIT
						Limit number of picks.
  --header HEADER, -H HEADER
						A string to use as a header.
  --footer FOOTER, -F FOOTER
						A string to use as a footer.
```

## PYTHON USAGE

``` python
import curses
from cpick import pick

# list to feed into the picker
item   = ['a', 'list', 'of', 'items']
# only allow five items to be picked, defaults to sys.maxsize
limit  = 5
# defaults to 'Pick some items from this list'
header = 'Pick some items from this list:'
# defaults to 'Press [?] to view keybindings'
footer = 'Press [?] to view keybindings'
# get picks!
picked = pick(items, limit, header, footer)
# print picked list
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

Pick a number from 1 to 100, using custom header/footer and limiting picks to 5.

`cpick --header "My header" --footer "My footer" --limit 5 {1..100}`

Pick 5 random words from the dictionary, using the default header/footer.

`cpick --limit 5 $(shuf -n 100 /usr/share/dict/words)`

Pick an unlimited number of paths from the current directory.

`cpick $(ls)`
