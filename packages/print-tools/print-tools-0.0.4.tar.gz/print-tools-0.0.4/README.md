# Print Tools
[![Build Status](https://travis-ci.org/edmundpf/print_tools.svg?branch=master)](https://travis-ci.org/edmundpf/print_tools)
[![PyPI version](https://badge.fury.io/py/print-tools.svg)](https://badge.fury.io/py/print-tools)
> Includes useful methods for stylized/formatted printing.
## Install
* `python3 -m pip install print-tools`
## Usage
``` python
from print_tools.printer import Printer
p = Printer()
p.log('Printer initialized!')
```
## Methods
* `__init__`
	* style
		* Default monokai, can use solarized as well
	* Monokai Colors
		* 'orange', 'magenta', 'purple', 'blue', 'seagreen', 'green', 'yellow'
	* Solorized Colors
		* 'yellow', 'orange', 'red', 'magenta', 'violet', 'blue', 'cyan', 'green'
* `log`
	* Logs text with bold date/time string in front of text
	* Args
		* text
* `error`
	* Prints red *ERROR:* in front of text, log string optional
	* Args
		* text
		* log (True)
* `success`
	* Prints green *SUCCESS:* in front of text, log string optional
	* Args
		* text
		* log (True)
* `arrow`
	* Prints "-->" in front of text, indentation optional
	* Args
		* text
		* indent (0)
* `chevron`
	* Prints ">>>" in front of text, indentation optional
	* Args
		* text
		* indent (0)
* `bullet`
	* Prints "•" in front of text, indentation optional
	* Args
		* text
		* indent (0)
* `format`
	* Custom template formatting of strings
	* Template formatting entered as so in string: i.e. `[bold:green]`
		* format_op arg can be changed to different outside operator, must be two char string, i.e. "||" would yield `|bold:green|`
	* Modifiers must be entered first
		* bold, italic, underlined, reset
	* Foreground color must be entered next i.e. `[green]`
	* Background color must be entered with *on_* prefix i.e. `[on_blue]`
	* Formatting can be removed with *reset* modifier, this can be mixed with new formatting i.e. `[reset:bold:green]`
	* To remove specific formatting, enter no_ before argument, (one argument per block) i.e. `[no_bold][no_italic]`
		* To remove foreground color
			* `[no_foreground]
		* To remove background color
			* `[no_background]
	* By default the string formatting is cleared after the print statement, this can be changed by setting arg *reset* to False
	* Additionally, the log string can be printed first by setting arg *log* to True
