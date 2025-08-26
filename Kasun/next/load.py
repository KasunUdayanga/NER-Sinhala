from sklearn.model_selection import train_test_split

def read_conll(file_path):
    sentences, labels = [], []
    sent, lab = [], []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:  # sentence boundary
                if sent:
                    sentences.append(sent)
                    labels.append(lab)
                    sent, lab = [], []
            else:
                word, tag = line.split()
                sent.append(word)
                lab.append(tag)
    if sent:  # last sentence
        sentences.append(sent)
        labels.append(lab)
    return sentences, labels

sentences, labels = read_conll("clean_dataset.conll")
unique_labels = sorted(set(tag for seq in labels for tag in seq))

# 2. Create dictionaries
label2id = {label: i for i, label in enumerate(unique_labels)}
id2label = {i: label for label, i in label2id.items()}

# 3. Print results
print("Unique Labels:", unique_labels)
print("Label → ID:", label2id)
print("ID → Label:", id2label)

print(sentences[0])
print(labels[0])
train_sents, temp_sents, train_labels, temp_labels = train_test_split(sentences, labels, test_size=0.2)
val_sents, test_sents, val_labels, test_labels = train_test_split(temp_sents, temp_labels, test_size=0.5)
