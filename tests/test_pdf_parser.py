from app.document_processing.pdf_parser import extract_text_from_pdf


def test_extract_text_from_pdf():

    file_path = "data/synthetic/LOAN-0001/loan_application.pdf"

    text = extract_text_from_pdf(file_path)

    assert text
    assert "John Carter" in text
    assert "Acme Technologies Inc." in text
    assert "Software Engineer" in text