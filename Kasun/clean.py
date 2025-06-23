import pandas as pd
import os

def clean_dataset():
    """
    Remove source_file and original_column from clean_text_data.csv
    """
    # File path
    clean_file = 'clean_text_data.csv'
    
    if not os.path.exists(clean_file):
        print(f"❌ File not found: {clean_file}")
        return
    
    print(f"🧹 Cleaning dataset: {clean_file}")
    
    # Read the file
    df = pd.read_csv(clean_file, encoding='utf-8-sig')
    
    print(f"📋 Original columns: {list(df.columns)}")
    print(f"📊 Original rows: {len(df)}")
    
    # Keep only id and text columns
    columns_to_keep = ['id', 'text']
    
    # Check if columns exist
    missing_columns = [col for col in columns_to_keep if col not in df.columns]
    if missing_columns:
        print(f"❌ Missing columns: {missing_columns}")
        return
    
    # Create cleaned dataframe
    df_cleaned = df[columns_to_keep]
    
    # Save the cleaned file
    df_cleaned.to_csv(clean_file, index=False, encoding='utf-8-sig')
    
    print(f"✅ Removed columns: source_file, original_column")
    print(f"📋 Remaining columns: {list(df_cleaned.columns)}")
    print(f"📊 Total rows: {len(df_cleaned)}")
    print(f"💾 Cleaned file saved: {clean_file}")

if __name__ == "__main__":
    clean_dataset()
