from enum import Enum

from pydantic import BaseModel

from app.schemas.conditions import UnderwritingCondition


class UnderwritingStatus(str, Enum):
    PASS = "pass"
    REVIEW = "review"
    INCOMPLETE = "incomplete"


class VerificationResult(BaseModel):
    check_name: str
    passed: bool
    description: str
    source_documents: list[str] = []


class DTIResult(BaseModel):
    monthly_income: float
    monthly_debt: float
    dti_percentage: float
    threshold_percentage: float
    passed: bool


class UnderwritingResult(BaseModel):
    loan_id: str
    status: UnderwritingStatus
    dti: DTIResult | None = None
    verification_results: list[VerificationResult] = []
    conditions: list[UnderwritingCondition] = []
    summary: str | None = None