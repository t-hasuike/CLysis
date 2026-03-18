---
name: code-review
description: Systematically review PR code quality and business perspective, providing approval judgment material.
argument-hint: <PR number> [repository name] [review focus]
---

> This is a generic skill from [decouple-legacy](https://github.com/t-hasuike/decouple-legacy-skills).
> Terminology can be customized via `config/terminology.md`.

# PR Review Skill

## Overview

Systematically review pull request code quality and business perspective, providing approval judgment material.

See config/terminology.md for term customization

## Review Target

$ARGUMENTS

## Review Flow

```
1. Get PR information (changed files, diff retrieval)
   |
2. Reference domain knowledge (input/domain/ + input/staging/in_progress/)
   |
3. Code quality review
   |
4. Business perspective review
   |
5. Overall evaluation and approval judgment
```

## Investigation Procedure

### Step 1: Get PR Information
- Retrieve PR overview, changed files, and diffs using GitHub MCP tool
- Determine team composition based on number of changed files

### Step 2: Reference Domain Knowledge
- Check related domain knowledge in `input/domain/`
- Reference task specification and impact analysis reports in `input/staging/in_progress/`
- Understand business rules related to the changes

### Step 3: Code Quality Review
- Implementation quality of changed symbols (structure, patterns, error handling)
- Consistency with existing code
- Security and performance concerns

### Step 4: Business Perspective Review
- Requirements alignment verification (cross-reference with impact analysis report)
- Domain knowledge alignment verification
- Impact scope appropriateness verification
- Test case coverage (from business scenario perspective)

### Step 5: Overall Evaluation
- Approval judgment (Approved / Conditional Approval / Changes Required)
- Present next actions

## Team Composition Patterns

| PR Scale | Changed Files | Team Composition | Notes |
|----------|--------------|-----------------|-------|
| Small | ~5 files | 2 workers (code quality + business perspective) | Task tool acceptable |
| Medium | 6-20 files | 3 workers (quality + business + test perspective) | Team members recommended |
| Large | 20+ files | Consult planner -> form team | Divide by domain area |

**Important**: Leader does not review directly; always delegate to workers (F002)

## Output Format

```markdown
# PR#[Number] Review Report

**PR**: [Title]
**Repository**: [Target repository (each repository if multiple)]
**Review Date**: YYYY-MM-DD

---

## 1. PR Overview

### Change Description
[Describe PR purpose and overview in 1-2 sentences]

### Changed File List
| File Path | Change Type | Lines |
|-----------|-----------|-------|
| xxx.php | Addition | +50 |

---

## 2. Code Quality Review

### [Pass] Positive Points
- [Include specific file:line numbers]

### [Warning] Improvement Suggestions
| Location | Description | Priority | Improvement Proposal |
|----------|-------------|----------|---------------------|
| xxx.php:45 | ... | High | ... |

### [NG] Required Fixes
| Location | Description | Reason |
|----------|-------------|--------|
| xxx.php:78 | ... | ... |

---

## 3. Business Perspective Review

### Requirements Alignment
| Requirement Item | Implementation Status | Judgment | Notes |
|-----------------|---------------------|----------|-------|
| xxx feature | OK | OK | ... |

### Domain Knowledge Alignment
**Referenced Domain Knowledge**:
- `input/domain/xxx.md`
- `input/staging/in_progress/yyy.md`

| Item | Domain Knowledge | Implementation | Judgment |
|------|-----------------|---------------|----------|
| xxx | ... | ... | OK |

---

## 4. Test Perspective

### Test Case Appropriateness
| Test Case | Judgment | Notes |
|-----------|----------|-------|
| xxx | OK | ... |

---

## 5. Overall Evaluation

### Approval Judgment
- **Approved** / **Conditional Approval** / **Changes Required**

### Reason
[State judgment reason]

### Next Actions
- [ ] [Assignee]: [Task description]
```

## Quality Checks

Upon review completion, verify the following:

- [ ] Reviewed all changed files in the PR
- [ ] Referenced domain knowledge (input/domain/ + staging/in_progress/)
- [ ] Reviewed both code quality and business perspective
- [ ] Included file path:line numbers
- [ ] Approval judgment is clear

---

## I/O Specification

### INPUT
| Type | Description | Required/Optional | Example |
|------|-------------|-------------------|---------|
| PR number | PR number to review | Required | `12345` |
| Repository | Target repository | Optional | `backend`, `frontend` |
| Review focus | Specify particular focus | Optional | `security`, `performance`, `business` |

### OUTPUT
| Type | Format | Destination |
|------|--------|-------------|
| PR review report | Detailed Markdown (code quality + business perspective + approval judgment) | stdout (report to leader) |

### Prerequisites
- GitHub MCP is available
- Serena MCP is running (for code reading)
- input/domain/ and input/staging/ are accessible

### Downstream Skills (Pipeline)
- None (final deliverable; judgment material for approval/change request)

### Quality Checkpoints
- [ ] Reviewed all changed files
- [ ] Verified alignment with domain knowledge
- [ ] Covered code quality, business perspective, and test perspective
- [ ] Approval judgment is clear (Approved/Conditional Approval/Changes Required)
- [ ] Included file path:line numbers
