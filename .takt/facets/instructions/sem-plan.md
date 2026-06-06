<!-- This instruction facet is based on the TAKT framework (https://github.com/nrslib/takt), MIT License, Copyright (c) 2026 Masanobu Naruse. -->
# SEM Plan - Planning Procedure

## Overview

Investigate the target domain and define the scope, approach, and prerequisite knowledge for the SEM document.

---

## Procedure

### Step 1: Confirm the boundary against existing SEM files

```bash
ls [your-project-knowledge-dir]/semantic/
```

Confirm the list of existing SEMs and state:
- The existing SEM closest to the target domain (clarify the boundary where scopes overlap)
- The domain range this SEM covers (the division of labor against existing SEMs)

### Step 2: Confirm the existence of target tables

For each specified primary table, confirm that the Model file exists.

```bash
grep -rn "<table-name>" [your-repo-path]/app/Models/ 2>/dev/null | head -20
```

Confirm:
- The path of the Model file (record as an absolute path)
- The physical table name from the `$table` property
- The managing database (e.g., [primary-db], [secondary-db])

### Step 3: Identify related tables

From the Models of the primary tables, extract HasMany / HasOne / BelongsTo and identify the related tables.

Confirm:
- A list of related tables (explain the business relationship in one line each)
- Classification of in-scope vs. out-of-scope tables (state the rationale for the boundary)

### Step 4: Confirm route differences

Confirm whether the target domain has multiple business routes or channels (e.g., direct sales / teacher / partner; Route A / Route B / Route C).

Confirm:
- Whether route differences exist (yes/no)
- If they exist, which column or flag the route branches on (confirm the specific column name and value)

### Step 5: G1 quality check

Only when all of the following items pass, judge "planning complete" and transition to execute_sem. If even one item fails, judge ABORT.

| Check item | Pass condition |
| :--- | :--- |
| Existence of primary tables | The Model file of every target table has been confirmed |
| Source of domain facts | Every scope definition has a source in "file path:line number" form |
| Boundary stated | Overlap and division of labor against existing SEMs is stated |
| Route differences | Presence of route differences is stated as "yes/no" |

---

## Format of the deliverable (sem-plan.md)

```
# SEM Plan

## Target domain
- SEM number: SEM-XX
- Domain name: [domain-name]

## Scope
- Target tables: [table list, with one line on each table's role]
- Exclusions: [state the reason for being out of scope]

## Boundary against existing SEMs
- [existing SEM number]: [boundary description]

## Route differences
- Presence: yes/no
- If present: [details of the branching column and value]

## Prerequisite knowledge
- [Business facts confirmed during investigation. Cite with file path:line number]

## G1 verdict
- Judgement: pass / fail (ABORT)
- Rationale: [describe the rationale for pass/fail]
```
