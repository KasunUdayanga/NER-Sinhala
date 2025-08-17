import csv

input_path = r"e:\campus\CAMPUS\Research\NER-Sinhala\PoliticianNames.csv"
output_path = r"e:\campus\CAMPUS\Research\NER-Sinhala\PoliticianNames_labeled_space.txt"

# Read politician names and write as: "<name> B-PER" (space-separated, no commas, no header)
with open(input_path, "r", encoding="utf-8-sig") as fin, \
     open(output_path, "w", encoding="utf-8-sig", newline="") as fout:
    for line in fin:
        name = line.strip()
        if not name:
            continue
        # remove any commas inside the name just in case
        name = name.replace(",", "")
        fout.write(f"{name} B-PER\n")

print(f"Saved (space-separated): {output_path}")