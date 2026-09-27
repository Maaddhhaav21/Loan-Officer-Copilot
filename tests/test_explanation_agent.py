from app.agents.explanation_agent import ExplanationAgent
from app.schemas.conditions import (
    ConditionStatus,
    Severity,
    UnderwritingCondition,
)
from app.schemas.underwriting import (
    DTIResult,
    UnderwritingResult,
    UnderwritingStatus,
    VerificationResult,
)


def create_sample_result() -> UnderwritingResult:
    return UnderwritingResult(
        loan_id="LOAN-0007",
        status=UnderwritingStatus.REVIEW,
        dti=DTIResult(
            monthly_income=8000.0,
            monthly_debt=2500.0,
            dti_percentage=31.25,
            threshold_percentage=43.0,
            passed=True,
        ),
        verification_results=[
            VerificationResult(
                check_name="income_verification",
                passed=True,
                description=(
                    "Application income ($96,000.00) is consistent "
                    "with supporting income ($96,000.03)."
                ),
                source_documents=[
                    "loan_application.pdf",
                    "w2.pdf",
                ],
            ),
            VerificationResult(
                check_name="employment_gap",
                passed=False,
                description=(
                    "Employment history contains a gap between "
                    "2024-03-01 and 2024-06-01."
                ),
                source_documents=[
                    "loan_application.pdf",
                    "employment_history.pdf",
                ],
            ),
        ],
        conditions=[
            UnderwritingCondition(
                condition_id="EMP-002",
                title="Employment gap identified",
                description=(
                    "Employment history contains a documented gap."
                ),
                severity=Severity.MEDIUM,
                status=ConditionStatus.OPEN,
                source_documents=[
                    "loan_application.pdf",
                    "employment_history.pdf",
                ],
                rule_id="EMP-002",
            )
        ],
    )


def test_explanation_agent_builds_prompt():
    agent = ExplanationAgent.__new__(ExplanationAgent)

    result = create_sample_result()

    prompt = agent.build_prompt(result)

    assert "LOAN-0007" in prompt
    assert "EMP-002" in prompt
    assert "Employment gap identified" in prompt
    assert "2024-03-01" in prompt
    assert "2024-06-01" in prompt
    assert "31.25%" in prompt
    assert "43.00%" in prompt


def test_explanation_prompt_prevents_underwriting_decision():
    agent = ExplanationAgent.__new__(ExplanationAgent)

    result = create_sample_result()

    prompt = agent.build_prompt(result)

    assert "MUST NOT" in prompt
    assert "make a new underwriting decision" in prompt
    assert "approve or deny the loan" in prompt
    assert "invent missing facts" in prompt


def test_explanation_prompt_contains_verification_results():
    agent = ExplanationAgent.__new__(ExplanationAgent)

    result = create_sample_result()

    prompt = agent.build_prompt(result)

    assert "income_verification" in prompt
    assert "PASSED" in prompt
    assert "employment_gap" in prompt
    assert "FAILED" in prompt


def test_explanation_prompt_handles_no_conditions():
    agent = ExplanationAgent.__new__(ExplanationAgent)

    result = UnderwritingResult(
        loan_id="LOAN-0001",
        status=UnderwritingStatus.PASS,
        dti=DTIResult(
            monthly_income=8000.0,
            monthly_debt=1200.0,
            dti_percentage=15.0,
            threshold_percentage=43.0,
            passed=True,
        ),
        verification_results=[],
        conditions=[],
    )

    prompt = agent.build_prompt(result)

    assert "LOAN-0001" in prompt
    assert "No underwriting conditions were identified." in prompt
    assert "no underwriting conditions were identified" in prompt.lower()