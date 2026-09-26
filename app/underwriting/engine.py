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
    create_dti_condition,
)


def run_underwriting(
    loan_id: str,
    verification_results: list[VerificationResult],
    dti: DTIResult,
) -> UnderwritingResult:

    conditions: list[UnderwritingCondition] = []

    for result in verification_results:

        if result.check_name == "income_verification":
            condition = create_income_condition(result)

        elif result.check_name == "asset_verification":
            condition = create_asset_condition(result)

        elif result.check_name == "employment_verification":
            condition = create_employment_condition(result)

        else:
            condition = None

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