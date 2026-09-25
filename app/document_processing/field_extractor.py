import re

from app.schemas.documents import DocumentType, DocumentExtraction, ExtractedField


def extract_money(text: str, label: str) -> float | None:

    pattern = rf"{re.escape(label)}\s*\$?\s*([\d,]+(?:\.\d{{1,2}})?)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE,
    )

    if not match:
        return None

    return float(
        match.group(1).replace(",", "")
    )


def extract_text_value(text: str, label: str) -> str | None:

    pattern = rf"{re.escape(label)}\s*(.+)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE,
    )

    if not match:
        return None

    return match.group(1).strip()


def add_field(
    fields,
    name,
    value,
    confidence,
    document_id,
):

    if value is not None:

        fields.append(
            ExtractedField(
                field_name=name,
                value=value,
                confidence=confidence,
                source_document=document_id,
            )
        )


def extract_fields(
    text: str,
    document_type: DocumentType,
    document_id: str = "unknown",
) -> DocumentExtraction:

    fields = []

    # ========================================================
    # LOAN APPLICATION
    # ========================================================

    if document_type == DocumentType.LOAN_APPLICATION:

        add_field(
            fields,
            "borrower_name",
            extract_text_value(
                text,
                "Borrower Name:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "date_of_birth",
            extract_text_value(
                text,
                "Date of Birth:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "employer_name",
            extract_text_value(
                text,
                "Employer:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "job_title",
            extract_text_value(
                text,
                "Job Title:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "employment_start",
            extract_text_value(
                text,
                "Employment Start:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "annual_income",
            extract_money(
                text,
                "Annual Income:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "loan_amount",
            extract_money(
                text,
                "Requested Loan:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "property_value",
            extract_money(
                text,
                "Property Value:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "property_address",
            extract_text_value(
                text,
                "Property Address:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "property_type",
            extract_text_value(
                text,
                "Property Type:",
            ),
            0.95,
            document_id,
        )

        # Assets

        add_field(
            fields,
            "checking_balance",
            extract_money(
                text,
                "Checking:",
            ),
            0.90,
            document_id,
        )

        add_field(
            fields,
            "savings_balance",
            extract_money(
                text,
                "Savings:",
            ),
            0.90,
            document_id,
        )

        # Liabilities

        add_field(
            fields,
            "auto_payment",
            extract_money(
                text,
                "Auto:",
            ),
            0.90,
            document_id,
        )

        add_field(
            fields,
            "student_payment",
            extract_money(
                text,
                "Student:",
            ),
            0.90,
            document_id,
        )

        add_field(
            fields,
            "credit_card_payment",
            extract_money(
                text,
                "Credit_Cards:",
            ),
            0.90,
            document_id,
        )

    # ========================================================
    # PAY STUB
    # ========================================================

    elif document_type == DocumentType.PAY_STUB:

        add_field(
            fields,
            "employee_name",
            extract_text_value(
                text,
                "Employee:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "employer_name",
            extract_text_value(
                text,
                "Employer:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "job_title",
            extract_text_value(
                text,
                "Job Title:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "gross_pay",
            extract_money(
                text,
                "Gross Pay",
            ),
            0.90,
            document_id,
        )

        add_field(
            fields,
            "net_pay",
            extract_money(
                text,
                "Net Pay",
            ),
            0.90,
            document_id,
        )

    # ========================================================
    # W2
    # ========================================================

    elif document_type == DocumentType.W2:

        add_field(
            fields,
            "employee_name",
            extract_text_value(
                text,
                "Employee:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "employer_name",
            extract_text_value(
                text,
                "Employer:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "w2_wages",
            extract_money(
                text,
                "Wages, tips, other compensation",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "federal_tax_withheld",
            extract_money(
                text,
                "Federal income tax withheld",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "social_security_wages",
            extract_money(
                text,
                "Social Security wages",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "medicare_wages",
            extract_money(
                text,
                "Medicare wages and tips",
            ),
            0.95,
            document_id,
        )

    # ========================================================
    # BANK STATEMENT
    # ========================================================

    elif document_type == DocumentType.BANK_STATEMENT:

        add_field(
            fields,
            "account_holder",
            extract_text_value(
                text,
                "Account Holder:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "account_number",
            extract_text_value(
                text,
                "Account:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "beginning_balance",
            extract_money(
                text,
                "Beginning Balance:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "ending_balance",
            extract_money(
                text,
                "Ending Balance:",
            ),
            0.95,
            document_id,
        )

        # Look for unexplained cash deposit

        cash_deposit = re.search(
            r"CASH DEPOSIT\s+\+?\$?([\d,]+(?:\.\d{1,2})?)",
            text,
            re.IGNORECASE,
        )

        if cash_deposit:

            amount = float(
                cash_deposit.group(1).replace(",", "")
            )

            add_field(
                fields,
                "cash_deposit",
                amount,
                0.90,
                document_id,
            )

    # ========================================================
    # TAX RETURN
    # ========================================================

    elif document_type == DocumentType.TAX_RETURN:

        add_field(
            fields,
            "taxpayer",
            extract_text_value(
                text,
                "Taxpayer:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "tax_year",
            extract_text_value(
                text,
                "Tax Year:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "wages",
            extract_money(
                text,
                "Wages:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "adjusted_gross_income",
            extract_money(
                text,
                "Adjusted Gross Income:",
            ),
            0.95,
            document_id,
        )

    # ========================================================
    # APPRAISAL
    # ========================================================

    elif document_type == DocumentType.APPRAISAL:

        add_field(
            fields,
            "property_address",
            extract_text_value(
                text,
                "Property Address:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "property_type",
            extract_text_value(
                text,
                "Property Type:",
            ),
            0.95,
            document_id,
        )

        add_field(
            fields,
            "appraised_value",
            extract_money(
                text,
                "Appraised Value:",
            ),
            0.95,
            document_id,
        )

    return DocumentExtraction(
        document_id=document_id,
        document_type=document_type,
        fields=fields,
    )