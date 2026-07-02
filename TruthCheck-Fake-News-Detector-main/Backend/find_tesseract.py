"""
Helper script to find Tesseract installation or set the path manually
"""

import os
import sys

print("=" * 60)
print("Tesseract Path Finder")
print("=" * 60)

# Common installation paths
possible_paths = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    r'C:\Tesseract-OCR\tesseract.exe',
]

# Check user-specific paths
username = os.getenv('USERNAME', '')
if username:
    possible_paths.extend([
        r'C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe'.format(username),
        r'C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'.format(username),
    ])

print("\nSearching for Tesseract in common locations...\n")

found_paths = []
for path in possible_paths:
    if os.path.exists(path):
        found_paths.append(path)
        print(f"✓ Found: {path}")

if not found_paths:
    print("✗ Tesseract not found in common locations")
    print("\nPlease enter the path to your Tesseract installation:")
    print("(Example: C:\\Program Files\\Tesseract-OCR\\tesseract.exe)")
    
    manual_path = input("\nEnter Tesseract path (or press Enter to skip): ").strip()
    
    if manual_path:
        # Remove quotes if present
        manual_path = manual_path.strip('"').strip("'")
        
        if os.path.exists(manual_path):
            found_paths.append(manual_path)
            print(f"✓ Valid path: {manual_path}")
        else:
            print(f"✗ Path does not exist: {manual_path}")
            sys.exit(1)
    else:
        print("\nNo path provided. Please:")
        print("1. Find where you installed Tesseract")
        print("2. Run this script again and enter the path")
        print("3. Or add Tesseract to your system PATH")
        sys.exit(1)

if found_paths:
    print("\n" + "=" * 60)
    print("Configuration for app.py:")
    print("=" * 60)
    print("\nAdd this line to app.py (after the pytesseract import):")
    print(f"\npytesseract.pytesseract.tesseract_cmd = r'{found_paths[0]}'")
    print("\nOr add this to your system PATH environment variable:")
    tesseract_dir = os.path.dirname(found_paths[0])
    print(f"  {tesseract_dir}")

