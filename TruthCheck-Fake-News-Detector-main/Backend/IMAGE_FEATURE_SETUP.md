# Image-Based Fake News Detection Setup Guide

## Overview
The image detection feature uses OCR (Optical Character Recognition) to extract text from images and then analyzes that text using the existing fake news detection model.

## Prerequisites

### 1. Install Tesseract OCR

#### Windows:
1. Download Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (recommended: `tesseract-ocr-w64-setup-5.x.x.exe`)
3. During installation, note the installation path (default: `C:\Program Files\Tesseract-OCR`)
4. Add Tesseract to your system PATH:
   - Open System Properties → Environment Variables
   - Add `C:\Program Files\Tesseract-OCR` to PATH
   - Or set the path in your code (see below)

#### macOS:
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

### 2. Install Python Dependencies

```bash
pip install -r requirement.txt
```

This will install:
- `Pillow` - Image processing
- `pytesseract` - Python wrapper for Tesseract OCR
- `opencv-python` - Additional image processing capabilities

### 3. Configure Tesseract Path (Windows only)

If Tesseract is not in your PATH, you can set it in `app.py`:

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## Usage

### API Endpoint

**POST** `/api/predict-image`

**Request:**
- Method: `multipart/form-data`
- Field: `image` (file upload)
- Supported formats: PNG, JPG, JPEG, GIF, BMP, WEBP
- Max file size: 10MB

**Response:**
```json
{
    "prediction": "FAKE" or "REAL",
    "is_fake": true or false,
    "extracted_text": "Text extracted from image...",
    "extracted_text_length": 123,
    "image_metadata": {
        "format": "PNG",
        "size": [400, 200],
        "mode": "RGB",
        "file_size_kb": 45.2
    },
    "message": "Image analysis completed successfully"
}
```

### Frontend Usage

1. Navigate to the "Image Analysis" section
2. Click or drag and drop an image
3. Click "Analyze Image"
4. View the results including extracted text and prediction

## How It Works

1. **Image Upload**: User uploads an image file
2. **OCR Processing**: Tesseract OCR extracts text from the image
3. **Text Analysis**: Extracted text is analyzed using the existing text-based fake news detection model
4. **Metadata Analysis**: Basic image information is collected (format, size, etc.)
5. **Result**: Prediction is returned along with extracted text and metadata

## Troubleshooting

### "Tesseract not found" error
- Ensure Tesseract is installed and in your PATH
- On Windows, you may need to set the path explicitly in code
- Restart your terminal/IDE after installation

### "Could not extract sufficient text from image"
- Ensure the image contains readable text
- Try images with higher resolution
- Ensure text is not too small or blurry
- Check that the image format is supported

### OCR accuracy issues
- Use high-quality images with clear text
- Ensure good contrast between text and background
- For better results, preprocess images (enhance contrast, remove noise)

## Limitations

- Requires clear, readable text in images
- OCR accuracy depends on image quality
- Works best with standard fonts and layouts
- May struggle with handwritten text or complex layouts
- Currently uses text-based analysis only (does not detect image manipulation)

## Future Enhancements

- Image manipulation detection (deepfake, photo editing)
- Better OCR preprocessing
- Support for multiple languages
- Batch image processing
- Image quality scoring

