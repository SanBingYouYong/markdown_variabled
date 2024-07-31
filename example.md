@year=2000
@year_offset=20
@book=Two Years of My Life
# Introduction
~updated_year=year + year_offset
In the year of {year + year_offset} or {updated_year + 1}: 
 - we read about the book {book}. 

~book_name='"' + str(year) + ": " + book + '"'
In Python, a variable like year={year} will be treated as a {type(year)}. 
 - Once integers are converted to strings, we can rename the book as {book_name}

~pic="intro.png" if show_pic else None
~pic_command="![pic]({pic})" if show_pic else "No Pic For You!"
@show_pic=True
Do we have a picture? Yes! 
 - {pic_command}
@show_pic=False
Do we have a picture now? No... 
 - {pic_command}
