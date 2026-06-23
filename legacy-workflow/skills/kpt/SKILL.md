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

Run KPT (Keep / Problem / Try) retrospectives at session boundaries or milestone completions to drive continuous improvement. For recurring problems, conduct Five Whys root cause analysis.

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

### Clear Preparation Priority Rule

When it is confirmed during the current session that "clear will execute in the next session", KPT becomes mandatory regardless of milestone judgment. Specifically:

1. If milestone completion flag `workspace/in_progress/_clear_milestone.flag` exists → treat as KPT-required
2. If the leader directs "proceed with clear preparation" → KPT is the session's top priority

Execute KPT before session end when both conditions are met.

**Rationale**: The flag indicates the leader has pre-confirmed readiness for clear. KPT in this state satisfies "KPT at milestone completion" requirement.

### Carryover Detection (Unexecuted Try Chain)

When reviewing previous Try items (Step 1), check if any "Not Executed" item was also marked "Not Executed" in the prior KPT session.

- **First recurrence of unexecuted Try**: At the start of the current session, confirm priority with the leader. Escalate the Try to "Must Execute" status in the current KPT.
- **Second consecutive recurrence** (unexecuted Try appearing 2+ times): Trigger Five Whys immediately (treat as equivalent to recurring Problem with failed Try). Conduct structural analysis of the root cause: process ambiguity, unclear priority judgment, or undefined execution responsibility. Record findings in feedback memory for permanent improvement.

**Why**: To catch structural problems where the improvement effort itself carries over across multiple sessions, indicating deeper process breakdown.

### Mandatory Try Execution Timing

"Mandatory Try" refers to any KPT Try item explicitly marked with deadline "by next session start".

- **Unconditional execution rule**: Mandatory Try items must begin immediately after the next session starts, before any other task. Do not re-evaluate priority (mechanically avoids carryover due to judgment delay).
- **/session-start integration**: When `/session-start` executes, extract all Try items with deadline "by next session start" and present them as the session's top priority to the leader. Completion judgment must finish before addressing any user-directed task.
- **Non-execution consequence**: If a Mandatory Try is not addressed in the session, escalate it to Five Whys trigger in the next KPT (same treatment as above carryover detection rule). Analyze why the unconditional execution rule failed.

**Why**: To mechanically prevent multi-session carryover of improvement efforts, eliminating human re-prioritization delay.

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

#### Handling Multi-Session Carryover

After identifying the status of each previous Try item, check for "Not Executed" items that also appeared as "Not Executed" in the prior KPT session.

- **Single carryover**: Verify priority with the leader at session start. Re-enter as "Must Execute" in the current KPT.
- **Double carryover** (Not Executed for 2+ consecutive KPTs): Treat as Five Whys trigger. Perform root-cause analysis: Why was this improvement effort delayed across sessions? Record root cause in feedback memory: what structural issue (process ambiguity, unclear priority, undefined responsibility) allowed the improvement itself to slip?

**Rationale**: When an improvement effort carries over across multiple sessions, the root problem lies in process structure, not execution effort. Capture this pattern.

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

## Role Assignment for KPT (Core Judgments by Leader)

KPT execution authority is distributed as follows:

| Role | Responsibility | Notes |
|------|-----------------|-------|
| KPT draft creation (Keep/Problem/Try initial candidates) | Planner | Multi-perspective analysis (PM, architect, engineer) |
| Session achievement certification & finalization | Leader | Validates planner draft; confirms realized value & milestones |
| Keep/Problem selection & finalization | Leader | Decides which behaviors to continue and which problems to prioritize |
| Five Whys execution | Leader | Analyzes root cause of recurring Problems |
| Try definition & finalization | Leader | Receives planner's draft; confirms final remediation actions |
| KPT file formatting & storage | Worker | Transforms leader-approved content into file format; verifies prohibited symbols |
| Symbol verification (grep check) | Worker | Confirms 0 occurrences of prohibited terms/symbols |

**Background**: Delegating core KPT judgments to workers resulted in 3 consecutive quality issues. Root cause (Five Whys analysis): KPT judgment is a leader's retrospective responsibility, not a worker's transcription task. Planner provides multi-perspective input; leader owns the final decision.

## File Management (Split Threshold)

If a single KPT file grows too large, split to maintain readability:

- **Recommended split threshold**: 250 lines per file
- **Split method**: If the threshold is exceeded, create a new file with sequential naming: `reports/YYYY.MM.DD_kpt_2.md`
- **Owner**: The worker implementing the KPT should confirm file size with `wc -l` before submitting. If threshold is exceeded, propose split to the leader.
- **Cross-referencing**: When multiple KPT files exist for the same day, add "Previous KPT: {filename}" link at the top of the newer file to enable traceability.

**Why**: During a previous 3-session retrospective on 2026-05-12, accumulated KPT appends reached 260 lines, degrading readability.

## Prohibited Actions (Detailed)

- Concealing or downplaying Problems: record all observed facts. "Impact was small so I omitted it" is prohibited. Verification: cross-check that all user corrections and feedback during the session are reflected in the Problem table
- Recording a Problem without a Try: every Problem must have a corresponding Try entry. Verification: Problem table row count <= Try table row count
- Generic entries: vague Try items like "try harder", "be careful", or "stay aware" are prohibited. Try entries must always include Owner, Deadline, and Completion Verification Method. Verification: confirm all rows in the Try table have these three fields populated
- Reporting without execution evidence: "0 items found" or similar qualitative claims alone are insufficient. Report grep/API commands, exact counts, and matching lines as proof of verification

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
| `/session-start` | Next session start | Extract Mandatory Tries and present as session priority before any other user direction |
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
- Reporting without execution evidence: "0 items found" or similar qualitative claims alone are insufficient. Report grep/API commands, exact counts, and matching lines as proof of verification
- Unchecked symbols in output: KPT files distributed externally must pass symbol verification. Worker must run prohibited symbol check before delivery. For external-facing deliverables, use pattern: `grep -nP "[\x{2190}-\x{2BFF}\x{1F000}-\x{1FAFF}]" <file>` and confirm 0 matches. For internal working notes, emoji check only: `grep -nP "[\x{1F000}-\x{1FAFF}]" <file>` and confirm 0 matches.
