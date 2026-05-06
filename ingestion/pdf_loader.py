import os
from typing import List, Dict, Any
import pdfplumber
from PyPDF2 import PdfReader
from io import BytesIO

def extract_text_from_pdf(file_path_or_bytes: str | bytes, use_pdfplumber: bool = True) -> List[Dict[str, Any]]:
    """
    Extract text from a PDF file.
    Returns a list of dictionaries containing text and metadata per page.
    """
    extracted_data = []
    
    if isinstance(file_path_or_bytes, str):
        # File path
        if use_pdfplumber:
            with pdfplumber.open(file_path_or_bytes) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        extracted_data.append({
                            "page_content": text,
                            "metadata": {
                                "source": os.path.basename(file_path_or_bytes),
                                "page": i + 1
                            }
                        })
        else:
            with open(file_path_or_bytes, "rb") as f:
                reader = PdfReader(f)
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text:
                        extracted_data.append({
                            "page_content": text,
                            "metadata": {
                                "source": os.path.basename(file_path_or_bytes),
                                "page": i + 1
                            }
                        })
    else:
        # Bytes (uploaded file)
        file_stream = BytesIO(file_path_or_bytes)
        if use_pdfplumber:
            with pdfplumber.open(file_stream) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        extracted_data.append({
                            "page_content": text,
                            "metadata": {
                                "source": "uploaded_file.pdf",
                                "page": i + 1
                            }
                        })
        else:
            reader = PdfReader(file_stream)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    extracted_data.append({
                        "page_content": text,
                        "metadata": {
                            "source": "uploaded_file.pdf",
                            "page": i + 1
                        }
                    })
                    
    return extracted_data
