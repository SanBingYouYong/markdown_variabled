@year=2000
@year_offset=20
@book=Two Years of My Life
# Introduction
### Just like you use an f-string
~updated_year=year + year_offset
In the year of {year + year_offset} or {updated_year + 1}: 
 - we read about the book {book}. 

~book_name='"' + str(year) + ": " + book + '"'
In Python, a variable like year={year} will be treated as a {type(year)}. 
 - Once integers are converted to strings, we can rename the book as {book_name}

### Dynamic Evaluation of @variables
@pic="intro.png"
@show_pic=True
~pic_command=f"![pic]({pic})" if show_pic else "No Pic For You!"

Do we have a picture? Yes! 
 - {pic_command}

@show_pic=False
Do we have a picture now? No... 
 - {pic_command}

### Function
~format_book_name=lambda name: '《' + str(name) + "》"
book name formated: {format_book_name(book)}

~multiple_arg_func=lambda name, year: '《' + str(name) + "》" + " in year " + str(year)
multiple args: {multiple_arg_func(book, year)}

~x=book
~this_is_a_func=f"{x} {y} {book}"
@y=book
func with vars: {this_is_a_func}

~func_with_ref=lambda z: str(z) + "{book}"
func with ref: {func_with_ref(111)}

### Nested Expression Support
@nested=nested
~nested1=nested + "1"
~nested2=nested1 + "2"
Nested expressions are now supported: 
 - nested: {nested}, nested1: {nested1}, nested2: {nested2}
@nested=really dynamic
And they are also dynamic: 
 - nested: {nested}, nested1: {nested1}, nested2: {nested2}
~nested1=nested + "?"
~nested2=nested1 + "!!"
 - nested: {nested}, nested1: {nested1}, nested2: {nested2}



/### Still Want {}?
 - Escape the line
     - Usual escape char `\` won't work here, instead, append an `/` to the start of the text line where you want to disable variable referencing. 
/         - e.g. `/I want my brackets {back}!`
/         - and not this: `I want my brackets \{back\}!` since f strings do not allow backslashes
@bracket_0 = {
@bracket_1 = }
 - Alternatively, define a variable: {bracket_0} and {bracket_1}
/   - e.g. `@bracket_0 = {`
     - so the header/list format in your working document won't be messed up
