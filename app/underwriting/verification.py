from app.schemas.underwriting import VerificationResult


def verify_income(
    application_income: float | None,
    w2_income: float | None,
    paystub_annual_income: float | None,
) -> VerificationResult:
    """
    Compare income reported across the loan application,
    W-2, and pay stubs.
    """

    source_documents = []

    if application_income is not None:
        source_documents.append("loan_application.pdf")

    if w2_income is not None:
        source_documents.append("w2.pdf")

    if paystub_annual_income is not None:
        source_documents.append("pay_stub.pdf")

    # We need at least two sources to verify income.
    available_values = [
        value
        for value in [
            application_income,
            w2_income,
            paystub_annual_income,
        ]
        if value is not None
    ]

    if len(available_values) < 2:

        return VerificationResult(
            check_name="income_verification",
            passed=False,
            description="Insufficient income documentation for verification.",
            source_documents=source_documents,
        )

    # Use W-2 and pay stubs as the supporting income sources.
    supporting_values = [
        value
        for value in [
            w2_income,
            paystub_annual_income,
        ]
        if value is not None
    ]

    # Calculate supporting income.
    verified_income = sum(supporting_values) / len(supporting_values)

    # Compare application income with verified income.
    if application_income is None:

        return VerificationResult(
            check_name="income_verification",
            passed=False,
            description="Loan application income is missing.",
            source_documents=source_documents,
        )

    difference = abs(application_income - verified_income)

    # Allow a small tolerance for rounding.
    tolerance = 100.0

    if difference <= tolerance:

        return VerificationResult(
            check_name="income_verification",
            passed=True,
            description=(
                f"Application income (${application_income:,.2f}) "
                f"is consistent with supporting income "
                f"(${verified_income:,.2f})."
            ),
            source_documents=source_documents,
        )

    return VerificationResult(
        check_name="income_verification",
        passed=False,
        description=(
            f"Application income (${application_income:,.2f}) "
            f"differs from supporting income "
            f"(${verified_income:,.2f}) "
            f"by ${difference:,.2f}."
        ),
        source_documents=source_documents,
    )

def verify_assets(
    declared_assets: float | None,
    verified_assets: float | None,
    source_documents: list[str] | None = None,
) -> VerificationResult:
    """
    Compare assets declared on the loan application
    against assets verified from bank statements.
    """

    documents = source_documents or []

    if declared_assets is None or verified_assets is None:

        return VerificationResult(
            check_name="asset_verification",
            passed=False,
            description="Insufficient asset documentation for verification.",
            source_documents=documents,
        )

    difference = abs(
        declared_assets - verified_assets
    )

    # Small tolerance for rounding.
    tolerance = 100.0

    if difference <= tolerance:

        return VerificationResult(
            check_name="asset_verification",
            passed=True,
            description=(
                f"Declared assets (${declared_assets:,.2f}) "
                f"are consistent with verified assets "
                f"(${verified_assets:,.2f})."
            ),
            source_documents=documents,
        )

    return VerificationResult(
        check_name="asset_verification",
        passed=False,
        description=(
            f"Declared assets (${declared_assets:,.2f}) "
            f"differ from verified assets "
            f"(${verified_assets:,.2f}) "
            f"by ${difference:,.2f}."
        ),
        source_documents=documents,
    )

def verify_employment(
    application_employer: str | None,
    supporting_employers: list[str],
    source_documents: list[str] | None = None,
) -> VerificationResult:
    """
    Compare the employer reported on the loan application
    against supporting employment documents.
    """

    documents = source_documents or []

    if not application_employer or not supporting_employers:
        return VerificationResult(
            check_name="employment_verification",
            passed=False,
            description="Insufficient employment documentation for verification.",
            source_documents=documents,
        )

    normalized_application = application_employer.strip().lower()

    normalized_supporting = [
        employer.strip().lower()
        for employer in supporting_employers
        if employer
    ]

    if not normalized_supporting:
        return VerificationResult(
            check_name="employment_verification",
            passed=False,
            description="No supporting employer information was found.",
            source_documents=documents,
        )

    all_match = all(
        employer == normalized_application
        for employer in normalized_supporting
    )

    if all_match:
        return VerificationResult(
            check_name="employment_verification",
            passed=True,
            description=(
                f"Employer '{application_employer}' "
                "is consistent across supporting documents."
            ),
            source_documents=documents,
        )

    return VerificationResult(
        check_name="employment_verification",
        passed=False,
        description=(
            f"Application employer '{application_employer}' "
            f"does not match supporting employers: "
            f"{', '.join(supporting_employers)}."
        ),
        source_documents=documents,
    )
