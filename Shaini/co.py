input_file = "Lraw.conll"      # your original file
output_file = "clean_datasetaa.conll"   # cleaned dataset

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        line = line.strip()
        if not line:
            outfile.write("\n")  # keep sentence boundaries
            continue
        if line.startswith("-DOCSTART-"):  # skip DOCSTART
            continue
        parts = line.split()
        if len(parts) >= 2:
            word = parts[0]
            label = parts[-1]  # last column is NER label
            outfile.write(f"{word} {label}\n")
#create as for using as dataset