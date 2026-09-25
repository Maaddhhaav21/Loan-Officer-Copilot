from app.schemas.documents import DocumentType


def classify_document(text: str) -> DocumentType:
    """
    Classify a document based on extracted text.
    """

    text_lower = text.lower()

    if "w-2" in text_lower or "wage and tax statement" in text_lower:
        return DocumentType.W2

    if (
        "bank statement" in text_lower
        or "account summary" in text_lower
        or "beginning balance" in text_lower
    ):
        return DocumentType.BANK_STATEMENT

    if (
        "earnings statement" in text_lower
        or "gross pay" in text_lower
        or "net pay" in text_lower
    ):
        return DocumentType.PAY_STUB

    if (
        "tax return" in text_lower
        or "adjusted gross income" in text_lower
    ):
        return DocumentType.TAX_RETURN

    if (
        "appraisal report" in text_lower
        or "appraised value" in text_lower
        or "comparable sales" in text_lower
    ):
        return DocumentType.APPRAISAL

    if (
        "loan application" in text_lower
        or "borrower information" in text_lower
        or "requested loan" in text_lower
    ):
        return DocumentType.LOAN_APPLICATION

    return DocumentType.UNKNOWN