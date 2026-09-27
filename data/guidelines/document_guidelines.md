# Synthetic Document Underwriting Guidelines

> This document contains synthetic rules created for the Loan Officer Copilot demo.
> These rules are not official mortgage underwriting guidelines.

## DOC-001 — W-2 Documentation

A W-2 document should be present when the synthetic loan scenario requires W-2 income verification.

The document may be used to verify:

- Employee name
- Employer
- W-2 wages
- Tax year

A missing required W-2 should be identified as an open condition.

## DOC-002 — Bank Statement Documentation

Required bank statements should be present when asset verification depends on those statements.

Bank statements may be used to verify:

- Account holder
- Account number
- Beginning balance
- Ending balance
- Deposits

A missing required bank statement should be identified as an open condition.

## DOC-003 — Tax Return Documentation

A tax return should be present when the synthetic loan scenario requires tax return verification.

The document may be used to review:

- Taxpayer
- Tax year
- Wages
- Adjusted gross income

A missing required tax return should be identified as an open condition.

## DOC-004 — Pay Stub Documentation

Required pay stubs should be present when current income verification depends on them.

Pay stubs may be used to verify:

- Employee name
- Employer
- Job title
- Gross pay
- Net pay

A missing required pay stub should be identified as an open condition.

## DOC-005 — Appraisal Documentation

An appraisal should be present when property valuation is required for the synthetic loan scenario.

The appraisal may be used to verify:

- Property address
- Property type
- Appraised value

A missing appraisal should be identified as an open condition.

## DOC-006 — Document Completeness

Required documents should be checked before the loan file is considered complete.

The system should identify:

- Missing documents
- Unexpected document types
- Documents required for a specific verification
- Documents associated with open underwriting conditions

Missing documentation should be reported clearly to the loan officer.