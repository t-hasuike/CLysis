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

- [ ] M1: All phases of an epic or multi-issue task are complete
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

### Step 2: Confirm Current Session Outcomes

- Review git log / GitHub Issues completion status
- Check user feedback (corrections, approvals)

### Step 3: Record KPT

Fill in the output format below.

### Step 4: Five Whys for Recurring Problems

If the same Problem appeared in the previous KPT (2nd+ occurrence), run Five Whys:

1. Why did the Problem occur?
2. Why wasn't it resolved by the previous Try?
3. Why was the Try not executed / ineffective?
4. Identify root cause
5. Draft a feedback memory entry for persistent storage

### Step 5: Save to File

Save to `reports/YYYY.MM.DD_kpt.md` (F006 mandatory).

## Modes

| Mode | Content |
|------|---------|
| `--light` | Minimum: 1 Keep, 1 Problem, 1 Try |
| `--full` (default) | All items + Five Whys check |
| `--analyze` | Analyze last 3 months of KPTs (recurring Problem detection + Try completion rate) |

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

## Prohibited Actions

- Concealing or downplaying Problems
- Recording a Problem without a Try (always include an improvement plan)
- Generic entries (vague Try items like "try harder" are prohibited)
