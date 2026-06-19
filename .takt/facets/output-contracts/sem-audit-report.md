<!-- This output-contract facet is based on the TAKT framework (https://github.com/nrslib/takt), MIT License, Copyright (c) 2026 Masanobu Naruse. -->
# SEM Audit Report - Quality Audit Report Format

## Overview

Format definition for the quality audit report (sem-audit.md) output by the gate_g2 step.

---

## Required Sections and Content

### Section 1: Audit target

- File path of the SEM document
- Audit date
- Cycle number of the audit target (1-3)

### Section 2: Result summary table

| Audit item | Result | Command run | Output / rationale |
| :--- | :--- | :--- | :--- |
| A. mermaid validation | pass/fail | [command] | [output] |
| B. Forbidden keywords | pass/fail | [command] | [0 or matching lines] |
| C. Unicode symbols | pass/fail | [command] | [0 or matching lines] |
| D-1. Axis 1 (domain purpose) | pass/fail | - | [rationale] |
| D-2. Axis 2 (domain terms) | pass/fail | - | [rationale] |
| D-3. Axis 3 (route differences) | pass/skip/fail | - | [rationale] |
| D-4. Axis 4 (business-meaning column) | pass/fail | - | [rationale] |
| D-5. Axis 5 (flag-value meaning) | pass/fail | - | [rationale] |
| D-6. Axis 6 (scope judgement) | pass/fail | - | [rationale] |
| D-7. Axis 7 (join-key meaning) | pass/skip/fail | - | [rationale] |
| E. Soft-delete condition | pass/fail | [command] | [output] |
| F. Three pitfalls | pass/fail | [command] | [output] |

### Section 3: Overall verdict

- pass or fail
- On pass: "All A-F items pass. Transition to create_pr"
- On fail: number of failing items (e.g., "3 items failed")

### Section 4: Fix instructions (only when failing)

For each failing item, write the following 3-part set:
- Fix location (file path, line number, target text)
- Fix content (specific fix method)
- Rationale (the rationale for why it failed)

---

## Quality Criteria

| Item | Criterion |
| :--- | :--- |
| Evidence of commands | The execution results (count, matching lines) of every grep / mermaid command are recorded |
| Clarity of judgement | Each item is stated as one of "pass", "fail", or "skip" |
| Specificity of fix instructions | When failing, the 3-part set "fix location, fix content, rationale" is complete |
| Rationale of the overall verdict | "pass" or "fail" is stated, with its rationale described |
