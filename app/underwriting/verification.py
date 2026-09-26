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

    supporting_values = [
        value
        for value in [
            w2_income,
            paystub_annual_income,
        ]
        if value is not None
    ]

    verified_income = sum(supporting_values) / len(supporting_values)

    if application_income is None:
        return VerificationResult(
            check_name="income_verification",
            passed=False,
            description="Loan application income is missing.",
            source_documents=source_documents,
        )

    difference = abs(application_income - verified_income)

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


def verify_required_documents(
    required_documents: list[str],
    available_documents: list[str],
) -> list[VerificationResult]:
    """
    Check whether required loan documents are present.
    """

    results = []

    available_set = set(available_documents)

    document_rules = {
        "w2.pdf": (
            "document_w2",
            "Required W-2 document is missing.",
        ),
        "bank_statement_02.pdf": (
            "document_bank_statement",
            "Required bank statement is missing.",
        ),
        "tax_return.pdf": (
            "document_tax_return",
            "Required tax return is missing.",
        ),
        "pay_stub_02.pdf": (
            "document_pay_stub",
            "Required pay stub is missing.",
        ),
        "appraisal.pdf": (
            "document_appraisal",
            "Required appraisal is missing.",
        ),
    }

    for document_name in required_documents:

        if document_name not in document_rules:
            continue

        check_name, description = document_rules[document_name]

        if document_name in available_set:
            results.append(
                VerificationResult(
                    check_name=check_name,
                    passed=True,
                    description=(
                        f"Required document '{document_name}' "
                        "is present."
                    ),
                    source_documents=[document_name],
                )
            )
        else:
            results.append(
                VerificationResult(
                    check_name=check_name,
                    passed=False,
                    description=description,
                    source_documents=[],
                )
            )

    return results


def verify_unexplained_deposit(
    cash_deposits: list[tuple[str, float]],
) -> VerificationResult:
    """
    Detect large cash deposits that require sourcing.
    """

    source_documents = [
        document_name
        for document_name, _ in cash_deposits
    ]

    large_deposits = [
        (document_name, amount)
        for document_name, amount in cash_deposits
        if amount >= 10000
    ]

    if not large_deposits:
        return VerificationResult(
            check_name="deposit_verification",
            passed=True,
            description="No large unexplained deposits were identified.",
            source_documents=source_documents,
        )

    descriptions = []

    for document_name, amount in large_deposits:
        descriptions.append(
            f"${amount:,.2f} cash deposit in {document_name}"
        )

    return VerificationResult(
        check_name="deposit_verification",
        passed=False,
        description=(
            "Large unexplained deposit requires sourcing: "
            + ", ".join(descriptions)
        ),
        source_documents=source_documents,
    )


def verify_employment_gap(
    employment_start: str | None,
    previous_employment_end: str | None,
) -> VerificationResult:
    """
    Detect a gap between previous employment and current employment.
    """

    if not employment_start or not previous_employment_end:
        return VerificationResult(
            check_name="employment_gap",
            passed=True,
            description="No documented employment gap was identified.",
            source_documents=[],
        )

    return VerificationResult(
        check_name="employment_gap",
        passed=False,
        description=(
            f"Employment history contains a gap between "
            f"{previous_employment_end} and {employment_start}."
        ),
        source_documents=[
            "loan_application.pdf",
            "employment_history.pdf",
        ],
    )


def verify_property_value(
    application_value: float | None,
    appraised_value: float | None,
) -> VerificationResult:
    """
    Compare the property value on the application
    against the appraisal.
    """

    if application_value is None or appraised_value is None:
        return VerificationResult(
            check_name="property_value_verification",
            passed=False,
            description="Insufficient property value documentation.",
            source_documents=[
                "loan_application.pdf",
                "appraisal.pdf",
            ],
        )

    difference = abs(
        application_value - appraised_value
    )

    tolerance = 100.0

    if difference <= tolerance:
        return VerificationResult(
            check_name="property_value_verification",
            passed=True,
            description=(
                f"Application property value "
                f"(${application_value:,.2f}) "
                f"is consistent with the appraised value "
                f"(${appraised_value:,.2f})."
            ),
            source_documents=[
                "loan_application.pdf",
                "appraisal.pdf",
            ],
        )

    return VerificationResult(
        check_name="property_value_verification",
        passed=False,
        description=(
            f"Application property value "
            f"(${application_value:,.2f}) "
            f"differs from the appraised value "
            f"(${appraised_value:,.2f}) "
            f"by ${difference:,.2f}."
        ),
        source_documents=[
            "loan_application.pdf",
            "appraisal.pdf",
        ],
    )