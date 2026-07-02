"""
Script to regenerate the Fake News Detection model and vectorizer
This script recreates the model files needed for the Flask backend
"""
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import os

print("=" * 60)
print("Fake News Detection Model Regeneration")
print("=" * 60)

# Step 1: Load the dataset
print("\n[1/6] Loading dataset...")
try:
    df = pd.read_csv("news.csv")
    print(f"✓ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
except Exception as e:
    print(f"✗ Error loading dataset: {e}")
    exit(1)

# Step 2: Check for null values
print("\n[2/6] Checking data quality...")
null_count = df.isnull().sum().sum()
if null_count > 0:
    print(f"⚠ Warning: {null_count} null values found")
    df = df.dropna()
    print(f"✓ Data cleaned: {df.shape[0]} rows remaining")
else:
    print("✓ No null values found")

# Step 3: Prepare features and labels
print("\n[3/6] Preparing features and labels...")
labels = df['label']
texts = df['text']
print(f"✓ Labels: {labels.value_counts().to_dict()}")
print(f"✓ Total samples: {len(texts)}")

# Step 4: Split the data
print("\n[4/6] Splitting data into train/test sets...")
x_train, x_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=20
)
print(f"✓ Training samples: {len(x_train)}")
print(f"✓ Test samples: {len(x_test)}")

# Step 5: Initialize and fit the vectorizer
print("\n[5/6] Creating and fitting TF-IDF vectorizer...")
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
tf_train = vectorizer.fit_transform(x_train)
tf_test = vectorizer.transform(x_test)
print(f"✓ Vectorizer fitted: {len(vectorizer.vocabulary_)} features")

# Step 6: Train the model
print("\n[6/6] Training PassiveAggressiveClassifier...")
model = PassiveAggressiveClassifier(max_iter=50)
model.fit(tf_train, y_train)
print("✓ Model trained successfully")

# Step 7: Evaluate the model
print("\n[7/7] Evaluating model...")
y_pred = model.predict(tf_test)
score = accuracy_score(y_test, y_pred)
print(f"✓ Accuracy: {round(score * 100, 2)}%")

# Confusion matrix
cm = confusion_matrix(y_test, y_pred, labels=['FAKE', 'REAL'])
print(f"\nConfusion Matrix:")
print(f"  FAKE: {cm[0]}")
print(f"  REAL: {cm[1]}")

# Step 8: Save the model
print("\n" + "=" * 60)
print("Saving model files...")
print("=" * 60)

try:
    # Save the model
    model_filename = 'finalized_model.pkl'
    with open(model_filename, 'wb') as f:
        pickle.dump(model, f)
    file_size = os.path.getsize(model_filename)
    print(f"✓ Model saved: {model_filename} ({file_size:,} bytes)")
    
    # Save the vectorizer
    vectorizer_filename = 'tfidf_vectorizer.pkl'
    with open(vectorizer_filename, 'wb') as f:
        pickle.dump(vectorizer, f)
    file_size = os.path.getsize(vectorizer_filename)
    print(f"✓ Vectorizer saved: {vectorizer_filename} ({file_size:,} bytes)")
    
    print("\n" + "=" * 60)
    print("✓ Model regeneration complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Copy the .pkl files to the Backend directory:")
    print("   - finalized_model.pkl")
    print("   - tfidf_vectorizer.pkl")
    print("\n2. Restart the Flask server")
    
except Exception as e:
    print(f"\n✗ Error saving files: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

