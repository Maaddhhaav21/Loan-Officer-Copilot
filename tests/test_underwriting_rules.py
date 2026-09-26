from app.underwriting.rules import (
    create_income_condition,
    create_asset_condition,
    create_employment_condition,
    create_dti_condition,
)
from app.schemas.underwriting import VerificationResult, DTIResult


def test_income_condition_created():

    result = VerificationResult(
        check_name="income_verification",
        passed=False,
        description="Application income differs from supporting income.",
        source_documents=[
            "loan_application.pdf",
            "w2.pdf",
        ],
    )

    condition = create_income_condition(result)

    assert condition is not None
    assert condition.condition_id == "INC-001"
    assert condition.severity.value == "high"
    assert condition.status.value == "open"


def test_income_condition_not_created_when_passed():

    result = VerificationResult(
        check_name="income_verification",
        passed=True,
        description="Income is consistent.",
        source_documents=[
            "loan_application.pdf",
            "w2.pdf",
        ],
    )

    condition = create_income_condition(result)

    assert condition is None


def test_asset_condition_created():

    result = VerificationResult(
        check_name="asset_verification",
        passed=False,
        description="Declared assets differ from verified assets.",
        source_documents=[
            "loan_application.pdf",
            "bank_statement_01.pdf",
        ],
    )

    condition = create_asset_condition(result)

    assert condition is not None
    assert condition.condition_id == "AST-001"
    assert condition.severity.value == "medium"


def test_employment_condition_created():

    result = VerificationResult(
        check_name="employment_verification",
        passed=False,
        description="Employer names do not match.",
        source_documents=[
            "loan_application.pdf",
            "w2.pdf",
        ],
    )

    condition = create_employment_condition(result)

    assert condition is not None
    assert condition.condition_id == "EMP-001"
    assert condition.severity.value == "high"


def test_dti_condition_created():

    dti = DTIResult(
        monthly_income=8000,
        monthly_debt=4000,
        dti_percentage=50.0,
        threshold_percentage=43.0,
        passed=False,
    )

    condition = create_dti_condition(dti)

    assert condition is not None
    assert condition.condition_id == "DTI-001"
    assert condition.severity.value == "high"


def test_dti_condition_not_created_when_passed():

    dti = DTIResult(
        monthly_income=8000,
        monthly_debt=3200,
        dti_percentage=40.0,
        threshold_percentage=43.0,
        passed=True,
    )

    condition = create_dti_condition(dti)

    assert condition is None