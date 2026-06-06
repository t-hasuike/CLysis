<!-- This instruction facet is based on the TAKT framework (https://github.com/nrslib/takt), MIT License, Copyright (c) 2026 Masanobu Naruse. -->
# SEM Audit - G2 Quality Audit Procedure

## Overview

For the SEM-draft.md produced by the sem-writer, confirm every item of the G2 quality gate from an independent perspective and judge pass/fail.

---

## Audit Procedure

### A. mermaid syntax validation

```bash
mmdc -i <path to SEM-draft.md> -o /tmp/sem_audit_check.png
```

Pass condition: 0 errors. Even 1 error is a fail.

Record: the command and output (the full error message or "0 errors").

### B. Forbidden-keyword grep

Confirm that the following pattern is not contained in SEM-draft.md:

```bash
grep -n "Users\/" <path to SEM-draft.md>
```

In addition, refer to the forbidden keywords defined for your project (internal names, service-specific terms, etc.; see [your-project-standards-doc]) and similarly confirm 0 occurrences with grep.

Pass condition: 0. Even 1 hit is a fail.

Record: the command and output (count, matching lines, or "0").

### C. Unicode symbol grep

Confirm that no Unicode symbols (arrows, box-drawing, emoji, etc.) appear outside code blocks:

```bash
grep -nP "[\x{2190}-\x{2BFF}\x{1F000}-\x{1FAFF}]" <path to SEM-draft.md>
```

Pass condition: 0 (symbols inside code blocks are allowed). The count outside code blocks must be 0.

Record: the command and output (count, matching lines, or "0").

### D. Business-meaning description check (axes 1-7)

Confirm the following 7 axes in SEM-draft.md:

| Axis | Check content | Pass condition |
| :--- | :--- | :--- |
| Axis 1 | Does chapter 1 start from the domain purpose (why it exists)? | It does not start from a bare list of table names |
| Axis 2 | Are the primary domain terms defined? | There is a definition of business terms in section 1.2 or chapter 3 |
| Axis 3 | Are route differences explained as differences in the business model? | When route differences exist, not only "the table differs" but also "the difference in business meaning" is explained |
| Axis 4 | Does every table in chapter 3 have a "business meaning" column? | Every table and every required column has a "business meaning" column |
| Axis 5 | Does the flag table in chapter 4 describe the meaning of values? | Not only "0/1/2" but also "what it means" is present |
| Axis 6 | Is the scope decided by business concepts rather than physical location of tables? | There is no statement like "in scope because it is a table in [primary-db]" |
| Axis 7 | When spanning multiple databases, is the business meaning of join keys present? | The "business meaning" of join keys is explained (skip axis 7 when there is no spanning) |

### E. Soft-delete condition check

```bash
grep -n "delflag" <path to SEM-draft.md>
```

Pass condition: every SQL statement in chapter 6 contains the project's soft-delete condition (e.g., `delflag = '0'`).

### F. Three-pitfalls check

```bash
grep -n "^### T-" <path to SEM-draft.md>
```

Pass condition: T-1, T-2, T-3 or more exist (at least 3).

---

## Pass/Fail Judgement

When all audit items (A-F) pass: **pass** -> transition to create_pr

When even one item fails: **fail** -> roll back to execute_sem

---

## Format of the deliverable (sem-audit.md)

```
# SEM Audit Report - SEM-XX

## Audit target: <path to SEM-draft.md>
## Audit date: YYYY-MM-DD

## Result summary

| Audit item | Result | Notes |
| :--- | :--- | :--- |
| A. mermaid validation | pass/fail | [command, output] |
| B. Forbidden keywords | pass/fail | [command, output] |
| C. Unicode symbols | pass/fail | [command, output] |
| D. Business meaning (axes 1-7) | pass/fail | [if failing, axis number and reason] |
| E. Soft-delete condition | pass/fail | [command, output] |
| F. Three pitfalls | pass/fail | [command, output] |

## Overall verdict: pass / fail

## Fix instructions when failing

[For each failing item, write the 3-part set: "fix location, fix content, rationale"]
```
