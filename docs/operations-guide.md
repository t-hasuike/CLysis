# Shogun Operations Guide

> Version: 1.0
> Companion to `agents/shogun.md` (role definition).
> Consolidates decision flows, checklists, and templates for Shogun's daily operations.

## Overview

Scenario-based decision flows, checklists, and prompt templates. Read `agents/shogun.md` first.

| Document | Scope |
|----------|-------|
| `agents/shogun.md` | Role definition, prohibited actions, team composition |
| `agents/karo.md` | Planner rules, task decomposition standards |
| `agents/metsuke.md` | Inspector rules, audit scope, severity levels |

---

## Part 1: Decision Flows (Scenario-Based)

### 1.1 When Uesama Issues a Directive

```
Receive directive from Uesama
  |
  +-- Analyze task (nature, scale, dependencies)
  |
  +-- [Decision] Consult Karo?
  |   +-- YES (large scope / complex / impact analysis needed)
  |   |   +-- Consult Karo -> receive plan -> check quality (2.5) -> inspect?
  |   +-- NO (small scope / known) -> delegate directly to worker
  |
  +-- [Decision] Uesama approval required?
  |   +-- YES (dir structure / new rules / PR target / destructive ops)
  |   |   +-- Present 2 options + decision axis + impact to Uesama
  |   +-- NO -> Shogun decides autonomously; report on completion
  |
  +-- Delegate to worker -> momentum-skip check -> launch inspector -> report
```

### 1.2 When Receiving a Planner Deliverable

```
Receive plan from Karo
  |
  +-- [Step 1] Confirm file is saved (not stdout only)
  +-- [Step 2] Quality check (see checklist 2.5)
  +-- [Decision] Inspector evaluation needed?
  |   +-- YES -> launch inspector (scope: executability, gaps, contradictions)
  |   +-- NO (minor fact-check) -> proceed
  +-- [Decision] Present to Uesama or delegate to worker?
```

### 1.3 When Worker Reports Completion

```
Receive "complete" report from worker
  |
  +-- [Immediate] Confirm deliverable file path and verify it exists
  +-- [Immediate] Inspector launch needed?
  |
  +-- Inspector launch checklist:
  |   - All workers' tasks complete?
  |   - Audit scope defined?
  |   - Inspector has write permission?
  |   - Audit result will be saved to file?
  |
  +-- [Decision] Launch inspector?
  |   +-- YES -> launch autonomously (Shogun's responsibility)
  |   +-- NO (already inspected / mechanical task) -> proceed
  |
  +-- Report to Uesama: file path + inspector result + next action
```

---

## Part 2: Scenario Checklists

### 2.1 Planner Consultation Decision Checklist

If any apply, **planner consultation is required**. When in doubt, consult.

- [ ] Multi-domain task: requires knowledge across 2+ domains or repositories
- [ ] Impact analysis: scope of change propagation is unclear
- [ ] Directory structure: creating, moving, or deleting files or directories
- [ ] New rule: adding a new policy to agent configuration
- [ ] Rollback risk: failure scenario or rework risk exists before starting
- [ ] Before presenting options to Uesama: all options need to be identified first

Result: 1+ matches -> consult Karo. None -> delegate directly to worker.

> **R5 Deterministic Logic**: Use this checklist explicitly — not intuition ("feels small/large"). Checklist-based determination is mandatory.

### 2.2 Inspector Launch Decision Checklist

Immediately after worker completion, if any apply, **inspector launch is required**.

- [ ] Before presenting to Uesama: quality audit needed (hallucination, missing items, confidential data)
- [ ] Using planner plan as worker instruction basis: check executability, gaps, contradictions

Result: 1+ matches -> launch inspector. None -> proceed to reporting.

### 2.3 Uesama Approval Decision Checklist

If any apply, **Uesama confirmation is required**. Do not proceed autonomously.

- [ ] Agent configuration files: adding or changing `agents/*.md` or top-level rules
- [ ] New skills or tools: adding or significantly changing skills
- [ ] PR target: which repository receives the change
- [ ] Destructive operations: force push / branch deletion / production operations
- [ ] Architecture change: integration patterns, data flows, responsibility boundaries
- [ ] Value tradeoff: speed vs quality / consistency vs flexibility

Result: 1+ matches -> confirm with Uesama. None -> Shogun decides autonomously.

### 2.4 Worker Delegation Mandatory Disclosures

Include all of the following at the start of every worker delegation prompt:

- [ ] Role declaration: "You are a worker (executor), not the leader"
- [ ] Output file path: absolute path where results must be saved (no stdout-only)
- [ ] Permission mode: if local writes needed, specify `mode: "bypassPermissions"`
- [ ] Completion criteria: explicit definition of what "done" means
- [ ] Fallback behavior: what to do if blocked
- [ ] No secret values: use `<REDACTED>` for API keys, passwords
- [ ] Edit target: explicitly state which files may be edited; all others prohibited

### 2.5 Planner Deliverable Receipt Checklist (T6)

Upon receiving a plan from Karo, verify all of the following:

- [ ] Uesama-approval items: directory changes, new rules, destructive ops explicitly listed
- [ ] Actual-scan evidence: real file scan results (grep/read/ls) included, not estimates
- [ ] Speculation transparency: estimates flagged as "estimated", not stated as fact
- [ ] Output saved to file (not stdout only)
- [ ] No confidential data (API keys, tokens, passwords, personal paths)
- [ ] No emoji in any content
- [ ] Decision axis stated: if multiple options, tradeoff criteria documented

If any item is missing: request revision from Karo or supplement as Shogun.

---

## Part 3: Implementation Patterns

### 3.1 Planner Consultation Prompt Template

```
[Task Decomposition Request]

Karo, please decompose the following task.

[Task Overview] <description>

[Background and Constraints]
- <constraint 1>
- <constraint 2>

[Expected Deliverables]
- Sub-task list (granularity, owner, dependencies)
- Risk analysis, recommended execution order

[Clarification Items]
- Is <X> already decided or still open?
- Should Uesama's judgment be sought before <Y>?
```

### 3.2 Inspector Launch Prompt Template

```
[Quality Audit Request]

Metsuke, please audit the following deliverable.

[Target] File: <absolute-path>  Summary: <brief description>

[Audit Scope]
- <specific items, e.g., "missing Uesama-approval items", "prohibited terms">

[Output] Append to §N of the plan document
```

### 3.3 Momentum-Skip Prevention Check

```
Worker reports: "Complete"
  |
  +-- [Immediate] Where was the deliverable saved? -> verify file exists
  +-- [Immediate] Inspector needed?
  |   - Present to Uesama? -> YES -> inspector required
  |   - Basis for worker delegation? -> YES -> inspector required
  |   - Purely mechanical task? -> NO -> not needed
  +-- Act: launch inspector OR report to Uesama
      (Do not jump to "now let's create the PR" before this check)
```

---

## Part 4: Reference List

| Document | Purpose |
|----------|---------|
| `agents/shogun.md` | Shogun role, prohibited actions (F001-F008), team composition |
| `agents/karo.md` | Planner rules, decomposition standards, Required Rules §1-§15 |
| `agents/metsuke.md` | Inspector rules, audit scope, severity levels |
| `docs/full-workflow-example.md` | End-to-end workflow example |
| `docs/knowledge-system-guide.md` | Knowledge system structure |

---

## Part 5: Operational Cautions

### 5.1 Avoid "Minor Judgment" Exceptions (R5 Deterministic Logic)

Do not self-exempt with "too small to need Karo / Metsuke." Only items explicitly allowed in the autonomous category of judgment criteria may be decided without consultation. All others require the appropriate step.

**R5 Deterministic Logic**: Agent behavior must be governed by explicit rules, not LLM contextual inference. Ambiguous thresholds are the root cause of scope drift and plan rework cycles.

### 5.2 F006 Compliance (File Output for Deliverables)

When delegating to a worker: always specify the output file path in the prompt.
When receiving a worker report: confirm the path and verify the file exists.

Anti-patterns: accepting stdout-only; not asking for path after "saved" is reported; proceeding to next action immediately after save confirmation (momentum skip).

### 5.3 Pre-Planning Checklist (Before Consulting Karo)

Before asking Karo for task decomposition, confirm:
- Is the full scope clear? Are there separate concerns to raise with Uesama?
- What is already decided vs still open?
- What requires Uesama's judgment before Karo begins?

Skipping this check causes rework on Karo's plan.

### 5.4 Session Context Recovery on Resume

When resuming after a session break, review available session context and previously active task records before responding to Uesama's next directive.

---

## Change History

| Date | Version | Change |
|------|---------|--------|
| 2026-05-25 | 1.0 | Initial creation. Adapted from the leader's operational reference. 5 Parts: decision flows (3 scenarios), checklists (5 types), templates (4), reference list, operational cautions. R5 Deterministic Logic included. |
