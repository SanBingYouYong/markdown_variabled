# Markdown Variabled
Custom **markdown** parser/syntax for defining and using variables like **Python format strings**. 
![intro](intro.png)
Now supports expressions parsed line-by-line so you can literally do fancy things: 
![fancy](fancy.png)
# Quick Start
You'll only need `parser.py` file. 
 - (or the packed binary file `parser.exe`, `parser.app` or `parser`, only `parser.exe` is available in the release currently)
## Syntax
 - use the following grammar to define variables on individual new lines:
      - `@var=value` for direct Python variables
      - `~var=expression` for Python expression that will be evaluated upon parsing the line
         - you may use other defined variables and expressions in the expression
 - reference your variables in text with brackets {}, just like you'd use an f string in python (`f"the variable is {var}"`):
     - "...`the variable is {var}`..."
         - it can also be an expression (like can be defined above): "...`the variable squared is {var * var}`..."
 - append `/` to the start of a text line if you want to "escape" the line and use the actual brackets
 - check `example.md` and `example_parsed.md` for more details. 
## Usage
 - use `python parser.py <markdown file>` on your markdown with above grammar and you get a brand new parsed markdown file `<original_name>_parsed.md` in the same directory by default.
     - check out more options with `python parser.py -h`
     - for the binary, just go with `parser.exe <markdown file>` or replace parser.exe with your binary file's name
## Tips
 - default encoding is utf-8, so multi-lang is supported
     - so if you Python version is high enough, you can do `@开始年份=2018` and `在{开始年份}年时`
 - name your variables like you would name them in Python
     - thus `@what?='what?'` will not work just like `what? = 'what?'` won't work in Python - they are and will be interpreted as Python variables
 - use your variables like in format strings
     - things inside `{}` will be faithfully passed to f-string evaluation function in Python
 - both `@var=value` and `@var = value` work, if you like it neat
     - ~~thanks to Python's strip method~~
- you can even define **functions** using lambda: ~~this is too evil~~
     - e.g. `~format_year=lambda x : str(x) + "年"` and then `{format_year(year)}`
         - to use other variables, you can either pass them in as a parameter (e.g. `lambda x,y: ...`), or you can use a complicated syntax: `"{var}"`, for example: 
             - `~func=lambda x: str(x) + "{var}"`
             - because for lambda functions to work properly, they are first interpreted as a normal string so that the variables in `{}` get expanded, then they get evaluated as a lambda expression - therefore you need to wrap your variables with `""` to make sure the expanded definition is still grammarly correct. 
                 - sadly you can't use your lambda input x as {x} in format strings since they aren't (and can't be?) added to current states of variables. (i.e. `str(x) + "{var}"` instead of `f"{x} {var}"`)
### Traps!
- if you want to combine string and some logic code in an expression, make sure you properly surround the strings with quotes, single or double
    - otherwise it's an invalid Python expression
    - e.g. `phrase = 'abc' if some_condition else 'xyz'` is good, but not `phrase = abc if some_condition else xyz`
        - the latter will trigger an exception during evaluation and thus make the parser fallback to treat your expression as a string, use -v flag to see the record if ever confused
- now that Python expressions (*essentially Python codes*) can be run in a markdown file, be aware of fraud and injection attacks! 
     - **don't run the parser on random markdown files people send you** (lol)
         - ~~I mean why don't they run it themselves and send you the parsed version~~

# Packing into Executable Binary
Using `pyinstaller`: 
 - `pip install pyinstaller`
 - `pyinstaller --onefile parser.py`
 - and theoretically you will receive a binary executable on your platform (win, linux, or mac) in `./dist/parser(.exe or whatever)`
     - so you can do `parser.exe <markdown file>` directly
 - an executable binary on Windows (tested on win11) is available and included in the release

# Future Plans
 - maybe a website can be set-up too in the near future. no promises.
     - considering the use of `eval`s, might actually not lol. 
 - maybe also available as a PyPI/Conda package, but meh
 - ~~anti-fraud!~~
 - maybe pack a binary or a GUI
     - this is actually more reasonable?
 - be able to import a definitions file
     - pythonic way of re-using templates lol
 - support nested expressions? 
     - NOW SUPPORTED! 
 - built-in variables? 
     - I feel like this is begining to act like LaTex
     - with the potential import functionality, you may do it yourself
 - add variables to `globals()` so we can reference other variables in lambda functions
     - instead, you may do it now, see Tips section
     - and globals() did not work that smoothly
