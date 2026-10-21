import pandas as pd
import re
import os
import unicodedata

def clean_text(text):
    if pd.isna(text):
        return ""
    text = unicodedata.normalize("NFKC", str(text)).lower()

    # Keep letters, accents, numbers, and punctuation for the vectorizer
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def clean_data(input_csv="books_data_full.csv", output_csv="books_data_clean.csv"):
    if not os.path.exists(input_csv):
        print(f"Error: {input_csv} not found.")
        return
        
    print(f"Loading {input_csv}...")
    df = pd.read_csv(input_csv, encoding='utf-8')
    
    print("Cleaning textual data (Titles and Descriptions)...")
    # Instead of creating new columns, just overwrite the existing ones to save space
    df['title'] = df['title'].apply(clean_text)
    df['description'] = df['description'].apply(clean_text)
    
    # Drop rows that ended up with completely empty descriptions after cleaning
    initial_len = len(df)
    df = df[df['description'] != ""]
    print(f"Dropped {initial_len - len(df)} books that lacked usable descriptions.")
    
    # Keep only the columns strictly needed for our machine learning tasks
    columns_to_keep = ['title', 'category', 'description', 'local_image_path']
    final_cols = [c for c in columns_to_keep if c in df.columns]
    df = df[final_cols]
    
    print(f"Saving cleaned dataset to {output_csv}...")
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print("Done!")

if __name__ == "__main__":
    clean_data()
