from pathlib import Path

from app.document_processing.document_classifier import classify_document
from app.document_processing.ingestion import ingest_document
from app.schemas.documents import DocumentType


def test_classify_loan_application():
    path = "data/synthetic/LOAN-0001/loan_application.pdf"

    text = ingest_document(path)

    assert classify_document(text) == DocumentType.LOAN_APPLICATION


def test_classify_pay_stub():
    path = "data/synthetic/LOAN-0001/pay_stub_01.pdf"

    text = ingest_document(path)

    assert classify_document(text) == DocumentType.PAY_STUB


def test_classify_bank_statement():
    path = "data/synthetic/LOAN-0001/bank_statement_01.pdf"

    text = ingest_document(path)

    assert classify_document(text) == DocumentType.BANK_STATEMENT


def test_classify_w2():
    path = "data/synthetic/LOAN-0001/w2.pdf"

    text = ingest_document(path)

    assert classify_document(text) == DocumentType.W2


def test_classify_tax_return():
    path = "data/synthetic/LOAN-0001/tax_return.pdf"

    text = ingest_document(path)

    assert classify_document(text) == DocumentType.TAX_RETURN


def test_classify_appraisal():
    path = "data/synthetic/LOAN-0001/appraisal.pdf"

    text = ingest_document(path)

    assert classify_document(text) == DocumentType.APPRAISAL