from app.underwriting.engine import run_underwriting
from app.schemas.underwriting import (
    VerificationResult,
    DTIResult,
    UnderwritingStatus,
)


def test_clean_loan_passes():

    verification_results = [
        VerificationResult(
            check_name="income_verification",
            passed=True,
            description="Income is consistent.",
        ),
        VerificationResult(
            check_name="asset_verification",
            passed=True,
            description="Assets are consistent.",
        ),
        VerificationResult(
            check_name="employment_verification",
            passed=True,
            description="Employment is consistent.",
        ),
    ]

    dti = DTIResult(
        monthly_income=8000,
        monthly_debt=3200,
        dti_percentage=40.0,
        threshold_percentage=43.0,
        passed=True,
    )

    result = run_underwriting(
        loan_id="LOAN-0001",
        verification_results=verification_results,
        dti=dti,
    )

    assert result.loan_id == "LOAN-0001"
    assert result.status == UnderwritingStatus.PASS
    assert len(result.conditions) == 0


def test_problem_loan_requires_review():

    verification_results = [
        VerificationResult(
            check_name="income_verification",
            passed=False,
            description="Application income differs from supporting income.",
            source_documents=["loan_application.pdf", "w2.pdf"],
        ),
        VerificationResult(
            check_name="asset_verification",
            passed=True,
            description="Assets are consistent.",
        ),
        VerificationResult(
            check_name="employment_verification",
            passed=True,
            description="Employment is consistent.",
        ),
    ]

    dti = DTIResult(
        monthly_income=8000,
        monthly_debt=4000,
        dti_percentage=50.0,
        threshold_percentage=43.0,
        passed=False,
    )

    result = run_underwriting(
        loan_id="LOAN-0002",
        verification_results=verification_results,
        dti=dti,
    )

    assert result.loan_id == "LOAN-0002"
    assert result.status == UnderwritingStatus.REVIEW

    assert len(result.conditions) == 2

    condition_ids = [
        condition.condition_id
        for condition in result.conditions
    ]

    assert "INC-001" in condition_ids
    assert "DTI-001" in condition_ids