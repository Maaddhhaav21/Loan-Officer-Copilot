from app.underwriting.dti import calculate_dti


def test_dti_passes():

    result = calculate_dti(
        monthly_income=8000,
        monthly_debt=3200,
    )

    assert result.dti_percentage == 40.0
    assert result.passed is True


def test_dti_fails():

    result = calculate_dti(
        monthly_income=8000,
        monthly_debt=4000,
    )

    assert result.dti_percentage == 50.0
    assert result.passed is False


def test_dti_custom_threshold():

    result = calculate_dti(
        monthly_income=10000,
        monthly_debt=4500,
        threshold_percentage=45.0,
    )

    assert result.dti_percentage == 45.0
    assert result.passed is True


def test_dti_invalid_income():

    try:
        calculate_dti(
            monthly_income=0,
            monthly_debt=1000,
        )
        assert False
    except ValueError:
        assert True