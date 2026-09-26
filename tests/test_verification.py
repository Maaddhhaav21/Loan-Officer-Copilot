from app.underwriting.verification import verify_income
from app.underwriting.verification import verify_assets
from app.underwriting.verification import verify_employment

def test_income_verification_passes():

    result = verify_income(
        application_income=96000,
        w2_income=96000,
        paystub_annual_income=96000,
    )

    assert result.passed is True
    assert result.check_name == "income_verification"


def test_income_verification_fails():

    result = verify_income(
        application_income=120000,
        w2_income=96000,
        paystub_annual_income=96000,
    )

    assert result.passed is False
    assert result.check_name == "income_verification"
    assert "120,000.00" in result.description
    assert "96,000.00" in result.description


def test_income_verification_missing_documents():

    result = verify_income(
        application_income=96000,
        w2_income=None,
        paystub_annual_income=None,
    )

    assert result.passed is False
    assert "Insufficient" in result.description

def test_asset_verification_passes():

    result = verify_assets(
        declared_assets=87500,
        verified_assets=87500,
        source_documents=[
            "loan_application.pdf",
            "bank_statement_01.pdf",
        ],
    )

    assert result.passed is True
    assert result.check_name == "asset_verification"


def test_asset_verification_fails():

    result = verify_assets(
        declared_assets=125000,
        verified_assets=87500,
        source_documents=[
            "loan_application.pdf",
            "bank_statement_01.pdf",
        ],
    )

    assert result.passed is False
    assert result.check_name == "asset_verification"
    assert "125,000.00" in result.description
    assert "87,500.00" in result.description


def test_asset_verification_missing_data():

    result = verify_assets(
        declared_assets=125000,
        verified_assets=None,
    )

    assert result.passed is False
    assert "Insufficient" in result.description

def test_employment_verification_passes():

    result = verify_employment(
        application_employer="Acme Technologies Inc.",
        supporting_employers=[
            "Acme Technologies Inc.",
            "Acme Technologies Inc.",
        ],
        source_documents=[
            "loan_application.pdf",
            "pay_stub_01.pdf",
            "w2.pdf",
        ],
    )

    assert result.passed is True
    assert result.check_name == "employment_verification"


def test_employment_verification_fails():

    result = verify_employment(
        application_employer="Acme Software LLC",
        supporting_employers=[
            "Acme Technologies Inc.",
            "Acme Technologies Inc.",
        ],
        source_documents=[
            "loan_application.pdf",
            "pay_stub_01.pdf",
            "w2.pdf",
        ],
    )

    assert result.passed is False
    assert result.check_name == "employment_verification"
    assert "Acme Software LLC" in result.description


def test_employment_verification_missing_data():

    result = verify_employment(
        application_employer=None,
        supporting_employers=[],
    )

    assert result.passed is False
    assert "Insufficient" in result.description