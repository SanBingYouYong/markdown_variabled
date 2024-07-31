# Markdown Variabled
Custom **markdown** parser/syntax for inserting variables like **Python format strings**. 
![intro](intro.png)
Now supports expressions parsed line-by-line so you can literally do fancy things: 
![fancy](fancy.png)
# Quick Start
You'll only need `parser.py` file. 
 - maybe a website can be set-up too in the near future. no promises.
## Syntax
 - use the following grammar to define variables on individual new lines:
      - `@var=value` for direct Python variables
      - `~var=expression` for Python expression that will be evaluated upon parsing the line
 - reference your variables in text with brackets {}, just like you'd use an f string in python (`f"the variable is {var}"`):
     - `the variable is {var}`
         - it can also be an expression (like can be defined above): `the variable is {var * var}
 - check `example.md` and `example_parsed.md` for more details. 
## Usage
 - use `python parser.py <markdown file>` on your markdown with above grammar and you get a brand new parsed markdown file `<original_name>_parsed.md` in the same directory by default.
     - check out more options with `python parser.py -h`
