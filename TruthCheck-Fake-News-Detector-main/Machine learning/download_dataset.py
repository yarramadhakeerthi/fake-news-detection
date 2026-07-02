"""
Script to download the Fake News Detection dataset
This will download a standard fake news dataset from a public source
"""
import pandas as pd
import urllib.request
import os

print("=" * 60)
print("Downloading Fake News Detection Dataset")
print("=" * 60)

# Option 1: Try to download from a public URL
dataset_urls = [
    # Common fake news dataset URLs (you may need to update these)
    "https://raw.githubusercontent.com/supercoder123/fake-news-detection/main/news.csv",
    # Add more URLs if needed
]

def download_dataset():
    """Try to download dataset from available sources"""
    for url in dataset_urls:
        try:
            print(f"\nAttempting to download from: {url}")
            urllib.request.urlretrieve(url, "news_temp.csv")
            
            # Verify it's a valid CSV
            df = pd.read_csv("news_temp.csv", nrows=5)
            if 'text' in df.columns and 'label' in df.columns:
                os.replace("news_temp.csv", "news.csv")
                print("✓ Dataset downloaded successfully!")
                return True
            else:
                os.remove("news_temp.csv")
                print("✗ Invalid format")
        except Exception as e:
            print(f"✗ Failed: {e}")
            if os.path.exists("news_temp.csv"):
                os.remove("news_temp.csv")
    
    return False

# Try to download
if not download_dataset():
    print("\n" + "=" * 60)
    print("Automatic download failed.")
    print("=" * 60)
    print("\nPlease download the dataset manually:")
    print("1. Go to: https://www.kaggle.com/datasets")
    print("2. Search for 'fake news' or 'fake and real news dataset'")
    print("3. Download a dataset with columns: title, text, label")
    print("4. Save it as 'news.csv' in this directory")
    print("\nOr use this direct link if available:")
    print("https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset")
    print("\nExpected CSV format:")
    print("  - Columns: title, text, label")
    print("  - Label values: 'FAKE' or 'REAL'")
    exit(1)

# Verify the downloaded dataset
print("\n" + "=" * 60)
print("Verifying dataset...")
print("=" * 60)

try:
    df = pd.read_csv("news.csv")
    print(f"✓ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"✓ Columns: {list(df.columns)}")
    
    if 'label' in df.columns:
        print(f"✓ Label distribution:")
        print(df['label'].value_counts().to_string())
    
    print("\n✓ Dataset is ready for model training!")
    
except Exception as e:
    print(f"✗ Error verifying dataset: {e}")
    exit(1)

