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

- After `/prd-generate` produces new findings that need to be integrated
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

## Integration with Existing Skills

| Existing Skill | Relationship |
|---------------|-------------|
| /prd-generate | Provides bulk findings that doc-update integrates |
| /build-knowledge | Point knowledge. doc-update handles systematic updates |
| /archive-output | Handles reports/ → knowledge/ promotion. doc-update handles knowledge/ maintenance |
| /legacy-analyze | Phase 3 updates maps. doc-update extends to all knowledge/ |

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

## Quality Checklist

- [ ] Version number incremented
- [ ] Last-updated date set to current
- [ ] Cross-references verified (no broken links)
- [ ] Audience-appropriate depth applied
- [ ] No modification proposals for application code
- [ ] Stale content flagged where applicable
