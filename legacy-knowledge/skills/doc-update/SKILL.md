---
name: doc-update
description: Update knowledge documents for target audience. Adjusts depth, adds context, and maintains documents as living documentation.
argument-hint: "[target-audience: developer | pm | onboarding] [scope: file-path | directory]"
---

# /doc-update -- Document Update & Audience Adaptation Skill

> This is a generic skill from [CLysis](https://github.com/t-hasuike/CLysis).
> Terminology can be customized via `config/terminology.md`.

## Overview

Update existing knowledge documents to match the needs of a specific audience. Maintains documents as living documentation by comparing current code state against documented state and updating accordingly.

## When to Use

- After `/current-prd` produces new findings that need to be integrated
- When onboarding a new team member (generate audience-appropriate docs)
- Periodic document freshness checks
- When code changes make existing documentation outdated

## Target Audiences

| Audience | Depth | Focus |
|---------|-------|-------|
| `developer` | Deep (code-level) | Implementation details, API contracts, database schemas, gotchas |
| `pm` | Medium (feature-level) | Business rules, user flows, feature boundaries, constraints |
| `onboarding` | Progressive (guided) | Start with overview, link to details. "Read this first" ordering |

## Workflow

### Step 1: Current State Assessment

1. Read the target knowledge file(s)
2. Check version/last-updated date
3. Compare against current codebase (use Serena for symbol verification)
4. Identify gaps: documented but changed, exists but undocumented, documented but removed

**Specific execution methods**:
- Version check: Check first 10 lines of file for `Version:` and `Last Updated:`
- Staleness detection: If Last Updated is 30+ days old, flag as `[NEEDS VERIFICATION]` candidate
- Code comparison: Use Serena `find_symbol` to verify existence of classes/methods documented in the file
  - **Fallback**: If Serena is unresponsive, use `grep -rn '[class/method name]' app/` as alternative search. If 0 results, report "symbol not found" and request confirmation
  - **Prohibition**: Do not delete from documents without existence verification. Deletion candidates must be backed by grep evidence, and reasoning must be noted in version history
- Gap classification: Categorize into "documented but changed", "exists but undocumented", "documented but removed"

### Step 2: Audience Adaptation

Based on target audience, adjust:

- **Level of detail**: developer gets code paths, PM gets business rules
- **Terminology**: developer uses class/method names, PM uses feature names
- **Examples**: developer gets code snippets, PM gets user scenarios
- **Navigation**: onboarding gets "read next" links, developer gets API reference

### Step 3: Update & Report

1. Update the target file(s) with new/corrected information
2. Maintain version history in the file
3. Report changes to the user (what was added, removed, corrected)

## Living Document Rules

- Every update increments the version number
- Last-updated date is always current
- Removed content is noted in version history (not silently deleted)
- Cross-references to other knowledge files are verified on each update
- Stale content (>30 days without verification) is flagged with `[NEEDS VERIFICATION]`

## Output Rules

- Update `knowledge/` files directly (this skill is authorized to modify knowledge/)
- State observations only. No modification proposals for application code
- Subject-first rule: always specify "whose/what's" for domain terms

**Strict F002 compliance**: Leader does not personally update knowledge/. Delegate execution to workers.

### Observation vs Modification Proposal Judgment Criteria

| Allowed (Observation) | Prohibited (Modification Proposal) | Judgment Rule |
|----------------------|-----------------------------------|---------------|
| "Method A is called from 3 locations" | "Method A should be split" | "X is Y" (state description) is allowed. "X should Y" (action directive) is prohibited |
| "Column X has been deprecated" | "Column X should be fully removed" | Factual recording is allowed. Modification instructions are prohibited |
| "No index is being used" | "An index should be created" | Problem identification is allowed. Modification instructions are prohibited |

**Self-check**: Verify with grep that the file contains no "should be", "needs to be", "must be changed to" directives

### Language and Tone

Clear, professional reporting with business etiquette. Clearly state OK/NG, explicitly state what is unclear.

### Verification Flow

1. After update, increment Version number and set Last Updated to current date
2. Verify all @reference links in the file are valid using grep
3. After completion, always run `/doc-check` to request quality audit

### Edge Case Handling

| Case | Action |
|------|--------|
| Target file does not exist | Report to leader. Request guidance on post-deletion handling |
| Reference link is broken | Fix the link and note in version history |
| Update conflicts with CLAUDE.md rules | Suspend the update and report to leader |

## Integration with Existing Skills

| Existing Skill | Relationship |
|---------------|-------------|
| `/current-spec` | Provides bulk findings that doc-update integrates |
| `/doc-organize` | Handles reports/ → knowledge/ promotion. doc-update handles knowledge/ maintenance |
| `/doc-check` | Diagnoses issues. doc-update executes fixes |

## I/O Specification

### INPUT
| Type | Content | Required |
|------|---------|----------|
| Target audience | `developer`, `pm`, or `onboarding` | Required |
| Scope | File path or directory within knowledge/ | Optional (default: all knowledge/) |

### OUTPUT
| Type | Format | Destination |
|------|--------|-------------|
| Updated documents | Markdown (in-place update) | `knowledge/` (direct modification) |
| Change report | Markdown (diff summary) | stdout (session report) |

### Downstream Skills (Pipeline)
| Skill | Condition |
|--------|-----------|
| `/doc-check` | **Skipping `/doc-check` after update is prohibited.** Report to leader and obtain approval before executing |

> **Fallback**: If prerequisites are not met, report to leader and await further instructions

## Quality Checklist

- [ ] Version number incremented: verify +1 increment via `git diff`
- [ ] Last-updated date set to current: visually confirm `Last Updated:` in file header matches today's date
- [ ] Cross-references verified: confirm all link paths in the file exist via `ls`, no broken links
- [ ] Audience-appropriate depth applied: visually review that terminology and detail level match target audience (developer/pm/onboarding)
- [ ] No modification proposals: grep the file for "should be", "needs to be", "must be changed" and confirm zero matches
- [ ] Stale content flagged: grep for sections where `Last Updated` is 30+ days old and confirm `[NEEDS VERIFICATION]` tag is present
