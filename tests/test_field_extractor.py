from app.document_processing.ingestion import ingest_document
from app.document_processing.document_classifier import classify_document
from app.document_processing.field_extractor import extract_fields
from app.schemas.documents import DocumentType


def test_extract_loan_application_fields():

    file_path = "data/synthetic/LOAN-0001/loan_application.pdf"

    text = ingest_document(file_path)

    document_type = classify_document(text)

    result = extract_fields(
        text,
        document_type,
        "loan_application.pdf",
    )

    assert document_type == DocumentType.LOAN_APPLICATION

    values = {
        field.field_name: field.value
        for field in result.fields
    }

    assert values["borrower_name"] == "John Carter"
    assert values["annual_income"] == 96000
    assert values["loan_amount"] == 420000
    assert values["property_value"] == 500000


def test_extract_w2_fields():

    file_path = "data/synthetic/LOAN-0001/w2.pdf"

    text = ingest_document(file_path)

    document_type = classify_document(text)

    result = extract_fields(
        text,
        document_type,
        "w2.pdf",
    )

    values = {
        field.field_name: field.value
        for field in result.fields
    }

    assert values["w2_wages"] == 96000


def test_extract_appraisal():

    file_path = "data/synthetic/LOAN-0001/appraisal.pdf"

    text = ingest_document(file_path)

    document_type = classify_document(text)

    result = extract_fields(
        text,
        document_type,
        "appraisal.pdf",
    )

    values = {
        field.field_name: field.value
        for field in result.fields
    }

    assert values["appraised_value"] == 500000