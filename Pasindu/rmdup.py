import pandas as pd

def process_comments(input_file, output_file):
    """
    Process Sinhala comments:
    1. Combine all comments into one text
    2. Remove duplicate words
    3. Create new comments of 200 words each
    
    Parameters:
    input_file (str): Path to the input CSV file
    output_file (str): Path to save the processed CSV file
    """
    try:
        # Read the CSV file with UTF-8 encoding
        df = pd.read_csv(input_file, encoding='utf-8')
        
        # Print information about the original dataframe
        print(f"Original CSV has {len(df)} rows and {len(df.columns)} columns")
        
        # Extract all comments and combine them into one string
        all_text = " ".join(df["text"].astype(str).tolist())
        print(f"Combined text has {len(all_text.split())} words")
        
        # Split into words and remove duplicates while preserving order
        words = all_text.split()
        unique_words = []
        seen = set()
        
        for word in words:
            if word.lower() not in seen:
                seen.add(word.lower())
                unique_words.append(word)
        
        print(f"After removing duplicates: {len(unique_words)} unique words")
        
        # Combine unique words back into one string
        deduplicated_text = " ".join(unique_words)
        
        # Split into chunks of approximately 200 words each
        word_chunks = []
        words = deduplicated_text.split()
        
        for i in range(0, len(words), 20):
            chunk = words[i:i+20]
            word_chunks.append(" ".join(chunk))
        
        print(f"Created {len(word_chunks)} comments with approximately 20 words each")
        
        # Create a new dataframe with the processed comments
        new_df = pd.DataFrame({
            "id": range(1, len(word_chunks) + 1),
            "text": word_chunks
        })
        
        # Save to CSV
        new_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Processed comments saved to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Replace these with your actual file paths
    input_csv_file = "clean_text_data.csv"
    output_csv_file = "processed_sinhala_comments.csv"
    
    process_comments(input_csv_file, output_csv_file)