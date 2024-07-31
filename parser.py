import argparse

# Create an argument parser
parser = argparse.ArgumentParser(description='Markdown Parser')

# Add arguments
parser.add_argument('md_path', type=str, help='Path to the markdown file')
parser.add_argument('--output_suffix', '-s', type=str, default='parsed', help='Suffix for the output file')
parser.add_argument('--forced_output_path', '-f',  type=str, help='Path to the forced output file')

# Parse the arguments
args = parser.parse_args()

# Assign the parsed arguments to variables
md_path = args.md_path
output_suffix = args.output_suffix
forced_output_path = args.forced_output_path

# Generate the output path
output_path = f"{md_path[:-3]}_{output_suffix}.md" if forced_output_path is None else forced_output_path

if forced_output_path is not None and output_suffix != 'parsed':
    print("Warning: Ignoring output suffix as forced output path is provided")

'''
Expected Markdown Format: 

 - Variables are defined individually on a new line: @<var>=<value>
 - Other contents untouched

Upon running the script, the variables will be parsed and formatted into the markdown content.
'''

# helper methods
def parse_strings_to_vars(strings):
    variables = {}
    for string in strings:
        # Remove the "@" symbol and split the string into key and value
        key, value = string[1:].split('=')
        key = key.strip()
        value = value.strip()
        
        # Assign the value to the key in the variables dictionary
        variables[key] = value

    return variables

def format_and_save_markdown(text_list, variables, output_file):
    # Create a dictionary from the variables to use in string formatting
    variables_dict = {key: value for key, value in variables.items()}

    # Format each line in the text list using the variables
    formatted_lines = [line.format(**variables_dict) for line in text_list]

    # Join the formatted lines into a single string
    formatted_content = ''.join(formatted_lines)

    # Write the formatted content to the output file
    with open(output_file, 'w') as file:
        file.write(formatted_content)

# main
with open(md_path, "r") as f:
    md = f.readlines()

defs = []
body = []
for line in md:
    if line.startswith("@") and "=" in line:
        defs.append(line.strip())
    else:
        body.append(line)

vars = parse_strings_to_vars(defs)
format_and_save_markdown(body, vars, output_path)
print(f"Formatted content saved to {output_path}")
