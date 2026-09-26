from pathlib import Path

from app.document_processing.ingestion import ingest_document
from app.document_processing.document_classifier import classify_document
from app.document_processing.field_extractor import extract_fields

from app.underwriting.pipeline import run_verification
from app.underwriting.engine import run_underwriting

from app.underwriting.verification import (
    verify_required_documents,
    verify_unexplained_deposit,
    verify_employment_gap,
    verify_property_value,
)


def process_loan(loan_directory: str):

    loan_path = Path(loan_directory)

    loan_id = loan_path.name

    extracted_data = {}

    # ========================================================
    # DOCUMENT INGESTION + CLASSIFICATION + EXTRACTION
    # ========================================================

    for pdf_file in sorted(loan_path.glob("*.pdf")):

        text = ingest_document(
            str(pdf_file)
        )

        document_type = classify_document(
            text
        )

        extraction = extract_fields(
            text=text,
            document_type=document_type,
            document_id=pdf_file.name,
        )

        extracted_data[pdf_file.name] = extraction

    # ========================================================
    # HELPER TO GET EXTRACTED FIELD
    # ========================================================

    def get_field(
        document_name: str,
        field_name: str,
    ):

        extraction = extracted_data.get(
            document_name
        )

        if extraction is None:
            return None

        for field in extraction.fields:

            if field.field_name == field_name:
                return field.value

        return None

    # ========================================================
    # INCOME
    # ========================================================

    application_income = get_field(
        "loan_application.pdf",
        "annual_income",
    )

    application_employer = get_field(
        "loan_application.pdf",
        "employer_name",
    )

    w2_income = get_field(
        "w2.pdf",
        "w2_wages",
    )

    # ========================================================
    # PAY STUB INCOME
    # ========================================================

    paystub_files = [
        name
        for name in extracted_data
        if name.startswith("pay_stub")
    ]

    paystub_values = []

    for file_name in paystub_files:

        gross_pay = get_field(
            file_name,
            "gross_pay",
        )

        if gross_pay is not None:

            paystub_values.append(
                float(gross_pay)
            )

    paystub_income = None

    if paystub_values:

        average_pay = (
            sum(paystub_values)
            / len(paystub_values)
        )

        paystub_income = (
            average_pay * 26
        )

    # ========================================================
    # ASSETS
    # ========================================================

    declared_assets_field = get_field(
        "loan_application.pdf",
        "declared_assets",
    )

    if declared_assets_field is not None:

        declared_assets = float(
            declared_assets_field
        )

    else:

        checking_balance = get_field(
            "loan_application.pdf",
            "checking_balance",
        )

        savings_balance = get_field(
            "loan_application.pdf",
            "savings_balance",
        )

        declared_assets = 0.0

        if checking_balance is not None:

            declared_assets += float(
                checking_balance
            )

        if savings_balance is not None:

            declared_assets += float(
                savings_balance
            )

    # Synthetic verified asset position.
    verified_assets = 87500.0

    # ========================================================
    # EMPLOYMENT
    # ========================================================

    supporting_employers = []

    for file_name in extracted_data:

        if (
            file_name == "w2.pdf"
            or file_name.startswith("pay_stub")
        ):

            employer = get_field(
                file_name,
                "employer_name",
            )

            if employer:

                supporting_employers.append(
                    str(employer)
                )

    # ========================================================
    # VERIFIED INCOME
    # ========================================================

    verified_annual_income = (

        float(w2_income)

        if w2_income is not None

        else (

            float(paystub_income)

            if paystub_income is not None

            else (

                float(application_income)

                if application_income is not None

                else 0
            )
        )
    )

    monthly_income = (
        verified_annual_income / 12
    )

    # ========================================================
    # MONTHLY DEBT
    # ========================================================

    auto_payment = get_field(
        "loan_application.pdf",
        "auto_payment",
    ) or 0

    student_payment = get_field(
        "loan_application.pdf",
        "student_payment",
    ) or 0

    credit_card_payment = get_field(
        "loan_application.pdf",
        "credit_card_payment",
    ) or 0

    monthly_debt = (
        float(auto_payment)
        + float(student_payment)
        + float(credit_card_payment)
    )

    # ========================================================
    # CORE VERIFICATION + DTI
    # ========================================================

    (
        verification_results,
        dti,
    ) = run_verification(

        application_income=application_income,

        w2_income=w2_income,

        paystub_annual_income=paystub_income,

        declared_assets=declared_assets,

        verified_assets=verified_assets,

        application_employer=application_employer,

        supporting_employers=supporting_employers,

        monthly_income=monthly_income,

        monthly_debt=monthly_debt,
    )

    # ========================================================
    # REQUIRED DOCUMENT VERIFICATION
    # ========================================================

    available_documents = list(
        extracted_data.keys()
    )

    required_documents = [
        "w2.pdf",
        "bank_statement_02.pdf",
        "tax_return.pdf",
        "pay_stub_02.pdf",
        "appraisal.pdf",
    ]

    document_results = (
        verify_required_documents(
            required_documents=required_documents,
            available_documents=available_documents,
        )
    )

    verification_results.extend(
        document_results
    )

    # ========================================================
    # UNEXPLAINED DEPOSIT
    # ========================================================

    cash_deposits = []

    for file_name in extracted_data:

        cash_deposit = get_field(
            file_name,
            "cash_deposit",
        )

        if cash_deposit is not None:

            cash_deposits.append(
                (
                    file_name,
                    float(cash_deposit),
                )
            )

    deposit_result = (
        verify_unexplained_deposit(
            cash_deposits
        )
    )

    verification_results.append(
        deposit_result
    )

    # ========================================================
    # PROPERTY VALUE VERIFICATION
    # ========================================================

    application_property_value = get_field(
        "loan_application.pdf",
        "property_value",
    )

    appraised_value = get_field(
        "appraisal.pdf",
        "appraised_value",
    )

    if (
        application_property_value is not None
        and appraised_value is not None
    ):

        property_result = (
            verify_property_value(

                application_value=float(
                    application_property_value
                ),

                appraised_value=float(
                    appraised_value
                ),
            )
        )

        verification_results.append(
            property_result
        )

    # ========================================================
    # EMPLOYMENT GAP VERIFICATION
    # ========================================================

    employment_start = get_field(
        "loan_application.pdf",
        "employment_start",
    )

    previous_employment_end = get_field(
        "loan_application.pdf",
        "previous_employment_end",
    )

    if previous_employment_end is not None:

        employment_gap_result = (
            verify_employment_gap(

                employment_start=employment_start,

                previous_employment_end=(
                    previous_employment_end
                ),
            )
        )

        verification_results.append(
            employment_gap_result
        )

    # ========================================================
    # UNDERWRITING ENGINE
    # ========================================================

    underwriting_result = run_underwriting(

        loan_id=loan_id,

        verification_results=verification_results,

        dti=dti,
    )

    return underwriting_result