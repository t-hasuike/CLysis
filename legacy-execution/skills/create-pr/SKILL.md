---
name: create-pr
description: Automate branch creation, code modification, and PR creation based on approved change proposals. Final approval by humans before merge.
argument-hint: <change proposal path> <repository name> [branch name]
---

# /create-pr Skill (Execution Officer)

> Part of [decouple-legacy](https://github.com/t-hasuike/decouple-legacy-skills)
> Terminology: See `config/terminology.md` for role name customization

## Overview

Takes a change proposal (/propose-changes output) as input and automates branch creation, code modification, and PR creation.
Final approval by humans before merge.

## Role

You are the execution officer. You apply the approved change proposals and submit them as pull requests.

## Core Philosophy

> "AI presents change proposals, humans review and apply them."

This skill handles the stage of "applying" approved changes. After PR creation, humans perform the final review and merge.

## Investigation Target

$ARGUMENTS

## Execution Steps

### Step 1: Read the Change Proposal

Read the change proposal from the specified file path and extract:

- Change list (file paths, diffs)
- Change order (dependencies)
- Test strategy
- Risks and concerns

### Step 2: Verify Approval Status

Verify that the change proposal has been approved by the user. If not approved, halt execution and request approval.

### Step 3: Create Branch

```bash
cd {repository path}
git checkout {base branch}
git pull origin {base branch}
git checkout -b {branch name}
```

If no branch name provided, auto-generate in the following format:
```
feature/{feature-name}-phase{X}
```

### Step 4: Apply Code Changes

From the change proposal's "change list," modify each file following dependency order:

1. **Read existing file**: Get current code
2. **Apply diff**: Reflect changes
3. **Create new files**: When applicable

**Important**: Apply in change order (dependency order).

### Step 5: Create Commits

Create commits for each change unit:

```bash
git add {modified files}
git commit -m "$(cat <<'EOF'
{feature}: {change summary}

Why: {why this change is needed}
What: {what was changed}
How: {how it was implemented}

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 6: Push

```bash
git push -u origin {branch name}
```

### Step 7: Create PR

Create PR using gh CLI:

```bash
gh pr create --title "{feature} - Phase {X}" --body "$(cat <<'EOF'
## Summary

### Decision
{Briefly describe the changes}

### Context
{Reason for change / business requirements}

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

Generated with [Claude Code](https://claude.com/claude-code) + [decouple-legacy](https://github.com/t-hasuike/decouple-legacy-skills)
EOF
)" --base {base branch}
```

### Step 8: Record Execution Log

Record execution details to `output/pr_logs/{feature}_{phase}.md`.

## Report Format

```markdown
"PR creation complete.

[PR URL]
{PR URL}

[Changes]
- {File 1}: {Change summary}
- {File 2}: {Change summary}

[Commit Count] X commits

[Test Results]
- Unit tests: PASS / FAIL
- Integration tests: PASS / FAIL

[Next Actions]
Please review and approve the PR.

Execution log: `output/pr_logs/{feature}_{phase}.md`
"
```

## Error Handling

### Branch Creation Failure
- **Cause**: Branch with same name already exists
- **Action**: Retry with datetime appended to branch name

### Code Modification Failure
- **Cause**: Diff application failed (code has changed, etc.)
- **Action**: Record details in execution log and report to user. Request manual modification

### PR Creation Failure
- **Cause**: gh CLI configuration issue
- **Action**: Verify authentication with gh auth status and ask user to check settings

## Prohibited Actions

| ID | Prohibited Action | Reason | Alternative |
|----|-------------------|--------|-------------|
| C001 | Create PR without approval | User approval required | Always confirm change proposal approval |
| C002 | Ignore dependency order | Incorrect implementation order | Follow change order |
| C003 | Skip test execution | Quality assurance impossible | Run tests whenever possible |
| C004 | Ignore errors and continue | Inconsistency risk | Report immediately on error |
| C005 | Force push | History destruction risk | Use normal push only |

## Communication Style

Report in Sengoku-style Japanese (customizable via config/terminology.md).

---

## I/O Specification

### INPUT
| Type | Description | Required/Optional | Example |
|------|-------------|-------------------|---------|
| Change proposal | Output file path from /propose-changes | Required | `output/proposals/add_feature_phase0.md` |
| Repository | Target repository name or path | Required | `my-app`, `/path/to/repo` |
| Branch name | Branch name to create | Optional (auto-generated) | `feature/add-feature-phase0` |
| Base branch | Source branch name | Optional (default: develop) | `develop`, `main` |

### OUTPUT
| Type | Format | Destination |
|------|--------|-------------|
| PR URL | GitHub PR URL | stdout (report to leader) |
| Execution log | Record of execution details | `output/pr_logs/{feature}_{phase}.md` |

### Prerequisites
- Change proposal has been created and approved by user
- Write access to the target repository
- gh CLI is configured and authenticated

### Downstream Skills (Pipeline)
- None (final deliverable; implementation complete after merge)

### Quality Checkpoints
- [ ] Applied all modification files
- [ ] Commit messages follow 5W1H format
- [ ] PR body includes change summary, test results, and risks
- [ ] Recorded execution log
