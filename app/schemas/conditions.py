from enum import Enum

from pydantic import BaseModel


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ConditionStatus(str, Enum):
    OPEN = "open"
    RESOLVED = "resolved"


class UnderwritingCondition(BaseModel):
    condition_id: str
    title: str
    description: str
    severity: Severity
    status: ConditionStatus = ConditionStatus.OPEN
    source_documents: list[str] = []
    rule_id: str | None = None