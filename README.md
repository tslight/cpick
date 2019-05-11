# CURSES LIST PICKER

![img](./cpick.gif "Curses List Picker")

*Pick items from a list with a nice TUI, & comfy Vi keybindings.*

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
import cpick

# list to feed into the picker
item   = ['a', 'list', 'of', 'items']

# only allow five items to be picked, defaults to sys.maxsize
limit  = 5
# defaults to 'Pick some items from this list'
header = 'Pick some items from this list:'
# defaults to 'Press [?] to view keybindings'
footer = 'Press [?] to view keybindings'
# get picks!
picked = cpick.get_picks(items, limit, header, footer)

# print picked list
print(picked)
```

## INTERFACE

``` text
[k][UP]       : Move up one line.
[j][DOWN]     : Move down one line.
[g][HOME]     : Jump to first line.
[G][END]      : Jump to last line.
[f][PGDN]     : Jump down a page of lines.
[b][PGUP]     : Jump up a page of lines.
[#]           : Jump to line number.
[/]           : Find items via globbing, regex or range.
[n]           : Jump to next search result.
[p]           : Jump to previous search result.
[CTRL-n]      : Jump to next pick.
[CTRL-p]      : Jump to previous pick.
[r][F5]       : Reset search results and picks.
[z][CTRL-l]   : Recenter current line on screen.
[RET]         : Pick an item.[u]           : Undo the last pick.
[U]           : Undo the last pick and move to it's line.
[t]           : Toggle item pick status.
[SPC]         : Toggle item and go down a line.
[CTRL-SPC]    : Toggle item and go up a line.
[a]           : Toggle picking of all items.
[;][F3]       : Toggle via globbing, regex or range.
[?][F1]       : View this help page.
[q][ESC]      : Quit and display all marked paths.
```

## NOTES

Picking`[;]` and searching`[/]` is supported via the following methods:

- Globbing & Wildcards.
- Regular Expressions.
- Specifying an index (line number) of an item.
- Specifying a range of indexes (line numbers) in the following forms:
  - *x..y* : Match numbers between *x* and *y*.
  - *x-y*  : Match numbers between *x* and *y*.
  - *x..*  : Match number from item at index *x* until the end of the list.
  - *..y*  : Match from beginning of list until item at index *y*.
  - *x-*   : Match number from item at index *x* until the end of the list.
  - *-y*   : Match from beginning of list until item at index *y*.
- Searching for literal strings.

These can also be combined. You can enter multiple patterns, ranges and strings
at one `Find:` or `Pick:` prompt.

However, be aware, that if patterns, ranges or strings are entered together that
match the same items they will cancel each other out. This is due to the
toggling nature of the resulting action.

I am open to changing this behaviour if requested...

## EXAMPLES

Pick a number from 1 to 100, using custom header/footer and limiting picks to 5.

`cpick --header "My header" --footer "My footer" --limit 5 {1..100}`

Pick 5 random words from the dictionary, using the default header/footer.

`cpick --limit 5 $(shuf -n 100 /usr/share/dict/words)`

Pick an unlimited number of paths from the current directory.

`cpick $(ls)`
