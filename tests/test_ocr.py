from app.document_processing.ocr import extract_text_with_ocr


def test_ocr():

    file_path = "data/synthetic/LOAN-0001/loan_application.pdf"

    text = extract_text_with_ocr(file_path)

    assert text
    assert "John Carter" in text