from app.schemas.conditions import (
    UnderwritingCondition,
    Severity,
)
from app.schemas.underwriting import (
    VerificationResult,
    DTIResult,
)


def create_income_condition(
    result: VerificationResult,
) -> UnderwritingCondition | None:

    if result.passed:
        return None

    return UnderwritingCondition(
        condition_id="INC-001",
        title="Income verification discrepancy",
        description=result.description,
        severity=Severity.HIGH,
        source_documents=result.source_documents,
        rule_id="INC-001",
    )


def create_asset_condition(
    result: VerificationResult,
) -> UnderwritingCondition | None:

    if result.passed:
        return None

    return UnderwritingCondition(
        condition_id="AST-001",
        title="Asset verification discrepancy",
        description=result.description,
        severity=Severity.MEDIUM,
        source_documents=result.source_documents,
        rule_id="AST-001",
    )


def create_employment_condition(
    result: VerificationResult,
) -> UnderwritingCondition | None:

    if result.passed:
        return None

    return UnderwritingCondition(
        condition_id="EMP-001",
        title="Employment verification discrepancy",
        description=result.description,
        severity=Severity.HIGH,
        source_documents=result.source_documents,
        rule_id="EMP-001",
    )


def create_dti_condition(
    dti: DTIResult,
) -> UnderwritingCondition | None:

    if dti.passed:
        return None

    return UnderwritingCondition(
        condition_id="DTI-001",
        title="Debt-to-income ratio exceeds threshold",
        description=(
            f"DTI of {dti.dti_percentage:.2f}% "
            f"exceeds the allowed threshold of "
            f"{dti.threshold_percentage:.2f}%."
        ),
        severity=Severity.HIGH,
        source_documents=[],
        rule_id="DTI-001",
    )