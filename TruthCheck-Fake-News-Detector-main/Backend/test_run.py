#!/usr/bin/env python
"""Test script to run the Flask app and capture all output"""
import sys
import traceback

try:
    print("=" * 60)
    print("Starting Fake News Detector Server")
    print("=" * 60)
    
    # Test imports
    print("\n[1/4] Testing imports...")
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    import pickle
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    print("✓ All imports successful")
    
    # Test file existence
    print("\n[2/4] Checking files...")
    import os
    files_to_check = ['finalized_model.pkl', 'tfidf_vectorizer.pkl', 'news.csv']
    for file in files_to_check:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✓ {file} exists ({size} bytes)")
        else:
            print(f"✗ {file} NOT FOUND")
    
    # Test model loading
    print("\n[3/4] Loading model...")
    try:
        with open('finalized_model.pkl', 'rb') as f:
            model = pickle.load(f)
        print(f"✓ Model loaded: {type(model)}")
    except Exception as e:
        print(f"✗ Model loading failed: {e}")
        print(f"  Error type: {type(e).__name__}")
        traceback.print_exc()
        model = None
    
    # Test vectorizer loading
    print("\n[4/4] Loading vectorizer...")
    try:
        with open('tfidf_vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        print(f"✓ Vectorizer loaded: {type(vectorizer)}")
    except Exception as e:
        print(f"✗ Vectorizer loading failed: {e}")
        print(f"  Error type: {type(e).__name__}")
        traceback.print_exc()
        vectorizer = None
        
        # Try fallback
        if os.path.exists('news.csv'):
            print("  Attempting fallback from news.csv...")
            try:
                df = pd.read_csv("news.csv")
                vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
                vectorizer.fit(df["text"])
                print("✓ Vectorizer initialized from CSV")
            except Exception as e2:
                print(f"✗ Fallback failed: {e2}")
                vectorizer = None
    
    # Now run the actual app
    print("\n" + "=" * 60)
    print("Starting Flask server...")
    print("=" * 60)
    print(f"Model loaded: {model is not None}")
    print(f"Vectorizer loaded: {vectorizer is not None}")
    print("Server will be available at: http://localhost:5001")
    print("Press Ctrl+C to stop")
    print("=" * 60 + "\n")
    
    # Import and run app
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
    
except KeyboardInterrupt:
    print("\n\nServer stopped by user")
    sys.exit(0)
except Exception as e:
    print(f"\n\nFATAL ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

