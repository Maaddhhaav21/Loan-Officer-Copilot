from app.schemas.underwriting import VerificationResult, DTIResult
from app.underwriting.verification import (
    verify_income,
    verify_assets,
    verify_employment,
)
from app.underwriting.dti import calculate_dti


def run_verification(
    application_income: float | None,
    w2_income: float | None,
    paystub_annual_income: float | None,
    declared_assets: float | None,
    verified_assets: float | None,
    application_employer: str | None,
    supporting_employers: list[str],
    monthly_income: float,
    monthly_debt: float,
    dti_threshold: float = 43.0,
) -> tuple[list[VerificationResult], DTIResult]:

    verification_results = []

    # 1. Income verification
    income_result = verify_income(
        application_income=application_income,
        w2_income=w2_income,
        paystub_annual_income=paystub_annual_income,
    )
    verification_results.append(income_result)

    # 2. Asset verification
    asset_result = verify_assets(
        declared_assets=declared_assets,
        verified_assets=verified_assets,
        source_documents=[
            "loan_application.pdf",
            "bank_statement_01.pdf",
            "bank_statement_02.pdf",
        ],
    )
    verification_results.append(asset_result)

    # 3. Employment verification
    employment_result = verify_employment(
        application_employer=application_employer,
        supporting_employers=supporting_employers,
        source_documents=[
            "loan_application.pdf",
            "w2.pdf",
            "pay_stub.pdf",
        ],
    )
    verification_results.append(employment_result)

    # 4. DTI calculation
    dti_result = calculate_dti(
        monthly_income=monthly_income,
        monthly_debt=monthly_debt,
        threshold_percentage=dti_threshold,
    )

    return verification_results, dti_result