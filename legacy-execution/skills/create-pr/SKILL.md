---
name: create-pr
description: Manage the complete code change lifecycle in two phases. --plan generates change proposals from impact analysis; --exec creates PR from approved proposals. Human approval gates between phases.
argument-hint: --plan <impact analysis report path> [Phase number] | --exec <change proposal path> [repository name] [branch name]
---

# /create-pr Skill

> Part of [CLysis](https://github.com/t-hasuike/CLysis)
> Terminology: See `config/terminology.md` for role name customization

## Overview

Manages the complete code change lifecycle with explicit human approval gates:

1. **--plan phase**: Reads impact analysis report → generates detailed change proposals in diff format
2. **[Human Checkpoint]**: User reviews and approves proposed changes
3. **--exec phase**: Reads approved proposal → creates branch, applies changes, commits, pushes, and creates PR

This two-phase structure ensures human judgment gates all code modifications.

## Core Philosophy

> "AI proposes changes, humans review and approve, AI implements approved changes."

## Usage

```
/create-pr --plan <change-impact-report> [Phase]    # Generate change proposal
/create-pr --exec <change-proposal> [repo] [branch]   # Create PR from approved proposal
/create-pr <change-proposal> [repo] [branch]           # Legacy: --exec only (backward compatible)
```

## Roles and Responsibilities

| Role | Responsibility |
|------|-----------------|
| **Leader** | Approves team formation, monitors progress, ensures human checkpoints are honored |
| **Planner** | Task decomposition for large changes (10+ files) |
| **Worker** | --plan: Generate change proposals. --exec: Implement approved changes, create PR |
| **Inspector** | Post-PR audit: Code quality, compliance, hallucination detection |

## Investigation Target

$ARGUMENTS

---

## --plan Phase: Generate Change Proposals

### Purpose

Transform impact analysis results into concrete, diff-based change proposals that humans can review and approve.

### Execution Steps

#### Step 1: Read Impact Analysis Report

Extract from the specified report:
- High-impact areas (changes required)
- Medium-impact areas (verification needed)
- Implementation plan (Phase breakdown)

#### Step 2: Identify Target Phase

- If Phase specified in input: analyze only that Phase
- If not specified: default to Phase 0 (foundation setup)

#### Step 3: Identify Target Files

From the impact analysis report's high-impact areas, enumerate files that require modification.

#### Step 4: Retrieve Current Code

For each target file, use semantic code analysis (Serena) to:
- Get symbol overview
- Identify modification points:
  - Hardcoded locations (arrays, switch statements, magic numbers)
  - Dynamic retrieval locations
  - New additions needed
  - Refactoring targets

#### Step 5: Create Change Proposals

For each file, generate:

1. **Change Content (diff format)**: Show before/after code (see "Diff Generation Requirements" below)
2. **Change Reason**: Why this change is needed
3. **Impact Scope**: Ripple effects to other areas
4. **Test Strategy**: Unit/integration/manual approach

##### Diff Generation Requirements

**Unified diff format requirements**:
- Context lines: Always include +-3 lines before and after the modification point (for position identification during review)
- Line numbers: Include `@@ -start_line,count +start_line,count @@` headers
- File paths: Use `--- a/path/to/file` / `+++ b/path/to/file` format with paths relative to repository root

**3 Generation Patterns**:

| Pattern | Condition | Generation Method |
|---------|-----------|-------------------|
| Code verified (single location) | Target code retrieved via Serena/Read | Create unified diff manually from retrieved code. Use actual line numbers from the file |
| Multiple modification locations | Multiple modification points within the same file | Separate `@@` blocks per modification point. Ensure context lines between blocks do not overlap |
| New file creation | File does not exist | Use `--- /dev/null` / `+++ b/path/to/new/file` format. All lines are `+` lines |

**Verification Checklist (confirm after diff creation)**:
- [ ] Line numbers match the actual file's line numbers (not guessed)
- [ ] Context line code matches the actual file contents
- [ ] Indentation (tabs/spaces) matches the original file's style
- [ ] Before-modification code (`-` lines) exactly matches the existing code
- [ ] After-modification code (`+` lines) is syntactically correct

**Fallback**: If Serena is unresponsive or times out, retrieve the target code using Grep/Read tools and create the diff with equivalent accuracy. Note "Serena unresponsive; retrieved via Grep/Read" in the proposal's remarks section (not as comments within the diff).

#### Step 6: Organize Dependencies

Analyze dependencies between changes and determine implementation order:

```
Example:
1. Create Enum (prerequisite)
   |
2. Modify Service (uses Enum)
   |
3. Modify Controller (calls Service)
```

#### Step 7: Risk Analysis

For each change:

| Risk | Trigger Condition | Countermeasure |
|------|-------------------|----------------|
| Existing test failure | Callers not adapted to changes | Include test fix proposals |

### Output Format

Save to `reports/proposals/{feature_name}_{phase}.md`:

```markdown
# [Feature Name] Change Proposal - Phase X

**Created**: YYYY-MM-DD
**Target Repository**: [Repository name]
**Source Report**: `[Path to impact analysis report]`

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

[Display change in unified diff format]

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

(Repeat format for changes 2, 3, ...)

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

1. **User Approval**: Review and approve this change proposal
2. **Launch `/create-pr --exec`**: After approval, use this proposal as input to create PR
```

### Change History Template

After creating a change proposal, record change management using this template:

| Date | Change Description | Target File | Impact Scope | Executor | Notes |
|------|-------------------|-------------|-------------|----------|-------|
| YYYY-MM-DD | [Change summary] | [File path] | [Impact classification] | [Worker/Team] | [Notable items] |

### Approval Gate

**Human approval is required before proceeding to --exec phase.**

User must confirm:
- Proposed diffs are correct and appropriate
- Impact scope analysis is complete
- Test strategy is adequate
- Risk assessment is acceptable

Only after approval should the worker execute `/create-pr --exec`.

---

## --exec Phase: Implement Changes and Create PR

### Purpose

Apply the approved change proposal: create branch, modify code, commit, push, and create PR.

### Execution Steps

#### Step 1: Read Change Proposal

From the specified proposal file, extract:
- Change list (file paths, diffs)
- Change order (dependencies)
- Test strategy
- Risks and concerns

#### Step 2: Knowledge Reference and Approval Verification

**Knowledge Reference (if applicable)**:
- `workspace/in_progress/adr/` -- If an ADR (Architecture Decision Record) exists for this change, review it for inclusion in the PR description
- `workspace/in_progress/` -- If an implementation spec (SPEC) exists, verify alignment with the change proposal. Reference the SPEC path noted in the proposal

**Approval Confirmation Protocol**:

Verify that the change proposal has been approved by the user through the following procedure.

**Prohibited Actions (approval-related)**:

| ID | Prohibited Action | Reason |
|----|-------------------|--------|
| APR-01 | Execute --exec without a confirmed approval comment | Execution is prohibited if no explicit approval ("approved", "OK", "proceed", etc.) exists in session history or Discussion/Issue |
| APR-02 | Execute --exec without identifiable approval timestamp | If the timing of approval is unknown, the proposal may have been updated since. Verify the approval timestamp |
| APR-03 | Execute --exec with proposal version mismatch | If the proposal was modified after approval (file modification timestamp > approval timestamp), re-approval is required. Present changes to the user and obtain fresh approval |

**Approval Verification Checklist**:
- [ ] User's approval comment exists in session history or Discussion/Issue
- [ ] Approved proposal version (file path, creation date) matches the current proposal
- [ ] User has acknowledged and accepted high-risk items (from the proposal's "High Risk" section)

**Fallback (approval not confirmed)**: If approval cannot be confirmed, do not execute --exec. Report to the leader: "Cannot confirm change proposal approval; requesting user confirmation." Self-declaring "considered approved" is prohibited.

#### Step 3: Create Branch

```bash
cd {repository_path}
git checkout {base_branch}
git pull origin {base_branch}
git checkout -b {branch_name}
```

If branch name not provided, auto-generate:
```
feature/{feature_name}-phase{X}
```

#### Step 4: Apply Code Changes

From the change proposal's change list, apply each file modification following dependency order:

1. **Read existing file**: Get current code
2. **Apply diff**: Reflect changes
3. **Create new files**: When applicable

**Important**: Apply modifications in dependency order.

#### Step 5: Create Commits

Commit each change unit:

```bash
git add {modified_files}
git commit -m "$(cat <<'EOF'
{feature}: {change summary}

Why: {why this change is needed}
What: {what was changed}
How: {how it was implemented}

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

#### Step 6: Push

```bash
git push -u origin {branch_name}
```

#### Step 7: Create PR

Create PR using gh CLI:

```bash
gh pr create --title "{feature} [- Phase {X}]" --body "$(cat <<'EOF'
## Summary

### Decision
{Briefly describe the changes}

### Context
{Reason for change / business requirements}

---

## Background (ADR)
{If an Architecture Decision Record exists, link or summarize it. Otherwise "N/A"}

## Specification (SPEC)
{If an implementation spec exists, link or summarize it. Otherwise "N/A"}

---

## Changes

{Change summary for each file}

---

## Test Results

{Test execution results}

---

## Risks and Concerns

{Transfer risks and concerns from change proposal}

---

Generated with [Claude Code](https://claude.com/claude-code) + [CLysis](https://github.com/t-hasuike/CLysis)
EOF
)" --base {base_branch}
```

#### Step 8: Record Execution Log

Document execution to `reports/pr_logs/{feature_name}_{phase}.md`.

### Report Format

```markdown
## PR Creation Complete

- **Repository**: {repository name}
- **PR URL**: {PR URL}
- **Branch**: {branch name} → {base branch}

### Changes
- {File 1}: {Change summary}
- {File 2}: {Change summary}
- Commit Count: X commits

### Test Results
- Unit tests: PASS / FAIL
- Integration tests: PASS / FAIL

### Next Actions
Please review and approve the PR.

Execution log: `reports/pr_logs/{feature_name}_{phase}.md`
```

---

## Error Handling

### Branch Creation Failure
- **Cause**: Branch with same name already exists
- **Action**: Retry with datetime appended to branch name

### Code Modification Failure
- **Cause**: Diff application failed (code has changed, etc.)
- **Action**: Record details in execution log and report. Request manual modification if needed.

### PR Creation Failure
- **Cause**: gh CLI configuration issue
- **Action**: Verify authentication with `gh auth status`. Ask user to check settings.

## Prohibited Actions

| ID | Prohibited Action | Reason | Alternative |
|----|-------------------|--------|-------------|
| P001 | Create proposals without verifying actual code | Hallucination risk | Always verify code before proposing |
| P002 | Describe changes without diffs | Review difficulty | Always present diffs |
| P003 | Omit test strategy | Quality assurance impossible | Always include test strategy |
| P004 | Omit risks | Implementation problems | Identify and document risks |
| P005 | Auto-proceed from --plan to --exec | User must retain approval control | Always wait for explicit user approval |
| C001 | Create PR without approval | User approval required | Always confirm change proposal approval |
| C002 | Ignore dependency order | Incorrect implementation | Follow documented change order |
| C003 | Skip test execution | Quality assurance impossible | Run tests whenever possible |
| C004 | Ignore errors and continue | Inconsistency risk | Report immediately on error |
| C005 | Force push | History destruction risk | Use normal push only |

## Communication Style

Communicate in clear, business-appropriate language. Be explicit about successes and failures; avoid ambiguity.

---

## I/O Specification

### INPUT (--plan)
| Type | Description | Required/Optional | Example |
|------|-------------|-------------------|---------|
| Impact analysis report | Output file path from /change-impact | Required | `reports/impact_reports/add_feature.md` |
| Phase number | Target Phase for implementation | Optional (default: Phase 0) | `Phase 0`, `Phase 1` |
| Additional instructions | Focus instructions on specific areas | Optional | "ValidationService only" |

### INPUT (--exec)
| Type | Description | Required/Optional | Example |
|------|-------------|-------------------|---------|
| Change proposal | Proposal path from --plan (approved) | Required | `reports/proposals/add_feature_phase0.md` |
| Repository | Target repository name or path | Optional (infer from proposal) | `my-app`, `/path/to/repo` |
| Branch name | Branch name to create | Optional (auto-generate) | `feature/add-feature-phase0` |
| Base branch | Source branch name | Optional (default: develop) | `develop`, `main` |

### OUTPUT (--plan)
| Type | Format | Destination |
|------|--------|-------------|
| Change proposal | Diff format + reasoning, impact, test strategy | `reports/proposals/{feature}_{phase}.md` |

### OUTPUT (--exec)
| Type | Format | Destination |
|------|--------|-------------|
| PR URL | GitHub PR link | stdout (report to leader) |
| Execution log | Record of execution details | `reports/pr_logs/{feature}_{phase}.md` |

### Prerequisites
- **--plan**: Impact analysis report has been created (via /change-impact)
- **--exec**: Change proposal created and user-approved
- Target repository exists and write access is available
- gh CLI is configured and authenticated

### Downstream Skills (Pipeline)

| Skill | Condition | Instruction |
|-------|-----------|-------------|
| `/review-code` | After --exec PR creation completes | **Skipping `/review-code [PR number]` after PR creation is prohibited.** Report to leader and obtain approval before executing review |

> **Fallback**: If prerequisites are not met, report to the leader and await further instructions.

### Quality Checkpoints

#### For --plan
- [ ] All modification points have diffs
- [ ] Change reasons documented
- [ ] Impact scope analyzed
- [ ] Test strategy is specific
- [ ] Risks and side effects identified
- [ ] Dependencies organized
- [ ] Change order is appropriate

#### For --exec
- [ ] All modification files applied
- [ ] Commits follow 5W1H format
- [ ] PR body includes change summary, test results, risks
- [ ] Execution log recorded
- [ ] Test results verified

---

## Delegation Templates

When delegating this skill to workers, include role clarification.

### --plan Delegation

```
**Important: You are a worker (executor). You are not the leader.
Do not propose team formation or consult the planner.
Execute the change proposal creation yourself and report results.**

Target:
- Impact analysis report: {report_path}
- Target repository: {repository_name}

Rules:
- Present before/after code in diff format
- Include change reason, risks, and test strategy
- This proposal requires user approval before execution

Output: Save to reports/proposals/ (file persistence required)
```

### --exec Delegation

```
**Important: You are a worker (executor). You are not the leader.
Do not propose team formation or consult the planner.
Execute the PR creation yourself and report results.**

Target:
- Change proposal: {proposal_path} (user-approved)
- Target repository: {repository_name}

Rules:
- Apply changes following dependency order
- Commit messages must follow 5W1H format
- Include risks and test results in PR body
- Use default permission mode for GitHub operations (requires approval for push/PR)

Output: Save execution log to reports/pr_logs/ (file persistence required)
```

---

## Examples

### Example 1: --plan Phase

```
Input: reports/impact_reports/add_express_shipping.md, Phase 0
Output: reports/proposals/add_express_shipping_phase0.md
```

### Example 2: --exec Phase

```
Input: reports/proposals/add_express_shipping_phase0.md (approved)
Output: PR URL + reports/pr_logs/add_express_shipping_phase0.md
```

