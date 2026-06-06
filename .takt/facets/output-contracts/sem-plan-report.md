<!-- This output-contract facet is based on the TAKT framework (https://github.com/nrslib/takt), MIT License, Copyright (c) 2026 Masanobu Naruse. -->
# SEM Plan Report - Plan Deliverable Format

## Overview

Format definition for the plan document (sem-plan.md) output by the plan step.

---

## Required Sections and Content

### Section 1: Target domain

- SEM number (e.g., SEM-02)
- Domain name
- Primary table list (one line on each table's role)

### Section 2: Scope

- In-scope tables (with sources)
- Exclusions (state the reason for exclusion)
- Boundary against existing SEMs (state any overlap)

### Section 3: Route differences

- Whether route differences exist (yes/no)
- If present: branching column, value, business meaning (with code sources)

### Section 4: Prerequisite knowledge

- Business facts confirmed during investigation
- Cite each fact in "file path:line number" form
- State assumptions as "presumed to be X (to be confirmed)"

### Section 5: G1 verdict

- Judgement: pass or ABORT
- Rationale: the specific reason for the judgement

---

## Quality Criteria

| Item | Criterion |
| :--- | :--- |
| Evidence of facts | Every scope definition has a source in "file path:line number" form |
| Transparency of assumptions | Assumptions are stated as "presumed to be X (to be confirmed)" |
| Clarity of the G1 verdict | "pass" or "ABORT" is stated |
| Boundary stated | Overlap and division of labor against existing SEMs is described |
