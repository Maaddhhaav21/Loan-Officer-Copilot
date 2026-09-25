from pathlib import Path
import shutil
import json
from datetime import date, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from faker import Faker

fake = Faker()

BASE_DIR = Path("data/synthetic")
BASE_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# BASE BORROWER
# ============================================================

BASE_BORROWER = {
    "borrower_name": "John Carter",
    "dob": "1988-05-14",
    "address": "1250 Maple Street, Austin, TX 78701",

    "employer_name": "Acme Technologies Inc.",
    "job_title": "Software Engineer",
    "employment_start": "2021-06-01",

    "annual_income": 96000.0,

    "loan_amount": 420000.0,
    "property_value": 500000.0,

    "debts": {
        "auto": 450.0,
        "student": 350.0,
        "credit_cards": 400.0,
        "other": 0.0,
    },

    "assets": {
        "checking": 25000.0,
        "savings": 62500.0,
    },

    "property_address": "742 Evergreen Avenue, Austin, TX 78704",
    "property_type": "Single Family Residence",
    "appraised_value": 500000.0,
}


# ============================================================
# PDF HELPERS
# ============================================================

def create_pdf(path, title):
    c = canvas.Canvas(str(path), pagesize=LETTER)
    width, height = LETTER

    c.setTitle(title)

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, title)

    c.setStrokeColor(colors.grey)
    c.line(50, height - 60, width - 50, height - 60)

    return c


def finish_pdf(c, path):
    c.save()


def draw_field(c, label, value, x, y, label_width=120):
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x, y, label)

    c.setFont("Helvetica", 9)
    c.drawString(x + label_width, y, str(value))


def draw_table_header(c, headers, x_positions, y):
    c.setFillColor(colors.lightgrey)

    for i in range(len(headers)):
        c.rect(
            x_positions[i],
            y - 15,
            x_positions[i + 1] - x_positions[i],
            20,
            fill=1,
            stroke=1,
        )

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 8)

    for i, header in enumerate(headers):
        c.drawString(x_positions[i] + 4, y - 8, header)


# ============================================================
# PAY STUB
# ============================================================

def generate_pay_stub(path, borrower, month_offset=0):
    c = create_pdf(path, "EARNINGS STATEMENT")

    width, height = LETTER

    pay_date = date(2025, 2, 14) + timedelta(days=30 * month_offset)
    period_start = pay_date - timedelta(days=13)

    annual_income = borrower["annual_income"]

    monthly_income = annual_income / 12
    biweekly_gross = annual_income / 26

    federal_tax = biweekly_gross * 0.16
    social_security = biweekly_gross * 0.062
    medicare = biweekly_gross * 0.0145

    deductions = federal_tax + social_security + medicare
    net_pay = biweekly_gross - deductions

    y = height - 95

    # Employer
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, borrower["employer_name"])

    c.setFont("Helvetica", 9)
    c.drawString(50, y - 15, "100 Technology Drive")
    c.drawString(50, y - 28, "Austin, TX 78701")

    y -= 65

    # Employee information
    draw_field(c, "Employee:", borrower["borrower_name"], 50, y)
    draw_field(c, "Employee ID:", "EMP-10482", 330, y)

    y -= 20

    draw_field(c, "Address:", borrower["address"], 50, y)
    draw_field(c, "Pay Date:", pay_date.strftime("%m/%d/%Y"), 330, y)

    y -= 20

    draw_field(
        c,
        "Pay Period:",
        f"{period_start.strftime('%m/%d/%Y')} - {pay_date.strftime('%m/%d/%Y')}",
        50,
        y,
    )

    y -= 40

    # Earnings table
    headers = ["Earnings", "Current", "YTD"]
    positions = [50, 250, 350, 500]

    draw_table_header(c, headers, positions, y)

    y -= 30

    ytd_gross = biweekly_gross * (2 + month_offset * 2)

    c.setFont("Helvetica", 9)

    c.drawString(55, y, "Regular Pay")
    c.drawRightString(345, y, f"${biweekly_gross:,.2f}")
    c.drawRightString(495, y, f"${ytd_gross:,.2f}")

    y -= 20

    c.drawString(55, y, "Gross Pay")
    c.drawRightString(345, y, f"${biweekly_gross:,.2f}")
    c.drawRightString(495, y, f"${ytd_gross:,.2f}")

    y -= 40

    # Deductions
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Deductions")

    y -= 20

    deductions_data = [
        ("Federal Income Tax", federal_tax),
        ("Social Security", social_security),
        ("Medicare", medicare),
    ]

    c.setFont("Helvetica", 9)

    for label, amount in deductions_data:
        c.drawString(55, y, label)
        c.drawRightString(345, y, f"${amount:,.2f}")
        y -= 18

    y -= 15

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Net Pay")
    c.drawRightString(345, y, f"${net_pay:,.2f}")

    y -= 50

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Employment Information")

    y -= 20

    draw_field(c, "Job Title:", borrower["job_title"], 50, y)
    draw_field(c, "Hire Date:", borrower["employment_start"], 330, y)

    y -= 40

    c.setFont("Helvetica-Oblique", 8)
    c.drawString(
        50,
        y,
        "This earnings statement is a synthetic document generated for testing purposes.",
    )

    finish_pdf(c, path)


# ============================================================
# BANK STATEMENT
# ============================================================

def generate_bank_statement(path, borrower, month_offset=0, unexplained_deposit=False):
    c = create_pdf(path, "BANK STATEMENT")

    width, height = LETTER

    account_number = "XXXX-4821"

    beginning_balance = borrower["assets"]["checking"]

    if month_offset > 0:
        beginning_balance += month_offset * 2500

    transactions = []

    # Payroll deposits
    transactions.append(
        ("02/14/2025", "PAYROLL ACME TECHNOLOGIES", 3692.31)
    )

    transactions.append(
        ("02/28/2025", "PAYROLL ACME TECHNOLOGIES", 3692.31)
    )

    # Normal expenses
    transactions.extend([
        ("02/03/2025", "MORTGAGE PAYMENT", -2100.00),
        ("02/05/2025", "UTILITY PAYMENT", -185.42),
        ("02/08/2025", "GROCERY STORE", -146.72),
        ("02/11/2025", "AUTO PAYMENT", -450.00),
        ("02/17/2025", "CREDIT CARD PAYMENT", -400.00),
        ("02/20/2025", "ONLINE TRANSFER", -500.00),
        ("02/25/2025", "GROCERY STORE", -132.18),
    ])

    if unexplained_deposit:
        transactions.insert(
            4,
            ("02/15/2025", "CASH DEPOSIT", 15000.00)
        )

    ending_balance = beginning_balance + sum(
        amount for _, _, amount in transactions
    )

    y = height - 90

    # Bank header
    c.setFont("Helvetica-Bold", 15)
    c.drawString(50, y, "FIRST NATIONAL BANK")

    c.setFont("Helvetica", 9)
    c.drawString(50, y - 18, "Austin Banking Center")
    c.drawString(50, y - 32, "Austin, TX")

    y -= 70

    draw_field(c, "Account Holder:", borrower["borrower_name"], 50, y)
    draw_field(c, "Account:", account_number, 330, y)

    y -= 20

    draw_field(c, "Statement Period:", "02/01/2025 - 02/28/2025", 50, y)
    draw_field(c, "Account Type:", "Checking", 330, y)

    y -= 35

    # Summary
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "ACCOUNT SUMMARY")

    y -= 22

    draw_field(
        c,
        "Beginning Balance:",
        f"${beginning_balance:,.2f}",
        50,
        y,
    )

    y -= 18

    draw_field(
        c,
        "Ending Balance:",
        f"${ending_balance:,.2f}",
        50,
        y,
    )

    y -= 40

    # Transaction table
    headers = ["Date", "Description", "Amount", "Balance"]
    positions = [50, 120, 355, 440, 540]

    draw_table_header(c, headers, positions, y)

    running_balance = beginning_balance

    y -= 30

    c.setFont("Helvetica", 8)

    for transaction_date, description, amount in transactions:

        running_balance += amount

        c.drawString(55, y, transaction_date)
        c.drawString(125, y, description)

        if amount >= 0:
            c.drawRightString(
                430,
                y,
                f"+${amount:,.2f}",
            )
        else:
            c.drawRightString(
                430,
                y,
                f"-${abs(amount):,.2f}",
            )

        c.drawRightString(
            530,
            y,
            f"${running_balance:,.2f}",
        )

        y -= 20

    y -= 30

    c.setFont("Helvetica-Oblique", 8)

    c.drawString(
        50,
        y,
        "This bank statement is a synthetic document generated for testing purposes.",
    )

    finish_pdf(c, path)


# ============================================================
# W-2
# ============================================================

def generate_w2(path, borrower):
    c = create_pdf(path, "W-2 WAGE AND TAX STATEMENT")

    width, height = LETTER

    annual_income = borrower["annual_income"]

    federal_tax = annual_income * 0.16
    social_security_wages = annual_income
    social_security_tax = annual_income * 0.062
    medicare_wages = annual_income
    medicare_tax = annual_income * 0.0145

    y = height - 90

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "W-2 WAGE AND TAX STATEMENT")

    y -= 35

    # Employer section
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "EMPLOYER INFORMATION")

    y -= 22

    draw_field(
        c,
        "Employer:",
        borrower["employer_name"],
        50,
        y,
    )

    y -= 18

    draw_field(
        c,
        "Employer Address:",
        "100 Technology Drive, Austin, TX 78701",
        50,
        y,
    )

    y -= 35

    # Employee section
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "EMPLOYEE INFORMATION")

    y -= 22

    draw_field(
        c,
        "Employee:",
        borrower["borrower_name"],
        50,
        y,
    )

    y -= 18

    draw_field(
        c,
        "Employee Address:",
        borrower["address"],
        50,
        y,
    )

    y -= 40

    # W2 boxes
    headers = [
        "Box",
        "Description",
        "Amount",
    ]

    positions = [50, 100, 370, 520]

    draw_table_header(c, headers, positions, y)

    y -= 30

    w2_data = [
        ("1", "Wages, tips, other compensation", annual_income),
        ("2", "Federal income tax withheld", federal_tax),
        ("3", "Social Security wages", social_security_wages),
        ("4", "Social Security tax withheld", social_security_tax),
        ("5", "Medicare wages and tips", medicare_wages),
        ("6", "Medicare tax withheld", medicare_tax),
    ]

    c.setFont("Helvetica", 9)

    for box, description, amount in w2_data:
        c.drawString(55, y, box)
        c.drawString(105, y, description)
        c.drawRightString(510, y, f"${amount:,.2f}")
        y -= 22

    y -= 25

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Tax Year:")
    c.setFont("Helvetica", 10)
    c.drawString(110, y, "2024")

    y -= 40

    c.setFont("Helvetica-Oblique", 8)
    c.drawString(
        50,
        y,
        "This W-2 is a synthetic document generated for testing purposes.",
    )

    finish_pdf(c, path)


# ============================================================
# LOAN APPLICATION
# ============================================================

def generate_loan_application(path, borrower):
    c = create_pdf(path, "RESIDENTIAL LOAN APPLICATION")

    width, height = LETTER

    y = height - 90

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "BORROWER INFORMATION")

    y -= 25

    draw_field(c, "Borrower Name:", borrower["borrower_name"], 50, y)

    y -= 20

    draw_field(c, "Date of Birth:", borrower["dob"], 50, y)

    y -= 20

    draw_field(c, "Current Address:", borrower["address"], 50, y)

    y -= 40

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "EMPLOYMENT")

    y -= 25

    draw_field(c, "Employer:", borrower["employer_name"], 50, y)

    y -= 20

    draw_field(c, "Job Title:", borrower["job_title"], 50, y)

    y -= 20

    draw_field(c, "Employment Start:", borrower["employment_start"], 50, y)

    y -= 40

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "INCOME")

    y -= 25

    draw_field(
        c,
        "Annual Income:",
        f"${borrower['annual_income']:,.2f}",
        50,
        y,
    )

    y -= 40

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "LOAN INFORMATION")

    y -= 25

    draw_field(
        c,
        "Requested Loan:",
        f"${borrower['loan_amount']:,.2f}",
        50,
        y,
    )

    y -= 20

    draw_field(
        c,
        "Property Value:",
        f"${borrower['property_value']:,.2f}",
        50,
        y,
    )

    y -= 20

    draw_field(
        c,
        "Property Address:",
        borrower["property_address"],
        50,
        y,
    )

    y -= 20

    draw_field(
        c,
        "Property Type:",
        borrower["property_type"],
        50,
        y,
    )

    y -= 40

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "ASSETS")

    y -= 25

    for account, balance in borrower["assets"].items():
        draw_field(
            c,
            account.title() + ":",
            f"${balance:,.2f}",
            50,
            y,
        )
        y -= 20

    y -= 20

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "LIABILITIES")

    y -= 25

    for debt_type, payment in borrower["debts"].items():
        draw_field(
            c,
            debt_type.title() + ":",
            f"${payment:,.2f}/month",
            50,
            y,
        )
        y -= 20

    finish_pdf(c, path)


# ============================================================
# APPRAISAL
# ============================================================

def generate_appraisal(path, borrower):
    c = create_pdf(path, "RESIDENTIAL APPRAISAL REPORT")

    width, height = LETTER

    y = height - 90

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "RESIDENTIAL APPRAISAL REPORT")

    y -= 35

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "PROPERTY INFORMATION")

    y -= 22

    draw_field(c, "Property Address:", borrower["property_address"], 50, y)

    y -= 20

    draw_field(c, "Property Type:", borrower["property_type"], 50, y)

    y -= 20

    draw_field(c, "County:", "Travis County", 50, y)

    y -= 20

    draw_field(c, "State:", "Texas", 50, y)

    y -= 40

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "VALUATION")

    y -= 25

    draw_field(
        c,
        "Appraised Value:",
        f"${borrower['appraised_value']:,.2f}",
        50,
        y,
    )

    y -= 20

    draw_field(
        c,
        "Effective Date:",
        "02/10/2025",
        50,
        y,
    )

    y -= 40

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "COMPARABLE SALES")

    y -= 25

    headers = ["Property", "Sale Price", "Distance", "Bedrooms"]
    positions = [50, 250, 350, 430, 520]

    draw_table_header(c, headers, positions, y)

    comps = [
        ("738 Oak Street", "$495,000", "0.8 mi", "3"),
        ("821 Pine Avenue", "$510,000", "1.2 mi", "3"),
        ("612 Cedar Lane", "$498,500", "1.0 mi", "4"),
    ]

    y -= 30

    c.setFont("Helvetica", 8)

    for address, price, distance, bedrooms in comps:
        c.drawString(55, y, address)
        c.drawString(255, y, price)
        c.drawString(355, y, distance)
        c.drawString(435, y, bedrooms)
        y -= 20

    y -= 35

    c.setFont("Helvetica-Oblique", 8)
    c.drawString(
        50,
        y,
        "This appraisal report is a synthetic document generated for testing purposes.",
    )

    finish_pdf(c, path)


# ============================================================
# SCENARIOS
# ============================================================

def apply_scenario(base, scenario):
    data = json.loads(json.dumps(base))

    flags = []
    conditions = []
    missing_documents = []

    if scenario == "clean":
        pass

    elif scenario == "income_discrepancy":
        data["application_income"] = 120000
        flags.append("income_discrepancy")
        conditions.append("Verify stated annual income against supporting documents.")

    elif scenario == "high_dti":
        data["debts"]["auto"] = 1500
        data["debts"]["student"] = 1000
        data["debts"]["credit_cards"] = 1500

        flags.append("high_dti")
        conditions.append("Debt-to-income ratio exceeds the configured threshold.")

    elif scenario == "missing_w2":
        missing_documents.append("w2")
        flags.append("missing_w2")
        conditions.append("W-2 documentation is missing.")

    elif scenario == "missing_bank_statement":
        missing_documents.append("bank_statement_02")
        flags.append("missing_bank_statement")
        conditions.append("Required bank statement is missing.")

    elif scenario == "unexplained_deposit":
        data["unexplained_deposit"] = 15000
        flags.append("unexplained_deposit")
        conditions.append("Large unexplained deposit requires sourcing.")

    elif scenario == "employment_gap":
        data["previous_employer"] = "Previous Software Corp."
        data["previous_employment_end"] = "2024-03-01"
        data["employment_start"] = "2024-06-01"

        flags.append("employment_gap")
        conditions.append("Employment history contains a documented gap.")

    elif scenario == "asset_discrepancy":
        data["declared_assets"] = 125000
        flags.append("asset_discrepancy")
        conditions.append("Declared assets differ from verified account balances.")

    elif scenario == "income_dti_discrepancy":
        data["application_income"] = 120000

        data["debts"]["auto"] = 1500
        data["debts"]["student"] = 1000
        data["debts"]["credit_cards"] = 1500

        flags.extend([
            "income_discrepancy",
            "high_dti",
        ])

        conditions.extend([
            "Verify stated annual income against supporting documents.",
            "Debt-to-income ratio exceeds the configured threshold.",
        ])

    elif scenario == "missing_tax_return":
        missing_documents.append("tax_return")
        flags.append("missing_tax_return")
        conditions.append("Required tax return documentation is missing.")

    elif scenario == "employment_inconsistency":
        data["application_employer"] = "Acme Software LLC"

        flags.append("employment_inconsistency")
        conditions.append("Employer name differs between application and supporting documents.")

    elif scenario == "property_value_discrepancy":
        data["application_property_value"] = 550000

        flags.append("property_value_discrepancy")
        conditions.append("Application property value differs from appraisal.")

    elif scenario == "missing_paystub":
        missing_documents.append("pay_stub_02")
        flags.append("missing_paystub")
        conditions.append("Required pay stub is missing.")

    elif scenario == "multiple_discrepancies":
        data["application_income"] = 120000
        data["declared_assets"] = 125000
        data["application_employer"] = "Acme Software LLC"

        flags.extend([
            "income_discrepancy",
            "asset_discrepancy",
            "employment_inconsistency",
        ])

        conditions.extend([
            "Verify stated annual income against supporting documents.",
            "Declared assets differ from verified account balances.",
            "Employer name differs between application and supporting documents.",
        ])

    elif scenario == "incomplete_paystubs":
        missing_documents.append("pay_stub_02")
        flags.append("incomplete_paystubs")
        conditions.append("Required pay stub documentation is incomplete.")

    elif scenario == "employment_inconsistency":
        data["application_employer"] = "Acme Software LLC"

        flags.append("employment_inconsistency")
        conditions.append("Employer name differs between application and supporting documents.")

    elif scenario == "property_value_discrepancy":
        data["application_property_value"] = 550000

        flags.append("property_value_discrepancy")
        conditions.append("Application property value differs from appraisal.")

    elif scenario == "missing_appraisal":
        missing_documents.append("appraisal")
        flags.append("missing_appraisal")
        conditions.append("Property appraisal is missing.")

    elif scenario == "complex_mixed":
        data["application_income"] = 120000
        data["declared_assets"] = 125000
        data["unexplained_deposit"] = 15000
        data["application_employer"] = "Acme Software LLC"

        data["debts"]["auto"] = 1500
        data["debts"]["student"] = 1000
        data["debts"]["credit_cards"] = 1500

        missing_documents.append("tax_return")

        flags.extend([
            "income_discrepancy",
            "asset_discrepancy",
            "unexplained_deposit",
            "employment_inconsistency",
            "high_dti",
            "missing_tax_return",
        ])

        conditions.extend([
            "Verify stated annual income against supporting documents.",
            "Declared assets differ from verified account balances.",
            "Large unexplained deposit requires sourcing.",
            "Employer name differs between application and supporting documents.",
            "Debt-to-income ratio exceeds the configured threshold.",
            "Required tax return documentation is missing.",
        ])

    return data, flags, conditions, missing_documents


# ============================================================
# GROUND TRUTH
# ============================================================

def create_ground_truth(loan_id, scenario, data, flags, conditions, missing_documents):

    verified_income = data["annual_income"]
    application_income = data.get(
        "application_income",
        verified_income,
    )

    monthly_income = verified_income / 12

    monthly_debt = sum(data["debts"].values())

    dti = (
        monthly_debt / monthly_income
        if monthly_income > 0
        else 0
    ) * 100

    verified_assets = sum(data["assets"].values())

    declared_assets = data.get(
        "declared_assets",
        verified_assets,
    )

    application_property_value = data.get(
        "application_property_value",
        data["property_value"],
    )

    status = "review" if flags or missing_documents else "pass"

    return {
        "loan_id": loan_id,
        "scenario": scenario,

        "borrower": {
            "name": data["borrower_name"],
        },

        "income": {
            "application_annual": application_income,
            "verified_annual": verified_income,
            "verified_monthly": monthly_income,
        },

        "debts": {
            "monthly": monthly_debt,
        },

        "dti": {
            "percentage": round(dti, 2),
            "threshold": 43.0,
        },

        "assets": {
            "verified": verified_assets,
            "declared": declared_assets,
        },

        "property": {
            "loan_amount": data["loan_amount"],
            "application_value": application_property_value,
            "appraised_value": data["appraised_value"],
        },

        "expected_flags": flags,
        "expected_conditions": conditions,
        "missing_documents": missing_documents,

        "expected_status": status,
    }


# ============================================================
# GENERATE ONE LOAN
# ============================================================

def generate_loan(loan_id, scenario):

    loan_dir = BASE_DIR / loan_id

    if loan_dir.exists():
        shutil.rmtree(loan_dir)

    loan_dir.mkdir(parents=True)

    data, flags, conditions, missing_documents = apply_scenario(
        BASE_BORROWER,
        scenario,
    )

    # ----------------------------------------
    # Loan application
    # ----------------------------------------

    if "loan_application" not in missing_documents:

        generate_loan_application(
            loan_dir / "loan_application.pdf",
            data,
        )

    # ----------------------------------------
    # Pay stubs
    # ----------------------------------------

    if "pay_stub_01" not in missing_documents:

        generate_pay_stub(
            loan_dir / "pay_stub_01.pdf",
            data,
            month_offset=0,
        )

    if "pay_stub_02" not in missing_documents:

        generate_pay_stub(
            loan_dir / "pay_stub_02.pdf",
            data,
            month_offset=1,
        )

    # ----------------------------------------
    # W2
    # ----------------------------------------

    if "w2" not in missing_documents:

        generate_w2(
            loan_dir / "w2.pdf",
            data,
        )

    # ----------------------------------------
    # Bank statements
    # ----------------------------------------

    if "bank_statement_01" not in missing_documents:

        generate_bank_statement(
            loan_dir / "bank_statement_01.pdf",
            data,
            month_offset=0,
            unexplained_deposit=(
                data.get("unexplained_deposit", 0) > 0
            ),
        )

    if "bank_statement_02" not in missing_documents:

        generate_bank_statement(
            loan_dir / "bank_statement_02.pdf",
            data,
            month_offset=1,
            unexplained_deposit=False,
        )

    # ----------------------------------------
    # Tax return
    # ----------------------------------------

    if "tax_return" not in missing_documents:

        c = create_pdf(
            loan_dir / "tax_return.pdf",
            "FEDERAL INDIVIDUAL INCOME TAX RETURN",
        )

        y = LETTER[1] - 90

        c.setFont("Helvetica-Bold", 13)
        c.drawString(
            50,
            y,
            "FEDERAL INDIVIDUAL INCOME TAX RETURN",
        )

        y -= 35

        draw_field(
            c,
            "Taxpayer:",
            data["borrower_name"],
            50,
            y,
        )

        y -= 20

        draw_field(
            c,
            "Tax Year:",
            "2024",
            50,
            y,
        )

        y -= 30

        draw_field(
            c,
            "Wages:",
            f"${data['annual_income']:,.2f}",
            50,
            y,
        )

        y -= 20

        draw_field(
            c,
            "Adjusted Gross Income:",
            f"${data['annual_income']:,.2f}",
            50,
            y,
        )

        y -= 40

        c.setFont("Helvetica-Oblique", 8)
        c.drawString(
            50,
            y,
            "This tax return is a synthetic document generated for testing purposes.",
        )

        finish_pdf(
            c,
            loan_dir / "tax_return.pdf",
        )

    # ----------------------------------------
    # Appraisal
    # ----------------------------------------

    if "appraisal" not in missing_documents:

        appraisal_data = dict(data)

        if scenario == "property_value_discrepancy":
            appraisal_data["appraised_value"] = 500000

        generate_appraisal(
            loan_dir / "appraisal.pdf",
            appraisal_data,
        )

    # ----------------------------------------
    # Ground truth
    # ----------------------------------------

    ground_truth = create_ground_truth(
        loan_id,
        scenario,
        data,
        flags,
        conditions,
        missing_documents,
    )

    with open(
        loan_dir / "ground_truth.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            ground_truth,
            f,
            indent=4,
        )

    print(
        f"Generated {loan_id} | "
        f"{scenario} | "
        f"Status: {ground_truth['expected_status']}"
    )


# ============================================================
# DATASET
# ============================================================

SCENARIOS = [
    ("LOAN-0001", "clean"),
    ("LOAN-0002", "income_discrepancy"),
    ("LOAN-0003", "high_dti"),
    ("LOAN-0004", "missing_w2"),
    ("LOAN-0005", "missing_bank_statement"),
    ("LOAN-0006", "unexplained_deposit"),
    ("LOAN-0007", "employment_gap"),
    ("LOAN-0008", "income_dti_discrepancy"),
    ("LOAN-0009", "missing_tax_return"),
    ("LOAN-0010", "asset_discrepancy"),
    ("LOAN-0011", "clean"),
    ("LOAN-0012", "multiple_discrepancies"),
    ("LOAN-0013", "incomplete_paystubs"),
    ("LOAN-0014", "employment_inconsistency"),
    ("LOAN-0015", "property_value_discrepancy"),
    ("LOAN-0016", "clean"),
    ("LOAN-0017", "unexplained_deposit"),
    ("LOAN-0018", "income_dti_discrepancy"),
    ("LOAN-0019", "missing_appraisal"),
    ("LOAN-0020", "complex_mixed"),
]


def main():

    print("\nGenerating synthetic loan dataset...\n")

    for loan_id, scenario in SCENARIOS:
        generate_loan(
            loan_id,
            scenario,
        )

    print("\nDataset generation complete.")
    print(f"Location: {BASE_DIR.resolve()}")


if __name__ == "__main__":
    main()