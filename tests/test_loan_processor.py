from app.underwriting.loan_processor import process_loan
from app.schemas.underwriting import UnderwritingStatus


def get_condition_ids(result):
    return [condition.condition_id for condition in result.conditions]


def test_process_clean_loan():
    result = process_loan("data/synthetic/LOAN-0001")

    assert result.loan_id == "LOAN-0001"
    assert result.status == UnderwritingStatus.PASS
    assert result.dti.dti_percentage == 15.0
    assert len(result.conditions) == 0


def test_process_income_discrepancy():
    result = process_loan("data/synthetic/LOAN-0002")

    assert result.loan_id == "LOAN-0002"
    assert result.status == UnderwritingStatus.REVIEW
    assert "INC-001" in get_condition_ids(result)


def test_process_high_dti():
    result = process_loan("data/synthetic/LOAN-0003")

    assert result.loan_id == "LOAN-0003"
    assert result.status == UnderwritingStatus.REVIEW
    assert result.dti.dti_percentage == 50.0
    assert "DTI-001" in get_condition_ids(result)


def test_process_asset_discrepancy():
    result = process_loan("data/synthetic/LOAN-0010")

    assert result.loan_id == "LOAN-0010"
    assert result.status == UnderwritingStatus.REVIEW
    assert "AST-001" in get_condition_ids(result)


def test_process_missing_w2():
    result = process_loan("data/synthetic/LOAN-0004")

    assert result.loan_id == "LOAN-0004"
    assert result.status == UnderwritingStatus.REVIEW


def test_process_missing_bank_statement():
    result = process_loan("data/synthetic/LOAN-0005")

    assert result.loan_id == "LOAN-0005"
    assert result.status == UnderwritingStatus.REVIEW


def test_process_unexplained_deposit():
    result = process_loan("data/synthetic/LOAN-0006")

    assert result.loan_id == "LOAN-0006"
    assert result.status == UnderwritingStatus.REVIEW


def test_process_employment_gap():
    result = process_loan("data/synthetic/LOAN-0007")

    assert result.loan_id == "LOAN-0007"
    assert result.status == UnderwritingStatus.REVIEW


def test_process_income_and_dti_discrepancy():
    result = process_loan("data/synthetic/LOAN-0008")

    assert result.loan_id == "LOAN-0008"
    assert result.status == UnderwritingStatus.REVIEW

    condition_ids = get_condition_ids(result)

    assert "INC-001" in condition_ids
    assert "DTI-001" in condition_ids


def test_process_missing_tax_return():
    result = process_loan("data/synthetic/LOAN-0009")

    assert result.loan_id == "LOAN-0009"
    assert result.status == UnderwritingStatus.REVIEW


def test_process_multiple_discrepancies():
    result = process_loan("data/synthetic/LOAN-0012")

    assert result.loan_id == "LOAN-0012"
    assert result.status == UnderwritingStatus.REVIEW

    condition_ids = get_condition_ids(result)

    assert "INC-001" in condition_ids
    assert "AST-001" in condition_ids
    assert "EMP-001" in condition_ids


def test_process_incomplete_paystubs():
    result = process_loan("data/synthetic/LOAN-0013")

    assert result.loan_id == "LOAN-0013"
    assert result.status == UnderwritingStatus.REVIEW


def test_process_employment_inconsistency():
    result = process_loan("data/synthetic/LOAN-0014")

    assert result.loan_id == "LOAN-0014"
    assert result.status == UnderwritingStatus.REVIEW

    assert "EMP-001" in get_condition_ids(result)


def test_process_property_value_discrepancy():
    result = process_loan("data/synthetic/LOAN-0015")

    assert result.loan_id == "LOAN-0015"
    assert result.status == UnderwritingStatus.REVIEW


def test_process_unexplained_deposit_2():
    result = process_loan("data/synthetic/LOAN-0017")

    assert result.loan_id == "LOAN-0017"
    assert result.status == UnderwritingStatus.REVIEW


def test_process_income_and_dti_discrepancy_2():
    result = process_loan("data/synthetic/LOAN-0018")

    assert result.loan_id == "LOAN-0018"
    assert result.status == UnderwritingStatus.REVIEW

    condition_ids = get_condition_ids(result)

    assert "INC-001" in condition_ids
    assert "DTI-001" in condition_ids


def test_process_missing_appraisal():
    result = process_loan("data/synthetic/LOAN-0019")

    assert result.loan_id == "LOAN-0019"
    assert result.status == UnderwritingStatus.REVIEW


def test_process_complex_mixed():
    result = process_loan("data/synthetic/LOAN-0020")

    assert result.loan_id == "LOAN-0020"
    assert result.status == UnderwritingStatus.REVIEW

    condition_ids = get_condition_ids(result)

    assert "INC-001" in condition_ids
    assert "AST-001" in condition_ids
    assert "EMP-001" in condition_ids
    assert "DTI-001" in condition_ids