import pytesseract
from PIL import Image
from io import BytesIO
from typing import List, Dict, Any

def extract_text_from_image(image_path_or_bytes: str | bytes, source_name: str = "image.png") -> List[Dict[str, Any]]:
    """
    Extract text from an image using Tesseract OCR.
    """
    if isinstance(image_path_or_bytes, str):
        image = Image.open(image_path_or_bytes)
        source = image_path_or_bytes
    else:
        image = Image.open(BytesIO(image_path_or_bytes))
        source = source_name
        
    text = pytesseract.image_to_string(image)
    
    if text.strip():
        return [{
            "page_content": text,
            "metadata": {
                "source": source,
                "type": "image"
            }
        }]
    return []

# Example of how you would integrate OCR into pdf_loader if a PDF page has no text
# (Implementation left as an advanced feature)
