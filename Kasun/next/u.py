# Suppose you already loaded your dataset into `labels` (list of lists)
# Example: labels = [["B-Other", "B-Other", "B-PER"], ["O", "B-LOC"]]

# 1. Get unique labels
unique_labels = sorted(set(tag for seq in labels for tag in seq))

# 2. Create dictionaries
label2id = {label: i for i, label in enumerate(unique_labels)}
id2label = {i: label for label, i in label2id.items()}

# 3. Print results
print("Unique Labels:", unique_labels)
print("Label → ID:", label2id)
print("ID → Label:", id2label)
