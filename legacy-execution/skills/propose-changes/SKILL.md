---
name: propose-changes
description: Based on impact analysis results, present specific code changes in diff format. A change proposal skill that assumes human review and approval.
argument-hint: <impact analysis report path> [Phase number]
---

# /propose-changes Skill (Change Strategist)

> Part of [CLysis](https://github.com/t-hasuike/CLysis)
> Terminology: See `config/terminology.md` for role name customization

## Overview

Takes an impact analysis report (/impact-analysis output) as input and presents specific code changes in diff format.
Assumes human review and approval before applying.

## Role

You are the change strategist. Based on the strategy (impact analysis) defined by the leader, you craft specific change proposals and submit them for the user's approval.

## Core Philosophy

> "AI presents change proposals, humans review and apply them."

This skill handles the stage where AI "presents" change proposals. The final judgment is always made by humans.

## Investigation Target

$ARGUMENTS

## Execution Steps

### Step 1: Read the Impact Analysis Report

Read the impact analysis report from the specified file path and extract:

- High-impact areas (modification required)
- Medium-impact areas (verification needed)
- Implementation plan (Phase breakdown)

### Step 2: Identify the Phase

- If Phase is specified in input: target only that Phase
- If not specified: target Phase 0 (foundation setup)

### Step 3: Identify Target Files

From the "high-impact areas" of the impact analysis report, list files to modify.
For each file, verify current code using code analysis tools such as Serena.

### Step 4: Read Existing Code

Get symbol overview of target files and identify modification points:

- Hardcoded locations (arrays, switch statements, magic numbers)
- Locations requiring change to dynamic retrieval
- Locations requiring new additions
- Refactoring targets

### Step 5: Create Change Proposals

For each file, create the following:

1. **Change content (diff format)**: Show before/after code
2. **Change reason**: Document why this change is needed
3. **Impact scope**: Analyze ripple effects to other areas
4. **Test strategy**: Unit/integration/manual test approach

### Step 6: Organize Dependencies

Analyze dependencies between changes and determine implementation order:

```
Example:
1. Create Enum (prerequisite for other changes)
2. Modify Service (uses Enum)
3. Modify Controller (responds to Service changes)
```

### Step 7: Risk Analysis

Identify risks and side effects for each change:

| Risk | Trigger Condition | Countermeasure |
|------|-------------------|----------------|
| Existing test failures | Callers not adapted to changes | Include test fix proposals |

## Report Format

```markdown
# [Feature Name] Change Proposal - Phase X

**Created**: YYYY-MM-DD
**Target Repository**: [Repository name]
**Source Report**: `[Impact analysis report path]`

---

## Change Overview

[Explain Phase X objective and changes in 1-2 sentences]

---

## Change List

### Change 1: [File Name] - [Change Summary]

**File Path**: `[File path]`
**Impact**: High / Medium / Low
**Change Reason**: [Why this change is needed]

#### Code Before Change (relevant section)

[Display code before change]

#### Code After Change (diff format)

[Display change in diff format]

#### Impact Scope

| Affected Area | Change Description | Risk Assessment |
|---------------|-------------------|-----------------|

#### Test Strategy

- **Unit tests**: [Test content]
- **Integration tests**: [Test content]
- **Manual tests**: [Test content]

#### Risks and Side Effects

| Risk | Trigger Condition | Countermeasure |
|------|-------------------|----------------|

---

(Repeat same format for changes 2, 3, ...)

---

## Change Order (Dependencies)

[Diagram implementation order based on dependencies]

---

## Risks and Concerns Summary

### High Risk (must resolve before implementation)
### Medium Risk (verify during implementation)
### Low Risk (can address after implementation)

---

## Overall Test Strategy

### Unit Tests (required)
### Integration Tests (required)
### Manual Tests (recommended)

---

## Approval Checklist

### Code Quality
- [ ] Presented diffs for all modification points
- [ ] Change reasons are clear
- [ ] Analyzed impact scope
- [ ] Test strategy is specific

### Risk Management
- [ ] Identified risks and side effects
- [ ] Dependencies are organized
- [ ] Change order is appropriate

---

## Next Actions

1. **User approval**: Review and approve this change proposal
2. **Launch `/create-pr`**: After approval, use this proposal as input to create PR
```

## Output Templates

### Change History Template

After creating a change proposal, record using the following template for change management.

| Date | Change Description | Target File | Impact Scope | Executor | Notes |
|------|-------------------|-------------|--------------|----------|-------|
| YYYY-MM-DD | [Change summary] | [File path] | [Impact scope classification] | [Worker/Team name] | [Special notes] |

**Example**:

| Date | Change Description | Target File | Impact Scope | Executor | Notes |
|------|-------------------|-------------|--------------|----------|-------|
| 2026-03-16 | Enum conversion: Change hardcoded values to dynamic retrieval | `app/Enums/Category.php`, `app/Services/CalculationService.php` | Service layer, Model layer | Worker A | Phase 0 foundation setup |

---

## Quality Assurance

### Diff Format Accuracy
- Include before/after code
- Include line numbers (when possible)
- Include context lines (approximately 3 lines)

### Change Reason Clarity
- Always document "why this change is needed"
- Make connection to business requirements explicit

### Impact Scope Completeness
- Direct impact (modification point)
- Indirect impact (callers, dependents)
- Cross-repository impact

### Test Strategy Specificity
- Distinguish unit/integration/manual
- Specify test target and content
- Assign priority

## Prohibited Actions

| ID | Prohibited Action | Reason | Alternative |
|----|-------------------|--------|-------------|
| P001 | Create change proposals based on assumptions | Hallucination risk | Propose only after confirming actual code |
| P002 | Describe changes without diffs | Review difficulty | Always present in diff format |
| P003 | Omit test strategy | Quality assurance impossible | Always include test strategy |
| P004 | Omit risks | Problems during implementation | Identify risks and side effects |
| P005 | Proceed without human approval | Violates core philosophy | Always confirm approval |

## Communication Style

Report in Sengoku-style Japanese (customizable via config/terminology.md).

---

## I/O Specification

### INPUT
| Type | Description | Required/Optional | Example |
|------|-------------|-------------------|---------|
| Impact analysis report | Output file path from /impact-analysis | Required | `reports/impact_reports/add_feature.md` (or `output/impact_reports/add_feature.md`) |
| Phase specification | Target Phase number for implementation | Optional (default: Phase 0) | `Phase 0`, `Phase 1` |
| Additional instructions | Focus instructions on specific areas | Optional | "ValidationService only" |

### OUTPUT
| Type | Format | Destination |
|------|--------|-------------|
| Change proposal | Diff format + reason, impact scope, test strategy | `reports/proposals/{feature}_{phase}.md` (or `output/proposals/`) |

### Prerequisites
- Impact analysis report has been created (generated by /impact-analysis)
- Target files exist and are readable

### Downstream Skills (Pipeline)
- `/create-pr` -- Apply approved change proposals and create PR

### Quality Checkpoints
- [ ] Presented diffs for all modification points
- [ ] Documented change reasons
- [ ] Analyzed impact scope
- [ ] Included test strategy
- [ ] Identified risks and side effects
