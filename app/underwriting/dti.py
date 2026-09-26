from app.schemas.underwriting import DTIResult


def calculate_dti(
    monthly_income: float,
    monthly_debt: float,
    threshold_percentage: float = 43.0,
) -> DTIResult:
    """
    Calculate debt-to-income ratio.

    DTI = (monthly debt / monthly gross income) * 100
    """

    if monthly_income <= 0:
        raise ValueError("Monthly income must be greater than zero.")

    dti_percentage = (
        monthly_debt / monthly_income
    ) * 100

    return DTIResult(
        monthly_income=monthly_income,
        monthly_debt=monthly_debt,
        dti_percentage=round(dti_percentage, 2),
        threshold_percentage=threshold_percentage,
        passed=dti_percentage <= threshold_percentage,
    )