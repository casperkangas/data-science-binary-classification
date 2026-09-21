import os
import requests
import pandas as pd
from urllib.parse import urlparse

def download_images(csv_path="books_data.csv", output_dir="data/images"):
    # Check if the CSV exists before proceeding
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Please run scraper.py first.")
        return

    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # List to keep track of local paths
    local_image_paths = []
    
    print(f"Downloading {len(df)} images...")
    
    for index, row in df.iterrows():
        url = row['image_url']
        
        # Use row index for a safe and unique filename: 'book_0001.jpg'
        filename = f"book_{index:04d}.jpg"
        local_path = os.path.join(output_dir, filename)
        
        # Only download if we haven't already
        if not os.path.exists(local_path):
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            except Exception as e:
                print(f"Failed to download {url}: {e}")
                local_image_paths.append(None)
                continue
                
        local_image_paths.append(local_path)
        
        if (index + 1) % 50 == 0:
            print(f"Downloaded {index + 1}/{len(df)} images...")
            
    # Add the new column for the local path
    df['local_image_path'] = local_image_paths
    
    # Save a new CSV so we have the references to the local files
    updated_csv_path = "books_data_with_images.csv"
    df.to_csv(updated_csv_path, index=False)
    print(f"Done! Updated data saved to {updated_csv_path}")

if __name__ == "__main__":
    download_images()

