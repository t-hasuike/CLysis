---
name: kpt
description: Run KPT (Keep/Problem/Try) retrospectives at session boundaries and milestones. Triggers Five Whys root cause analysis for recurring problems.
argument-hint: "[--light (minimal)] [--full (default)] [--analyze (trend analysis)]"
---

> This is a generic skill from [CLysis](https://github.com/t-hasuike/CLysis).
> Terminology can be customized via `config/terminology.md`.
> Adapt paths and technology references to match your project.

# KPT Retrospective Skill

## Overview

Run KPT (Keep / Problem / Try) retrospectives at session boundaries or milestone completions to drive continuous improvement.

## Trigger Conditions (Mandatory)

### Milestone Checklist

KPT is mandatory when any primary condition is met:

- [ ] M1: All planned deliverables of an epic or multi-issue task (3+ related Issues) are complete
   - Definition: "All phases" = all planned work items in planner decomposition, or all related GitHub Issues marked as closed
   - Example: Epic "Skill improvement" with 5 Issues → all 5 Issues closed = M1 met
- [ ] M2: A mechanism was created or removed (hook, skill, directory structure change)
- [ ] M3: A multi-session effort has concluded

If no primary condition is met, apply secondary scoring (execute if total >= 2 points):

- [ ] S1: User approval was required 2+ times (2 points)
- [ ] S2: Direction change or failure-based insight occurred (1 point)
- [ ] S3: Planner or inspector was invoked 1+ times (1 point)
- [ ] S4: 5+ files were modified (1 point)

### Session Boundaries

Even without a milestone, run a lightweight version (`--light`) at session boundaries.

## Execution Steps

### Step 1: Check Previous Try Execution

Load the most recent KPT file and verify execution status of previous Try items:
```bash
ls -t reports/*_kpt.md | head -1
```

**Judgment criteria** (select one per Try):

| Status | Condition | Evidence |
|--------|-----------|----------|
| **Complete** | Try action fully executed and Problem resolved | Git commit / closed Issue / feedback memory created |
| **Partial** | Try action partially executed or Problem only partially resolved | Partial commit / partial Issue completion |
| **Not Executed** | Try action was not attempted | No relevant commit / Issue not opened |
| **Ineffective** | Try was executed but Problem persists (triggers Five Whys) | Commit exists but recurrence detected |

### Step 2: Confirm Current Session Outcomes

- Review git log / GitHub Issues completion status
- Check user feedback (corrections, approvals)

### Step 3: Record KPT

Fill in the output format below.

### Step 4: Five Whys for Recurring Problems (if applicable)

**Trigger**: Run Five Whys only if BOTH conditions are met:
1. Same Problem ID (by title, not semantically similar) appears in 2+ consecutive KPTs
2. Associated Try from previous KPT was marked as "Complete" but Problem persists, OR Try was not executed

**Procedure**:
1. Why did the Problem occur? (current session evidence)
2. Why wasn't it resolved by the previous Try? (if Try was executed)
3. Why was the Try not executed / ineffective? (root cause level)
4. Identify systemic root cause (e.g., process ambiguity, skill definition gap, tooling limitation)
5. Draft feedback memory entry:
   - Format: use memory frontmatter (name, description, type: feedback, **Why:**, **How to apply:**)
   - File naming: `feedback_[brief-title].md`

**Non-trigger cases** (do NOT run Five Whys):
- First-time Problem (Recurrence Count = 1)
- Previous Try marked as "Not Executed" (indicates evaluation-phase problem, not implementation failure)

### Step 5: Save to File

Save to `reports/YYYY.MM.DD_kpt.md` (F006 mandatory).

## Modes

| Mode | Content |
|------|---------|
| `--light` | Minimum: 1 Keep, 1 Problem, 1 Try |
| `--full` (default) | All items + Five Whys check |
| `--analyze` | Analyze last 3 months of KPTs (recurring Problem detection + Try completion rate) |

## Acceptance Criteria per Item

Entries that fail these criteria must be rejected and rewritten:

### Keep Acceptance Criteria
- Must describe a reproducible behavior applicable across the project
- Record specific team-level actions, not personal impressions
- Fail example: "Things went well today" / "I felt productive"
- Pass example: "Consulted planner before task decomposition, resulting in 0 rework items"

### Problem Acceptance Criteria
- Must state the observed fact and its impact. No speculation or emotion
- Must include Recurrence Count (use "1" for first occurrence)
- Fail example: "Quality feels low somehow" / "Should have tried harder"
- Pass example: "F002 violation: leader directly edited a file (3rd recurrence). Root cause: failed to delegate to worker"

### Try Acceptance Criteria
- Must include Owner, Deadline, and Completion Verification Method
- Vague actions like "try harder", "be careful", "stay aware" are prohibited (not verifiable as actions)
- Fail example: "Be more careful next time" / "Do a better job"
- Pass example: "Add delegation checklist to leader agent definition (Owner: leader, Deadline: before next session start, Verification: checklist item exists in agent definition file)"

## Output Format

```markdown
# KPT Retrospective — YYYY-MM-DD

> Session summary: [one-line summary]
> Period: [start — end]
> KPT type: light / full
> Milestone trigger: [matching condition]

## Previous Try Execution Check

| Try | Previous Plan | Execution Status | Next Action |
|-----|--------------|-----------------|-------------|

## Keep (Continue)

| # | Behavior to Continue | Verification Method |
|---|---------------------|-------------------|

## Problem

| # | Issue | Location | First Seen | Recurrence Count |
|---|-------|----------|-----------|-----------------|

## Try (Improvement)

| # | Target Problem | Try Content | Owner | Deadline | Completion Check Date |
|---|---------------|-------------|-------|----------|--------------------|

## Five Whys (Recurring Problems Only)

(Include only when applicable)
```

## Subsequent Skills (Pipeline)

| Skill | Condition | Instruction |
|-------|-----------|-------------|
| `/session-start` | Next session start | Include previous Try execution check |
| `/empirical-prompt-tuning` | Problem root cause is skill definition ambiguity | Propose skill definition improvement |

> **Fallback**: Even if Problem count is 0, record at least 1 Keep and 1 Try.

**Additional Fallbacks**:
- Previous KPT file not found → run `git log --oneline -n 20` to review recent commits and reconstruct session context. Record "No previous KPT (first run)" in the Previous Try section
- git log returns 0 entries → record "No code changes" and conduct KPT based on documentation/configuration changes only
- Five Whys trigger judgment is ambiguous → report to the leader for decision. Do not self-decide to skip Five Whys

## Edge Case Handling

| Case | Action |
|------|--------|
| Previous KPT file not found | Run `ls -t reports/*_kpt.md` to verify. If 0 results, treat as "First KPT" and skip Step 1 |
| Previous and current Problem are similar but not identical | Record as separate Problems (Five Whys not applicable). If judgment is unclear, escalate to leader |
| Five Whys root cause points to skill definition gap | Propose new feedback memory creation to leader. Consider running /empirical-prompt-tuning |
| 5+ Problems exceed timebox | Record only top 3 by severity. Mark remaining as "Carried over to next session" |

## Prohibited Actions

- Concealing or downplaying Problems: record all observed facts. "Impact was small so I omitted it" is prohibited. Verification: cross-check that all user corrections and feedback during the session are reflected in the Problem table
- Recording a Problem without a Try: every Problem must have a corresponding Try entry. Verification: Problem table row count <= Try table row count
- Generic entries: vague Try items like "try harder", "be careful", or "stay aware" are prohibited. Try entries must always include Owner, Deadline, and Completion Verification Method. Verification: confirm all rows in the Try table have these three fields populated
