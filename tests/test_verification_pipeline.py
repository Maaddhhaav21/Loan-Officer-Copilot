from app.underwriting.pipeline import run_verification


def test_clean_loan_verification():
    results, dti = run_verification(
        application_income=96000,
        w2_income=96000,
        paystub_annual_income=96000,
        declared_assets=87500,
        verified_assets=87500,
        application_employer="Acme Technologies Inc.",
        supporting_employers=[
            "Acme Technologies Inc.",
            "Acme Technologies Inc.",
        ],
        monthly_income=8000,
        monthly_debt=3200,
    )

    assert len(results) == 3

    assert results[0].check_name == "income_verification"
    assert results[0].passed is True

    assert results[1].check_name == "asset_verification"
    assert results[1].passed is True

    assert results[2].check_name == "employment_verification"
    assert results[2].passed is True

    assert dti.dti_percentage == 40.0
    assert dti.passed is True


def test_problem_loan_verification():
    results, dti = run_verification(
        application_income=120000,
        w2_income=96000,
        paystub_annual_income=96000,
        declared_assets=125000,
        verified_assets=87500,
        application_employer="Acme Software LLC",
        supporting_employers=[
            "Acme Technologies Inc.",
            "Acme Technologies Inc.",
        ],
        monthly_income=8000,
        monthly_debt=4000,
    )

    assert len(results) == 3

    # Income discrepancy
    assert results[0].passed is False

    # Asset discrepancy
    assert results[1].passed is False

    # Employer discrepancy
    assert results[2].passed is False

    # High DTI
    assert dti.dti_percentage == 50.0
    assert dti.passed is False