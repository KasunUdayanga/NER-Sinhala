# First install required packages
# pip install transformers datasets torch scikit-learn seqeval

from sklearn.model_selection import train_test_split
from datasets import Dataset
import torch
import numpy as np

def read_conll(file_path):
    """Read CoNLL format data with proper error handling"""
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
                parts = line.split()
                if len(parts) >= 2:  # Ensure at least token and label
                    word, tag = parts[0], parts[-1]  # First and last columns
                    sent.append(word)
                    lab.append(tag)
    if sent:  # last sentence
        sentences.append(sent)
        labels.append(lab)
    return sentences, labels

# 1. Read data
print("Loading CoNLL data...")
sentences, labels = read_conll("clean_dataset.conll")
unique_labels = sorted(set(tag for seq in labels for tag in seq))

# 2. Create dictionaries
label2id = {label: i for i, label in enumerate(unique_labels)}
id2label = {i: label for label, i in label2id.items()}

# 3. Print results
print(f"\nFound {len(sentences)} sentences with {len(unique_labels)} unique labels")
print("Unique Labels:", unique_labels)
print("Label → ID:", label2id)
print("ID → Label:", id2label)

if sentences:
    print("\nSample sentence:", sentences[0])
    print("Sample labels:", labels[0])

# 4. Split into train/val/test
train_sents, temp_sents, train_labels, temp_labels = train_test_split(
    sentences, labels, test_size=0.2, random_state=42)
val_sents, test_sents, val_labels, test_labels = train_test_split(
    temp_sents, temp_labels, test_size=0.5, random_state=42)

print(f"\nTrain: {len(train_sents)} sentences")
print(f"Validation: {len(val_sents)} sentences")
print(f"Test: {len(test_sents)} sentences")

# 5. Load tokenizer
from transformers import AutoTokenizer

print("\nLoading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

# 6. Prepare datasets
def prepare_dataset(sentences, labels):
    """Convert sentences and labels to Dataset format with proper tokenization"""
    # Convert list of token/label sequences to dataset dict
    dataset_dict = {"tokens": sentences, "tags": labels}
    dataset = Dataset.from_dict(dataset_dict)
    
    # Tokenize and align labels
    def tokenize_and_align(examples):
        tokenized_inputs = tokenizer(
            examples["tokens"],
            truncation=True,
            is_split_into_words=True,
            padding="max_length",
            max_length=128
        )
        
        aligned_labels = []
        for i, label_seq in enumerate(examples["tags"]):
            word_ids = tokenized_inputs.word_ids(batch_index=i)
            label_ids = []
            
            for word_idx in word_ids:
                if word_idx is None or word_idx >= len(label_seq):
                    # Special tokens or out of bounds get -100
                    label_ids.append(-100)
                else:
                    # Use the actual label ID
                    label_ids.append(label2id[label_seq[word_idx]])
            
            aligned_labels.append(label_ids)
        
        tokenized_inputs["labels"] = aligned_labels
        return tokenized_inputs
    
    # Apply tokenization to entire dataset
    tokenized_dataset = dataset.map(
        tokenize_and_align,
        batched=True,
        remove_columns=dataset.column_names
    )
    
    return tokenized_dataset

print("\nPreparing datasets...")
train_dataset = prepare_dataset(train_sents, train_labels)
val_dataset = prepare_dataset(val_sents, val_labels)
test_dataset = prepare_dataset(test_sents, test_labels)

# 7. Initialize model
from transformers import AutoModelForTokenClassification, TrainingArguments, Trainer

print("\nInitializing model...")
model = AutoModelForTokenClassification.from_pretrained(
    "bert-base-multilingual-cased",
    num_labels=len(label2id),
    id2label=id2label,
    label2id=label2id
)

# 8. Set up training arguments - compatible with older transformers versions
try:
    # For newer versions
    training_args = TrainingArguments(
        output_dir="./ner_sinhala",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_dir="./logs",
        report_to="none",
        load_best_model_at_end=True,
    )
except TypeError:
    # For older versions
    training_args = TrainingArguments(
        output_dir="./ner_sinhala",
        eval_steps=500,             # Instead of evaluation_strategy
        save_steps=500,             # Instead of save_strategy
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_dir="./logs",
        load_best_model_at_end=True,
    )

# 9. Initialize trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
)

# 10. Train model
print("\nTraining model...")
trainer.train()

# 11. Evaluate
print("\nEvaluating model...")
from seqeval.metrics import classification_report

# Make predictions
predictions, labels, _ = trainer.predict(test_dataset)
predictions = np.argmax(predictions, axis=-1)

# Convert IDs back to labels
true_labels = []
pred_labels = []

for prediction, label in zip(predictions, labels):
    true_sequence = []
    pred_sequence = []
    
    for pred_id, true_id in zip(prediction, label):
        if true_id != -100:  # Skip special tokens
            true_sequence.append(id2label[true_id])
            pred_sequence.append(id2label[pred_id])
    
    true_labels.append(true_sequence)
    pred_labels.append(pred_sequence)

# Print classification report
print("\nClassification Report:")
print(classification_report(true_labels, pred_labels))

# 12. Save model
print("\nSaving model...")
model.save_pretrained("./ner_sinhala_model")
tokenizer.save_pretrained("./ner_sinhala_model")
print("Model saved to ./ner_sinhala_model")

# 13. Test with a sample sentence
print("\nTesting with a sample sentence...")
from transformers import pipeline

nlp = pipeline("ner", model="./ner_sinhala_model", tokenizer="./ner_sinhala_model")

# Sample sentence - replace with your own Sinhala text
sample = "අපිත් ආදරෙයි සර් ඔබතුමාට"
tokens = sample.split()
result = nlp(tokens)

print(f"\nSample: {sample}")
print("NER Results:")
for item in result:
    if isinstance(item, list):
        for entity in item:
            print(f"- {entity['word']}: {entity['entity']}")
    else:
        print(f"- {item['word']}: {item['entity']}")

print("\nTraining complete! Your Sinhala NER model is ready to use.")