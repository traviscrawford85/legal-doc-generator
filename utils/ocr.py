# utils/ocr.py

import os
import pdfplumber
from pdf2image import convert_from_path
import pytesseract

def is_searchable_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return any(page.extract_text() for page in pdf.pages)

def ocr_pdf_to_text(pdf_path):
    images = convert_from_path(pdf_path)
    return '\n\n'.join(pytesseract.image_to_string(img) for img in images)

def ocr_pdf_if_needed(pdf_path, output_dir=None, force=False):
    """
    Runs OCR if PDF is not searchable. Saves .txt file in output_dir if given.
    Returns a dict with status and optional extracted text.
    """
    if not os.path.exists(pdf_path) or not pdf_path.lower().endswith(".pdf"):
        return {"status": "❌ Invalid file", "text": None}

    basename = os.path.basename(pdf_path).replace(".pdf", ".txt")
    txt_path = os.path.join(output_dir, basename) if output_dir else None

    if not force and txt_path and os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            return {"status": "🟡 Cached", "text": f.read()}

    if is_searchable_pdf(pdf_path) and not force:
        return {"status": "🟢 Searchable", "text": None}

    text = ocr_pdf_to_text(pdf_path)

    if txt_path:
        os.makedirs(os.path.dirname(txt_path), exist_ok=True)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

    return {"status": "🔵 OCR applied", "text": text}
