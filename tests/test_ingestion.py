from app.document_processing.ingestion import ingest_document


def test_ingest_document():

    file_path = "data/synthetic/LOAN-0001/loan_application.pdf"

    text = ingest_document(file_path)

    assert text
    assert "John Carter" in text