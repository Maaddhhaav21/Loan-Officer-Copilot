from enum import Enum
from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    PAY_STUB = "pay_stub"
    W2 = "w2"
    BANK_STATEMENT = "bank_statement"
    TAX_RETURN = "tax_return"
    APPRAISAL = "appraisal"
    LOAN_APPLICATION = "loan_application"
    UNKNOWN = "unknown"


class Document(BaseModel):
    document_id: str
    file_name: str
    document_type: DocumentType = DocumentType.UNKNOWN
    file_path: str
    page_count: int | None = None
    extracted_text: str | None = None


class ExtractedField(BaseModel):
    field_name: str
    value: str | float | int | None
    confidence: float = Field(ge=0.0, le=1.0)
    source_document: str
    source_page: int | None = None


class DocumentExtraction(BaseModel):
    document_id: str
    document_type: DocumentType
    fields: list[ExtractedField] = []