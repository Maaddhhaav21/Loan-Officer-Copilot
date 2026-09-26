from app.schemas.underwriting import (
    UnderwritingResult,
    UnderwritingStatus,
    VerificationResult,
    DTIResult,
)
from app.schemas.conditions import UnderwritingCondition

from app.underwriting.rules import (
    create_income_condition,
    create_asset_condition,
    create_employment_condition,
    create_document_condition,
    create_deposit_condition,
    create_employment_gap_condition,
    create_property_condition,
    create_dti_condition,
)


def run_underwriting(
    loan_id: str,
    verification_results: list[VerificationResult],
    dti: DTIResult,
) -> UnderwritingResult:

    conditions: list[UnderwritingCondition] = []

    document_condition_map = {
        "document_w2": (
            "DOC-001",
            "Missing W-2",
        ),
        "document_bank_statement": (
            "DOC-002",
            "Missing bank statement",
        ),
        "document_tax_return": (
            "DOC-003",
            "Missing tax return",
        ),
        "document_pay_stub": (
            "DOC-004",
            "Missing pay stub",
        ),
        "document_appraisal": (
            "DOC-005",
            "Missing appraisal",
        ),
    }

    for result in verification_results:

        condition = None

        if result.check_name == "income_verification":
            condition = create_income_condition(result)

        elif result.check_name == "asset_verification":
            condition = create_asset_condition(result)

        elif result.check_name == "employment_verification":
            condition = create_employment_condition(result)

        elif result.check_name in document_condition_map:
            condition_id, title = document_condition_map[
                result.check_name
            ]

            condition = create_document_condition(
                result,
                condition_id,
                title,
            )

        elif result.check_name == "deposit_verification":
            condition = create_deposit_condition(result)

        elif result.check_name == "employment_gap":
            condition = create_employment_gap_condition(result)

        elif result.check_name == "property_value_verification":
            condition = create_property_condition(result)

        if condition is not None:
            conditions.append(condition)

    dti_condition = create_dti_condition(dti)

    if dti_condition is not None:
        conditions.append(dti_condition)

    if conditions:
        status = UnderwritingStatus.REVIEW
    else:
        status = UnderwritingStatus.PASS

    return UnderwritingResult(
        loan_id=loan_id,
        status=status,
        dti=dti,
        verification_results=verification_results,
        conditions=conditions,
    )