input_file = "lable_data1.conll"     # your original file
output_file = "clean_datasetts.conll"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        line = line.strip()
        
        # Skip DOCSTART and empty lines
        if not line or line.startswith("-DOCSTART-"):
            continue
        
        # Split columns
        parts = line.split()
        
        if len(parts) >= 2:
            word = parts[0].strip()
            label = parts[-1].strip().replace(" ", "")  # fix labels like "B- PER" -> "B-PER"
            
            # Write cleaned word + label (always one space)
            outfile.write(f"{word} {label}\n")

#remove all spaces and other unwanted characters