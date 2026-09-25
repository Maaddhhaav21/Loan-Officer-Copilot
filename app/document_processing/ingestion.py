from app.document_processing.pdf_parser import extract_text_from_pdf
from app.document_processing.ocr import extract_text_with_ocr


def ingest_document(file_path: str) -> str:
    """
    Extract text from a PDF.

    Uses normal PDF extraction first.
    Falls back to OCR if no text layer is found.
    """

    text = extract_text_from_pdf(file_path)

    if text.strip():
        return text

    return extract_text_with_ocr(file_path)