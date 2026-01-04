from PIL import Image
import os
import sys

def perform_ocr(image_path):
    """
    Perform OCR on the given image path.
    Returns extracted text or empty string if failed.
    """
    try:
        import pytesseract
    except ImportError:
        print("OCR Error: pytesseract library is not installed.")
        return ""

    try:
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"OCR Error: File not found at {image_path}")
            return ""
            
        # Configuration for Windows: Try to find tesseract executable
        if os.name == 'nt':
            import shutil
            # If tesseract is not in PATH, try explicit paths
            if not shutil.which('tesseract'):
                possible_paths = [
                    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                    os.path.join(os.environ.get('LOCALAPPDATA', ''), r'Tesseract-OCR\tesseract.exe'),
                    os.path.join(os.environ.get('ProgramFiles', 'C:\Program Files'), r'Tesseract-OCR\tesseract.exe'),
                ]
                
                found = False
                for path in possible_paths:
                    if os.path.exists(path):
                        pytesseract.pytesseract.tesseract_cmd = path
                        found = True
                        break
                
                if not found:
                    print("OCR Warning: Tesseract executable not found in common Windows paths.")
        
        # Open image
        img = Image.open(image_path)
        
        # Perform OCR
        text = pytesseract.image_to_string(img)
        return text.strip()
    except ImportError:
        print("OCR Error: pytesseract or PIL not installed.")
        return ""
    except pytesseract.TesseractNotFoundError:
        print("OCR Error: Tesseract not found. Please install Tesseract-OCR and add to PATH or install in C:\Program Files\Tesseract-OCR.")
        return ""
    except Exception as e:
        print(f"OCR Exception: {type(e).__name__}: {e}")
        return ""
