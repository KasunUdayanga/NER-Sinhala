import pandas as pd
import os
import glob

def combine_all_csv_files():
    """
    Combine all CSV files in the current folder into one master file
    """
    # Get current directory (Kasun folder)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"🔍 Working in directory: {current_dir}")
    
    # Find all CSV files in current directory
    csv_files = glob.glob(os.path.join(current_dir, "*.csv"))
    csv_files = [f for f in csv_files if not f.endswith('_combined.csv')]  # Exclude previous combined files
    
    print(f"📄 Found {len(csv_files)} CSV files:")
    for file in csv_files:
        print(f"   - {os.path.basename(file)}")
    
    if not csv_files:
        print("❌ No CSV files found in current directory!")
        return None
    
    # List to store all data
    all_data = []
    
    # Process each CSV file
    for file_path in csv_files:
        filename = os.path.basename(file_path)
        print(f"\n📖 Processing: {filename}")
        
        try:
            # Try to read with different encodings
            df = None
            encodings = ['utf-8', 'utf-8-sig', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    print(f"   ✅ Read with {encoding} encoding")
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                print(f"   ❌ Could not read {filename} with any encoding")
                continue
            
            # Add source file column
            df['source_file'] = filename
            df['file_id'] = len(all_data) + 1
            
            # Add to combined data
            all_data.append(df)
            print(f"   📊 Added {len(df)} rows from {filename}")
            
        except Exception as e:
            print(f"   ❌ Error processing {filename}: {e}")
    
    if not all_data:
        print("❌ No data was successfully read from any file!")
        return None
    
    # Combine all DataFrames
    print(f"\n🔄 Combining {len(all_data)} files...")
    combined_df = pd.concat(all_data, ignore_index=True, sort=False)
    
    # Add master index
    combined_df.reset_index(drop=True, inplace=True)
    combined_df['master_id'] = range(1, len(combined_df) + 1)
    
    # Reorder columns to put master_id first
    cols = ['master_id'] + [col for col in combined_df.columns if col != 'master_id']
    combined_df = combined_df[cols]
    
    # Save combined file
    output_filename = os.path.join(current_dir, 'all_csv_combined.csv')
    combined_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    
    print(f"\n🎉 Combined file created: {output_filename}")
    print(f"📊 Total rows: {len(combined_df)}")
    print(f"📋 Total columns: {len(combined_df.columns)}")
    print(f"📁 Files included: {combined_df['source_file'].nunique()}")
    
    # Show file distribution
    print(f"\n📈 Data distribution by file:")
    file_counts = combined_df['source_file'].value_counts()
    for file, count in file_counts.items():
        print(f"   {file}: {count} rows")
    
    # Show column information
    print(f"\n📋 Columns in combined dataset:")
    for i, col in enumerate(combined_df.columns, 1):
        print(f"   {i}. {col}")
    
    return output_filename

def create_clean_dataset(input_file):
    """
    Create a cleaned version focusing on text data
    """
    df = pd.read_csv(input_file, encoding='utf-8-sig')
    
    # Find text columns (likely to contain comments or text data)
    text_columns = []
    for col in df.columns:
        if any(keyword in col.lower() for keyword in ['comment', 'text', 'sinhala', 'content']):
            text_columns.append(col)
    
    if text_columns:
        print(f"\n🧹 Creating clean dataset with text columns: {text_columns}")
        
        clean_data = []
        for _, row in df.iterrows():
            for text_col in text_columns:
                text_value = str(row[text_col]).strip()
                if text_value and text_value != 'nan' and len(text_value) > 5:
                    clean_data.append({
                        'id': len(clean_data) + 1,
                        'text': text_value,
                        'source_file': row['source_file'],
                        'original_column': text_col
                    })
        
        if clean_data:
            clean_df = pd.DataFrame(clean_data)
            clean_filename = os.path.join(os.path.dirname(input_file), 'clean_text_data.csv')
            clean_df.to_csv(clean_filename, index=False, encoding='utf-8-sig')
            
            print(f"✅ Clean dataset created: {clean_filename}")
            print(f"📊 Clean text entries: {len(clean_df)}")
            return clean_filename
    
    return None

def remove_unwanted_columns(clean_file):
    """
    Remove source_file and original_column from the clean dataset
    """
    if clean_file and os.path.exists(clean_file):
        print(f"\n🧹 Removing unwanted columns from: {clean_file}")
        
        # Read the clean dataset
        df = pd.read_csv(clean_file, encoding='utf-8-sig')
        
        print(f"📋 Original columns: {list(df.columns)}")
        
        # Keep only id and text columns
        columns_to_keep = ['id', 'text']
        df_cleaned = df[columns_to_keep]
        
        # Save the cleaned file
        df_cleaned.to_csv(clean_file, index=False, encoding='utf-8-sig')
        
        print(f"✅ Removed columns: source_file, original_column")
        print(f"📋 Remaining columns: {list(df_cleaned.columns)}")
        print(f"📊 Total rows: {len(df_cleaned)}")
        
        return clean_file
    
    return None

if __name__ == "__main__":
    print("🚀 Starting CSV combination process...")
    
    # Combine all CSV files
    combined_file = combine_all_csv_files()
    
    if combined_file:
        # Create clean dataset
        clean_file = create_clean_dataset(combined_file)
        
        if clean_file:
            # Remove unwanted columns
            remove_unwanted_columns(clean_file)
        
        print("\n✨ Process completed successfully!")
        print(f"📁 Files created:")
        print(f"   - Combined: {combined_file}")
        if clean_file:
            print(f"   - Clean text: {clean_file}")
    else:
        print("❌ Process failed!")