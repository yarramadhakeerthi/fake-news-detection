"""
Test script to verify Tesseract OCR installation and configuration
Run this script to diagnose Tesseract issues
"""

import sys
import os

print("=" * 60)
print("Tesseract OCR Diagnostic Test")
print("=" * 60)

# Test 1: Check if pytesseract is installed
print("\n1. Checking pytesseract installation...")
try:
    import pytesseract
    print("   ✓ pytesseract is installed")
except ImportError:
    print("   ✗ pytesseract is NOT installed")
    print("   → Install with: pip install pytesseract")
    sys.exit(1)

# Test 2: Check Tesseract executable
print("\n2. Checking Tesseract executable...")
import platform

if platform.system() == 'Windows':
    # Check common Windows paths
    possible_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    ]
    
    # Check user-specific path
    username = os.getenv('USERNAME', '')
    if username:
        possible_paths.append(r'C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe'.format(username))
    
    tesseract_found = False
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            print(f"   ✓ Found Tesseract at: {path}")
            tesseract_found = True
            break
    
    if not tesseract_found:
        print("   ⚠ Tesseract not found in common paths")
        print("   Checking system PATH...")
        try:
            import subprocess
            result = subprocess.run(['tesseract', '--version'], 
                                  capture_output=True, 
                                  timeout=2)
            if result.returncode == 0:
                print("   ✓ Tesseract found in system PATH")
                tesseract_found = True
        except:
            pass
    
    if not tesseract_found:
        print("   ✗ Tesseract executable NOT found")
        print("\n   SOLUTION:")
        print("   1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   2. Install it (default location: C:\\Program Files\\Tesseract-OCR)")
        print("   3. Either:")
        print("      a) Add it to your system PATH, OR")
        print("      b) Set the path in app.py:")
        print("         pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'")
        sys.exit(1)
else:
    print("   Checking system PATH...")
    try:
        import subprocess
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, 
                              timeout=2)
        if result.returncode == 0:
            print("   ✓ Tesseract found in system PATH")
        else:
            print("   ✗ Tesseract not found")
            sys.exit(1)
    except FileNotFoundError:
        print("   ✗ Tesseract not found in PATH")
        print("   → Install with: brew install tesseract (macOS) or sudo apt-get install tesseract-ocr (Linux)")
        sys.exit(1)

# Test 3: Get Tesseract version
print("\n3. Getting Tesseract version...")
try:
    version = pytesseract.get_tesseract_version()
    print(f"   ✓ Tesseract version: {version}")
except Exception as e:
    print(f"   ✗ Error getting version: {e}")
    sys.exit(1)

# Test 4: Test OCR with a simple image
print("\n4. Testing OCR functionality...")
try:
    from PIL import Image, ImageDraw, ImageFont
    import io
    
    # Create a simple test image with text
    img = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img)
    test_text = "Hello Tesseract"
    draw.text((50, 80), test_text, fill='black')
    
    # Try to extract text
    extracted = pytesseract.image_to_string(img).strip()
    
    if extracted:
        print(f"   ✓ OCR test successful!")
        print(f"   → Extracted text: '{extracted}'")
    else:
        print("   ⚠ OCR test completed but no text extracted")
        print("   → This might be normal for simple test images")
        
except ImportError:
    print("   ⚠ PIL/Pillow not available - skipping OCR test")
    print("   → Install with: pip install Pillow")
except Exception as e:
    print(f"   ✗ OCR test failed: {e}")
    print("   → Check Tesseract installation and configuration")

print("\n" + "=" * 60)
print("Diagnostic complete!")
print("=" * 60)
print("\nIf all tests passed, Tesseract should work with the API.")
print("If any test failed, follow the instructions above to fix the issue.")

