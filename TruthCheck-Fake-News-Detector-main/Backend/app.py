from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from PIL import Image
import io
import os
from werkzeug.utils import secure_filename
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Try to import OCR libraries (optional)
try:
    import pytesseract
    OCR_AVAILABLE = True
    
    # Configure Tesseract path for Windows
    import platform
    if platform.system() == 'Windows':
        # Common Tesseract installation paths on Windows
        possible_paths = [
            r'C:\Users\Dell\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            r'C:\Users\Dell\Tesseract-OCR\tesseract.exe'.format(os.getenv('USERNAME', '')),
        ]
        
        # Try to find Tesseract executable
        tesseract_found = False
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                tesseract_found = True
                print(f"✓ Tesseract found at: {path}")
                break
        
        # If not found in common paths, try to use it from PATH
        if not tesseract_found:
            try:
                # Test if tesseract is in PATH
                import subprocess
                result = subprocess.run(['tesseract', '--version'], 
                                      capture_output=True, 
                                      timeout=2)
                if result.returncode == 0:
                    print("✓ Tesseract found in system PATH")
                    tesseract_found = True
            except:
                pass
        
        # If still not found, print warning
        if not tesseract_found:
            print("⚠️ Warning: Tesseract executable not found automatically.")
            print("   Please set the path manually by adding this to app.py:")
            print("   pytesseract.pytesseract.tesseract_cmd = r'C:\\Path\\To\\Tesseract-OCR\\tesseract.exe'")
            print("   Or add Tesseract to your system PATH environment variable.")
    
except ImportError:
    OCR_AVAILABLE = False
    print("Warning: pytesseract not available. Image analysis will be limited.")

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("Warning: opencv-python not available. Some image processing features may be limited.")

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Image upload configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB max file size

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_image(image_file):
    """Extract text from image using OCR"""
    if not OCR_AVAILABLE:
        raise Exception("OCR not available. Please install pytesseract and Tesseract OCR.")
    
    try:
        # Read image from file
        image = Image.open(io.BytesIO(image_file.read()))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Use pytesseract to extract text
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text.strip()
    except pytesseract.TesseractNotFoundError:
        error_msg = (
            "Tesseract OCR not found. Please:\n"
            "1. Install Tesseract OCR from https://github.com/UB-Mannheim/tesseract/wiki\n"
            "2. Add it to your PATH, OR\n"
            "3. Set the path in app.py: pytesseract.pytesseract.tesseract_cmd = r'C:\\Path\\To\\tesseract.exe'"
        )
        print(f"OCR Error: {error_msg}")
        raise Exception(error_msg)
    except Exception as e:
        error_msg = f"Failed to extract text from image: {str(e)}"
        print(f"OCR Error: {error_msg}")
        raise Exception(error_msg)

def analyze_image_metadata(image_file):
    """Analyze basic image metadata"""
    try:
        image_file.seek(0)  # Reset file pointer
        image = Image.open(io.BytesIO(image_file.read()))
        
        metadata = {
            "format": image.format,
            "size": image.size,  # (width, height)
            "mode": image.mode,
            "has_exif": hasattr(image, '_getexif') and image._getexif() is not None
        }
        
        # Get file size
        image_file.seek(0, os.SEEK_END)
        file_size = image_file.tell()
        image_file.seek(0)
        metadata["file_size_kb"] = round(file_size / 1024, 2)
        
        return metadata
    except Exception as e:
        print(f"Image analysis error: {e}")
        return None

# Load the trained model
try:
    with open('finalized_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Load the fitted vectorizer
vectorizer = None

def load_vectorizer():
    """Load the pre-fitted TF-IDF vectorizer"""
    global vectorizer
    try:
        with open('tfidf_vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        print("Vectorizer loaded successfully!")
    except FileNotFoundError:
        print("Warning: tfidf_vectorizer.pkl not found. Attempting to initialize from data...")
        # Fallback: initialize from training data if pickle file not found
        try:
            df = pd.read_csv("news.csv")
            vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
            vectorizer.fit(df["text"])
            print("Vectorizer initialized from training data!")
        except Exception as e:
            print(f"Error initializing vectorizer from data: {e}")
            vectorizer = None
    except Exception as e:
        print(f"Error loading vectorizer: {e}")
        vectorizer = None

# Load vectorizer on startup
load_vectorizer()

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "message": "Fake News Detection API is active",
        "model_loaded": model is not None,
        "vectorizer_loaded": vectorizer is not None,
        "image_support": OCR_AVAILABLE,
        "endpoints": {
            "text_analysis": "/api/predict",
            "batch_analysis": "/api/batch-predict",
            "image_analysis": "/api/predict-image",
            "model_info": "/api/model-info"
        }
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict if news is fake or real"""
    try:
        # Check if model and vectorizer are loaded
        if model is None or vectorizer is None:
            return jsonify({
                "error": "Model or vectorizer not loaded properly"
            }), 500
        
        # Get data from request
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                "error": "No text provided. Please send JSON with 'text' field"
            }), 400
        
        news_text = data['text']
        title = data.get('title', '')
        
        # Combine title and text for better prediction
        combined_text = f"{title} {news_text}"
        
        # Transform text using vectorizer
        text_vectorized = vectorizer.transform([combined_text])
        
        # Make prediction
        prediction = model.predict(text_vectorized)[0]
        
        # Prepare response
        response = {
            "prediction": prediction,
            "is_fake": prediction == "FAKE",
            "message": "Prediction completed successfully"
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Prediction failed: {str(e)}"
        }), 500

@app.route('/api/batch-predict', methods=['POST'])
def batch_predict():
    """Predict multiple news articles at once"""
    try:
        if model is None or vectorizer is None:
            return jsonify({
                "error": "Model or vectorizer not loaded properly"
            }), 500
        
        data = request.get_json()
        
        if not data or 'articles' not in data:
            return jsonify({
                "error": "No articles provided. Please send JSON with 'articles' array"
            }), 400
        
        articles = data['articles']
        
        if not isinstance(articles, list) or len(articles) == 0:
            return jsonify({
                "error": "Articles must be a non-empty array"
            }), 400
        
        results = []
        
        for idx, article in enumerate(articles):
            try:
                text = article.get('text', '')
                title = article.get('title', '')
                combined_text = f"{title} {text}"
                
                # Transform and predict
                text_vectorized = vectorizer.transform([combined_text])
                prediction = model.predict(text_vectorized)[0]
                results.append({
                    "index": idx,
                    "prediction": prediction,
                    "is_fake": prediction == "FAKE"
                })
            except Exception as e:
                results.append({
                    "index": idx,
                    "error": str(e)
                })
        
        return jsonify({
            "results": results,
            "total": len(articles),
            "message": "Batch prediction completed"
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Batch prediction failed: {str(e)}"
        }), 500

@app.route('/api/predict-image', methods=['POST'])
def predict_image():
    """Predict if news in image is fake or real"""
    try:
        # Check if model and vectorizer are loaded
        if model is None or vectorizer is None:
            return jsonify({
                "error": "Model or vectorizer not loaded properly"
            }), 500
        
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({
                "error": "No image file provided. Please upload an image file."
            }), 400
        
        image_file = request.files['image']
        
        if image_file.filename == '':
            return jsonify({
                "error": "No image file selected"
            }), 400
        
        if not allowed_file(image_file.filename):
            return jsonify({
                "error": f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400
        
        # Check file size
        image_file.seek(0, os.SEEK_END)
        file_size = image_file.tell()
        image_file.seek(0)
        
        if file_size > MAX_IMAGE_SIZE:
            return jsonify({
                "error": f"File too large. Maximum size: {MAX_IMAGE_SIZE / (1024*1024)}MB"
            }), 400
        
        # Extract text from image using OCR
        extracted_text = extract_text_from_image(image_file)
        
        if not extracted_text or len(extracted_text.strip()) < 10:
            return jsonify({
                "error": "Could not extract sufficient text from image. Please ensure the image contains readable text.",
                "extracted_text_length": len(extracted_text) if extracted_text else 0
            }), 400
        
        # Analyze image metadata
        image_metadata = analyze_image_metadata(image_file)
        
        # Use the existing text model to predict
        text_vectorized = vectorizer.transform([extracted_text])
        prediction = model.predict(text_vectorized)[0]
        
        # Prepare response
        response = {
            "prediction": prediction,
            "is_fake": prediction == "FAKE",
            "extracted_text": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
            "extracted_text_length": len(extracted_text),
            "image_metadata": image_metadata,
            "message": "Image analysis completed successfully"
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Image prediction failed: {str(e)}"
        }), 500

@app.route('/api/check-ocr', methods=['GET'])
def check_ocr():
    """Check if OCR/Tesseract is properly configured"""
    try:
        status = {
            "pytesseract_installed": OCR_AVAILABLE,
            "tesseract_configured": False,
            "tesseract_path": None,
            "tesseract_version": None,
            "error": None
        }
        
        if OCR_AVAILABLE:
            try:
                # Try to get Tesseract version
                import platform
                if platform.system() == 'Windows':
                    status["tesseract_path"] = getattr(pytesseract.pytesseract, 'tesseract_cmd', 'Not set (using PATH)')
                else:
                    status["tesseract_path"] = "Using system PATH"
                
                version = pytesseract.get_tesseract_version()
                status["tesseract_version"] = str(version)
                status["tesseract_configured"] = True
                status["message"] = "Tesseract OCR is properly configured!"
            except pytesseract.TesseractNotFoundError as e:
                status["error"] = str(e)
                status["message"] = "Tesseract executable not found. Please install Tesseract OCR."
            except Exception as e:
                status["error"] = str(e)
                status["message"] = f"Error checking Tesseract: {str(e)}"
        else:
            status["message"] = "pytesseract is not installed. Please install it with: pip install pytesseract"
        
        return jsonify(status), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to check OCR status: {str(e)}"
        }), 500

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get information about the model"""
    try:
        info = {
            "model_type": "PassiveAggressiveClassifier",
            "vectorizer": "TfidfVectorizer",
            "accuracy": "94.79%",
            "training_samples": 6335,
            "max_iterations": 50,
            "features": {
                "stop_words": "english",
                "max_df": 0.7
            },
            "image_support": OCR_AVAILABLE,
            "allowed_image_formats": list(ALLOWED_EXTENSIONS),
            "max_image_size_mb": MAX_IMAGE_SIZE / (1024 * 1024)
        }
        
        if model is not None:
            info["model_params"] = {
                "C": model.C,
                "max_iter": model.max_iter,
                "loss": model.loss
            }
        
        return jsonify(info), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get model info: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Starting Fake News Detection API Server")
    print("="*50)
    print(f"Model loaded: {model is not None}")
    print(f"Vectorizer loaded: {vectorizer is not None}")
    print("="*50 + "\n")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5001)