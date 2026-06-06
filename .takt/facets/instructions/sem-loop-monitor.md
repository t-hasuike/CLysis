<!-- This instruction facet is based on the TAKT framework (https://github.com/nrslib/takt), MIT License, Copyright (c) 2026 Masanobu Naruse. -->
# SEM Loop Monitor - Loop-Health Judgement Procedure

## Overview

When the execute_sem and gate_g2 loop reaches the threshold (3 cycles), judge the health of the loop. This corresponds to takt's `loop-monitor-reviewers-fix` instruction.

---

## Judgement Procedure

### Step 1: Collect the audit reports of each cycle

Read all of the recent sem-audit.md reports across cycles (up to 3).

Confirm:
- The overall verdict (fail) of each cycle
- The audit items (A-F) that failed in each cycle
- The number of failures in each cycle

### Step 2: Confirm the improving trend

Compare the following:

| Comparison item | How to confirm |
| :--- | :--- |
| Trend in number of failures | Is the number of failures decreasing from cycle 1 -> cycle 2 -> cycle 3? |
| Kind of failing items | Does cycle 3 still contain the same failing items as cycle 1? |
| Evidence of fixes | Is there evidence that execute_sem actually made fixes (changes to SEM-draft.md)? |

### Step 3: Judgement

Conditions for **Healthy (continue)** (any one met):
- The number of failures decreased by 1 or more compared with the previous cycle
- No new failing item was added (work on the same issue is continuing)

Conditions for **Unproductive (ABORT)** (any one met):
- The failing items of the latest cycle are identical to those 2 cycles earlier
- The number of failures has not changed across 3 cycles
- execute_sem made no substantive fix (no change to SEM-draft.md)

---

## Format for recording the judgement

```
# Loop-Health Judgement

## Failure status per cycle

| Cycle | Number of failures | Failing items |
| :--- | :--- | :--- |
| Cycle 1 | N | [item names] |
| Cycle 2 | N | [item names] |
| Cycle 3 | N | [item names] |

## Improving trend

- Trend in number of failures: increasing / decreasing / flat
- Repetition of the same failure: yes / no
- Track record of fixes by execute_sem: yes / no

## Judgement

Healthy / Unproductive

## Rationale

[Describe the specific rationale for the judgement]
```

---

## Notes

- A "Healthy" judgement requires evidence of an improving trend. "Continuation without evidence" is prohibited.
- When you ABORT with an "Unproductive" judgement, report the following to the leader:
  - The failing items that are repeating
  - The recommended action (re-planning by the sem-planner / human confirmation)
