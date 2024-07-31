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


### HELPERS ###
class MarkdownParser():
    def __init__(self, verbose: bool=False) -> None:
        self.variables = {}
        self.raw_expressions = {}
        self.markdown_lines = []
        self.parsed_lines = []

        self.verbose = verbose
    
    @staticmethod
    def is_definition_line(line: str):
        '''
        Identify a definition line with @/~ prefix and = in it
        '''
        has_prefix = line.startswith("@") or line.startswith("~")
        has_equals = "=" in line
        return has_prefix and has_equals
    
    @staticmethod
    def parse_value(value: str):
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

    def parse_definition_line(self, line: str):
        '''
        Parse a definition line: 
             - if it's a variable definition (@), 
             parse and store it, or update it if exists (just dict anyways)
             - if it's an expression definition (~), 
             store it as raw expression and evaluate it later (supports dynamic variables)
        
        When same name is used to define the other type of var, 
            it will overwrite the previous definition, 
            meaning that the previous definition will be lost. 
        '''
        if line.startswith("@"):
            key, value = line[1:].split("=")
            key = key.strip()
            if key in self.raw_expressions:
                if self.verbose:
                    print(f"Warning: Expression {key} already defined as expression, overwriting as variable")
                del self.raw_expressions[key]
            value = MarkdownParser.parse_value(value.strip())
            self.variables[key] = value
        elif line.startswith("~"):
            key, expression = line[1:].split("=")
            key = key.strip()
            if key in self.variables:
                if self.verbose:
                    print(f"Warning: Variable {key} already defined, overwriting as expression")
                del self.variables[key]
            expression = expression.strip()
            self.raw_expressions[key] = expression

    @staticmethod
    def eval_f_string(s, vars_dict):
        return eval(f"f'''{s}'''", {}, vars_dict)
    
    def evaluate_expressions(self):
        '''
        Evaluate the raw expressions using the current variables
        '''
        cur_exprs = {}
        for key, expression in self.raw_expressions.items():
            try:
                value = eval(expression, {}, self.variables)
            except Exception as e:
                if verbose:
                    print(f"Error evaluating expression for {key}: {e}")
                    print(f"Falling back to treat expression as string")
                value = expression
            cur_exprs[key] = value
        return cur_exprs
    
    def get_current_state(self):
        '''
        Get the current state of variables and evaluated expressions
        '''
        cur_vars = self.variables.copy()
        cur_exprs = self.evaluate_expressions()
        cur_vars.update(cur_exprs)
        return cur_vars
    
    def parse_text_line(self, line: str):
        '''
        Parse a text line by formatting it with the current state of variables and expressions, 
        and append it to the parsed lines
        '''
        cur_vars = self.get_current_state()
        formatted_line = MarkdownParser.eval_f_string(line, cur_vars)
        self.parsed_lines.append(formatted_line)

    def interpret_line(self, line: str):
        '''
        Interpret a line. 
        '''
        if MarkdownParser.is_definition_line(line):
            self.parse_definition_line(line)
        else:
            self.parse_text_line(line)
            
    def parse(self, md_filepath: str, output_filepath: str, 
              encoding: str='utf-8'):
        '''
        Reads the markdown file, parses the content line-by-line, and writes to the output file, creating the output directory if necessary.
        '''
        if not os.path.exists(md_filepath):
            raise FileNotFoundError(f"File not found: {md_filepath}")
        with open(md_filepath, "r") as f:
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
        with open(output_filepath, 'w', encoding=encoding) as file:
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
    parser = MarkdownParser(verbose=verbose)
    # Parse the markdown file
    parser.parse(md_path, output_path, encoding)
