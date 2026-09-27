from langchain_groq import ChatGroq

from app.schemas.underwriting import UnderwritingResult


class ExplanationAgent:
    """
    Converts deterministic underwriting results into
    loan-officer-friendly explanations.

    IMPORTANT:
    This agent does NOT make underwriting decisions.
    It only explains decisions already produced by the
    deterministic underwriting engine.
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "llama-3.1-8b-instant",
    ):
        self.llm = ChatGroq(
            api_key=api_key,
            model=model,
            temperature=0,
        )

    def build_prompt(self, result: UnderwritingResult) -> str:
        conditions_text = ""

        if result.conditions:
            for condition in result.conditions:
                conditions_text += (
                    f"- Condition ID: {condition.condition_id}\n"
                    f"  Title: {condition.title}\n"
                    f"  Description: {condition.description}\n"
                    f"  Severity: {condition.severity.value}\n"
                    f"  Rule ID: {condition.rule_id}\n"
                    f"  Source documents: "
                    f"{', '.join(condition.source_documents)}\n\n"
                )
        else:
            conditions_text = "No underwriting conditions were identified."

        verification_text = ""

        if result.verification_results:
            for verification in result.verification_results:
                verification_text += (
                    f"- {verification.check_name}: "
                    f"{'PASSED' if verification.passed else 'FAILED'}\n"
                    f"  {verification.description}\n"
                )
        else:
            verification_text = "No verification results available."

        dti_text = "No DTI calculation available."

        if result.dti:
            dti_text = (
                f"Monthly income: ${result.dti.monthly_income:,.2f}\n"
                f"Monthly debt: ${result.dti.monthly_debt:,.2f}\n"
                f"DTI: {result.dti.dti_percentage:.2f}%\n"
                f"Threshold: {result.dti.threshold_percentage:.2f}%\n"
                f"DTI check: "
                f"{'PASSED' if result.dti.passed else 'FAILED'}"
            )

        prompt = f"""
You are an explanation assistant for a mortgage loan officer.

Your job is ONLY to explain the underwriting analysis that has
already been performed.

You MUST NOT:
- make a new underwriting decision
- approve or deny the loan
- invent missing facts
- invent guideline requirements
- change the severity of a condition
- contradict the supplied underwriting result
- claim that a rule comes from Fannie Mae, FHA, Freddie Mac,
  or another organization unless that information is explicitly
  provided

The deterministic underwriting engine has already produced the result.

LOAN ID:
{result.loan_id}

UNDERWRITING STATUS:
{result.status.value}

DTI:
{dti_text}

VERIFICATION RESULTS:
{verification_text}

UNDERWRITING CONDITIONS:
{conditions_text}

Write a concise explanation for a loan officer.

Use this structure:

Overall Status:
Explain what the current status means based only on the supplied result.

Key Findings:
List the important findings.

Conditions Requiring Attention:
Explain each open condition in plain English.
For every condition, include:
- condition ID
- what was identified
- why it matters based on the supplied description
- which source documents are relevant

Next Steps:
Suggest document-review or verification actions only.
Do not make an approval or denial recommendation.

If there are no conditions, state that no underwriting conditions
were identified by the current deterministic checks.

Keep the response professional and concise.
"""

        return prompt

    def explain(self, result: UnderwritingResult) -> str:
        prompt = self.build_prompt(result)

        response = self.llm.invoke(prompt)

        return response.content