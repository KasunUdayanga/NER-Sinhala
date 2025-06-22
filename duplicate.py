import csv

def remove_duplicate_rows(input_csv, output_csv):
    seen = set()
    unique_rows = []

    with open(input_csv, "r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        for row in reader:
            row_tuple = tuple(cell.strip() for cell in row)
            if row_tuple not in seen:
                seen.add(row_tuple)
                unique_rows.append(row)

    with open(output_csv, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(unique_rows)

    print(f"Removed duplicates. Saved {len(unique_rows)} unique rows to '{output_csv}'.")

# Example usage:
remove_duplicate_rows("OldPolitician.csv", "sinhala_output2.csv")
