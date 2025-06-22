import csv

def remove_commas_only(input_file, output_file):
    cleaned_rows = []

    with open(input_file, newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        for row in reader:
            if row:
                # Remove all comma characters
                cleaned_name = row[0].replace(',', '')
                cleaned_rows.append([cleaned_name.strip()])

    with open(output_file, 'w', newline='', encoding='utf-8-sig') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(cleaned_rows)

    print(f"✅ Comma-free names saved to: {output_file}")

# === USAGE ===
input_file = 'OldPolitician.csv'       # Input CSV (no header, one name per line)
output_file = 'OldPolitician_cleaned.csv'  # Output CSV

remove_commas_only(input_file, output_file)
