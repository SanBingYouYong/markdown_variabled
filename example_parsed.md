# Introduction
### Just like you use an f-string
In the year of 2020 or 2021: 
 - we read about the book Two Years of My Life. 

In Python, a variable like year=2000 will be treated as a <class 'int'>. 
 - Once integers are converted to strings, we can rename the book as "2000: Two Years of My Life"

### Dynamic Evaluation of @variables

Do we have a picture? Yes! 
 - ![pic](intro.png)

Do we have a picture now? No... 
 - No Pic For You!

### Function
book name formated: 《Two Years of My Life》

multiple args: 《Two Years of My Life》 in year 2000

func with vars: Two Years of My Life book Two Years of My Life

func with ref: 111Two Years of My Life

### Nested Expression Support
Nested expressions are now supported: 
 - nested: nested, nested1: nested1, nested2: nested12
And they are also dynamic: 
 - nested: really dynamic, nested1: really dynamic1, nested2: really dynamic12
 - nested: really dynamic, nested1: really dynamic?, nested2: really dynamic?!!



### Still Want {}?
 - Escape the line
     - Usual escape char `\` won't work here, instead, append an `/` to the start of the text line where you want to disable variable referencing. 
         - e.g. `/I want my brackets {back}!`
         - and not this: `I want my brackets \{back\}!` since f strings do not allow backslashes
 - Alternatively, define a variable: { and }
   - e.g. `@bracket_0 = {`
     - so the header/list format in your working document won't be messed up
