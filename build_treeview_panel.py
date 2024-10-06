import json

def count_leading_tabs(line):
    """Count the number of leading tabs in a line."""
    return len(line) - len(line.lstrip('\t'))

def convert_to_json(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()

    indent_stack = [1]
    json_lines = ['{']
    indent_diff = 0  # To keep track of indentation levels

    I = len(lines)

    for i, line in enumerate(lines):
        current_indent = count_leading_tabs(line)
        key = line.strip()
        
        # Determine the indentation of the next line
        if i + 1 < I:
            next_indent = count_leading_tabs(lines[i + 1])
        else:
            next_indent = 0  # No next line

        indent_diff = next_indent - current_indent

        # Prepare the key with proper indentation
        indent = '\t' * (indent_stack[-1])
        if indent_diff < 0:
            # Current key has children
            json_lines.append(f'{indent}"{key}": ""')
            while indent_diff < 0:
                indent_stack.pop()
                json_lines.append(f'{'\t' * (indent_stack[-1])}}}')
                indent_diff += 1
            if i < I:
                json_lines[-1] += ","
        elif indent_diff > 0:
            # Current key is a leaf and we need to close braces
            _ = indent_stack[-1]
            json_lines.append(f'{indent}"{key}": {{')
            indent_stack.append(_ + 1)
            # Close the braces outside the loop
        else:
            # Current key is a leaf
            json_lines.append(f'{indent}"{key}": "",')

    # Remove the last comma if exists
    if json_lines[-1].endswith(','):
        json_lines[-1] = json_lines[-1][:-1]

    # Close the root
    json_lines.append('}')

    # Join all lines into a single JSON string
    json_str = '\n'.join(json_lines)

    # Optional: Validate JSON by loading it
    try:
        parsed_json = json.loads(json_str)
    except json.JSONDecodeError as e:
        print("Error in generated JSON:", e)
        print("Generated JSON:")
        # print(json_str)
        # return

    # Write the JSON to the output file with indentation
    with open(output_file, 'w') as f:
        # json.dump(parsed_json, f, indent=2)
        f.write(json_str)

    print(f"JSON has been successfully written to {output_file}")

if __name__ == "__main__":
    input_file = 'TreeViewPanel.txt'   # Replace with your input file path
    output_file = 'TreeViewPanel.json'  # Replace with your desired output file path
    convert_to_json(input_file, output_file)