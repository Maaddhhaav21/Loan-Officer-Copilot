from app.document_processing.pdf_parser import extract_text_from_pdf
from app.document_processing.ingestion import ingest_document


def test_scanned_pdf_uses_ocr():

    file_path = "data/synthetic/LOAN-0001/scanned_loan_application.pdf"

    # The scanned PDF should have no usable text layer.
    direct_text = extract_text_from_pdf(file_path)

    assert direct_text == ""

    # Ingestion should automatically fall back to OCR.
    text = ingest_document(file_path)

    assert text
    assert "John Carter" in text