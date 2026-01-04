import pytesseract
from PIL import Image
import os
import sys

def perform_ocr(image_path):
    """
    Perform OCR on the given image path.
    Returns extracted text or empty string if failed.
    """
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            return ""
            
        # Configuration for Windows: Try to find tesseract executable
        if os.name == 'nt':
            # Check common installation paths
            possible_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                os.path.join(os.environ.get('LOCALAPPDATA', ''), r'Tesseract-OCR\tesseract.exe')
            ]
            
            # If tesseract is not in PATH (shutil.which returns None), try explicit paths
            import shutil
            if not shutil.which('tesseract'):
                for path in possible_paths:
                    if os.path.exists(path):
                        pytesseract.pytesseract.tesseract_cmd = path
                        break
        
        # Open image
        img = Image.open(image_path)
        
        # Perform OCR
        text = pytesseract.image_to_string(img)
        return text.strip()
    except ImportError:
        print("pytesseract or PIL not installed.")
        return ""
    except pytesseract.TesseractNotFoundError:
        # Tesseract is not installed or not in PATH
        # We can try a common location or just fail gracefully
        print("Tesseract not found. Please install Tesseract-OCR.")
        return ""
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""
