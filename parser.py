'''
Expected Markdown Format: 

 - Variables are defined individually on a new line: 
     - @<var>=<value>
     - ~<var>=<expression>
 - Other contents untouched

Upon running the script, the variables will be parsed and formatted into the markdown content.
'''


import argparse
import os
from typing import Any


### HELPERS ###
class MarkdownParser():
    def __init__(self, verbose: bool=False, encoding: str='utf-8') -> None:
        self.current_state = {}

        self.raw_expressions = {}
        self.markdown_lines = []
        self.parsed_lines = []

        self.verbose: bool = verbose
        self.encoding: str = encoding
    
    @staticmethod
    def is_definition_line(line: str) -> bool:
        '''
        Identify a definition line with @/~ prefix and = in it
        '''
        has_prefix = line.startswith("@") or line.startswith("~")
        has_equals = "=" in line
        not_del_line = not line.startswith("~~")  # not a deletion line
        return has_prefix and has_equals and not_del_line
    
    @staticmethod
    def parse_value(value: str) -> Any:
        '''
        Parse a variable into correct type: int/float/bool/str, default (last) str
        '''
        value = value.strip()
        # following: GPT type matching
        # int/float
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            pass
        # boolean
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        # string (with or without quotes)
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        if value.startswith("'") and value.endswith("'"):
            return value[1:-1]
        return value  # default to string

    def parse_definition_line(self, line: str) -> None:
        '''
        Parse a definition line: 
             - if it's a variable definition (@), 
             parse and update current_state
             - if it's an expression definition (~), 
             store it as raw expression for evaluation it later (when a textline is encountered, all expressions are evaluated)
        
        When same name is used, old definition will be overwritten:
            meaning that the previous definition will be lost. 
                 - e.g. naming a var(@) with an expr(~)'s name will delete the expr from raw_expressions
                 - e.g. naming an expr(~) with a repeated name(@/~) will update the expr in raw_expressions
                    and remove the previous value from current_state, be it defined by @ or evaluated from raw_expressions.
        
        When an expression self-referencing, e.g. ~x = x, it will be treated as string "x" and NOT added to raw_expressions. 
        '''
        if line.startswith("@"):
            key, value = line[1:].split("=")
            key = key.strip()
            value = MarkdownParser.parse_value(value.strip())
            if key in self.raw_expressions:  # overwrite the expr with var
                if self.verbose:
                    print(f"Warning: {key} already defined, previous definition in raw_expressions as {self.raw_expressions[key]} will be overwritten by: {value}.")
                del self.raw_expressions[key]  # removed from raw_expressions
            self.current_state[key] = value  # maybe can remove variables now if directly added
        elif line.startswith("~"):
            key, expression = line[1:].split("=")
            key = key.strip()
            expression = expression.strip()
            if key in self.current_state:  # overwrite (deletes and wait to be eval'd) previous var or eval'd expr
                if self.verbose:
                    print(f"Warning: {key} already defined, previous definition in current_stateas {self.current_state[key]} will be removed and {expression} will be added to raw_expressions.")
                del self.current_state[key]  # deletes previous var/eval'd expr from current_state
            # avoid x = x, treat as x = "x"
            if key == expression:
                if self.verbose:
                    print(f"Warning: Expression {key} is self-referencing, treating as string and not recording as expression")
                self.current_state[key] = expression
            else:
                self.raw_expressions[key] = expression

    @staticmethod
    def eval_f_string(s, vars_dict) -> str:
        return eval(f"f'''{s}'''", {}, vars_dict)  # eval as f string (expression wrapped in f string)
    
    def eval_expressions_and_update_state(self) -> None:
        '''
        Evaluate the raw expressions using the current state, and update the current state
        '''
        for key, expression in self.raw_expressions.items():
            try:
                # eval an expression directly
                value = eval(expression, {}, self.current_state)
            except Exception as e:
                if verbose:
                    print(f"Error evaluating expression for {key}: {e}")
                    print(f"Falling back to treat expression as string")
                value = expression
            # update current state immediately
            self.current_state[key] = value
    
    def parse_text_line(self, line: str) -> None:
        '''
        Parse a text line by formatting it with the current state of variables and expressions, 
        and append it to self.parsed_lines. 
        
        If the line contains references to variable/expressions ({}s), 
            it triggers an update of the current state by evaluating the raw expressions using the current current_state.
        '''
        # early termination
        if line == '\n':  # emtpy new line
            self.parsed_lines.append(line)
            return
        if '{' not in line and '}' not in line:  # no variables or expressions
            self.parsed_lines.append(line)
            return
        if line.startswith("/"):  # disable parsing for this line (if {} is needed as a text symbol instead)
            self.parsed_lines.append(line[1:])
            return
        self.eval_expressions_and_update_state()
        formatted_line = MarkdownParser.eval_f_string(line, self.current_state)
        self.parsed_lines.append(formatted_line)

    def interpret_line(self, line: str) -> None:
        '''
        Interpret a line, be it definition (@/~) or text line, and parse accordingly.
        '''
        if MarkdownParser.is_definition_line(line):
            self.parse_definition_line(line)
        else:
            self.parse_text_line(line)
            
    def parse(self, md_filepath: str, output_filepath: str) -> None:
        '''
        Reads the markdown file, parses the content line-by-line, and writes to the output file, creating the output directory if necessary.
        '''
        if not os.path.exists(md_filepath):
            raise FileNotFoundError(f"File not found: {md_filepath}")
        with open(md_filepath, "r", encoding=self.encoding) as f:
            self.markdown_lines = f.readlines()
        for line in self.markdown_lines:
            self.interpret_line(line)
        if len(self.parsed_lines) == 0:
            raise ValueError("No content to write to the output: no parsed line recorded.")
        # check if output directory exists
        output_dir = os.path.dirname(output_filepath)
        if not os.path.exists(output_dir) and output_dir != '':
            if self.verbose:
                print(f"Creating output directory: {output_dir} for the output file: {output_filepath}")
            os.makedirs(output_dir)
        with open(output_filepath, 'w', encoding=self.encoding) as file:
            file.write(''.join(self.parsed_lines))
        print(f"Formatted content saved to {output_filepath}")
        



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Markdown Parser')
    # Add arguments
    parser.add_argument('md_path', type=str, help='Path to the markdown file')
    parser.add_argument('--output_suffix', '-s', type=str, default='parsed', help='Suffix for the output file')
    parser.add_argument('--forced_output_path', '-f', type=str, help='Path to the forced output file')
    parser.add_argument('--verbose', '-v', action='store_true', default=False, help='Print verbose output')
    parser.add_argument('--encoding', '-e', type=str, default='utf-8', help='Encoding for reading and writing files')
    # Parse the arguments
    _args = parser.parse_args()
    # Assign the parsed arguments to variables
    md_path = _args.md_path
    _output_suffix = _args.output_suffix
    _forced_output_path = _args.forced_output_path
    verbose = _args.verbose
    encoding = _args.encoding
    # Generate the output path
    output_path = f"{md_path[:-3]}_{_output_suffix}.md" if _forced_output_path is None else _forced_output_path
    if _forced_output_path is not None and _output_suffix != 'parsed':
        print("Warning: Ignoring output suffix as forced output path is provided")
    # Instantiate the parser
    parser = MarkdownParser(verbose=verbose, encoding=encoding)
    # Parse the markdown file
    parser.parse(md_path, output_path)
