# Synthetic DTI Underwriting Guidelines

> This document contains synthetic rules created for the Loan Officer Copilot demo.
> These rules are not official mortgage underwriting guidelines.

## DTI-001 — Debt-to-Income Ratio

Debt-to-income ratio (DTI) is calculated using monthly debt obligations divided by monthly qualifying income.

Formula:

DTI = (Monthly Debt / Monthly Income) × 100

For this synthetic Loan Officer Copilot dataset, the reference DTI threshold is:

43%

A DTI at or below 43% passes the synthetic DTI check.

A DTI above 43% should be identified for underwriting review.

### Example

Monthly income:

$8,000

Monthly debt:

$4,000

DTI:

50%

Because 50% is above the synthetic 43% threshold, the file should receive a DTI review condition.

## DTI-002 — DTI Review

When the calculated DTI exceeds the synthetic threshold:

- Verify the monthly income used in the calculation.
- Verify the monthly debt obligations.
- Review the liabilities included in the calculation.
- Confirm that the calculation uses the correct financial information.

The system should explain the DTI calculation rather than making an independent lending decision.

## DTI-003 — Invalid Income

DTI cannot be calculated when monthly qualifying income is zero or negative.

Such cases should be identified as incomplete or invalid data and reviewed before calculating DTI.