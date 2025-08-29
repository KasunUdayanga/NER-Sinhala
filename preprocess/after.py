def remove_duplicates(input_file, output_file):
    """
    Removes duplicate lines from a NER dataset file.
    
    Args:
        input_file (str): Path to the input file
        output_file (str): Path to save the deduplicated file
    """
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Remove duplicates while preserving order
    seen = set()
    deduplicated_lines = []
    
    for line in lines:
        line = line.strip()
        if line not in seen:
            seen.add(line)
            deduplicated_lines.append(line)
        # Keep empty lines for sequence separation
        elif not line:
            deduplicated_lines.append(line)
    
    # Write the deduplicated data to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(deduplicated_lines))
    
    print(f"Duplicates removed. Original lines: {len(lines)}, Deduplicated lines: {len(deduplicated_lines)}")

# Example usage
input_file = "After.conll"  # Replace with your input file path
output_file = "deduplicated_dataset.txt"  # Replace with your output file path

remove_duplicates(input_file, output_file)