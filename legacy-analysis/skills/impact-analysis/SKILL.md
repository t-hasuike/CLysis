---
name: impact-analysis
description: Systematically investigate the impact scope when adding new features or changing specifications, and create an impact analysis report. Used in combination with service specification summaries.
argument-hint: <description of the change>
---

> This is a generic skill from [CLysis](https://github.com/t-hasuike/CLysis).
> Terminology can be customized via `config/terminology.md`.

# Impact Analysis Skill

## Overview

Systematically investigate the impact scope when adding new features or changing specifications, and create a report.

See config/terminology.md for term customization

## Investigation Target

$ARGUMENTS

## Investigation Flow

```
1. Organize change overview
   |
2. Identify impact scope (file and table list)
   |
3. Classify impact severity (High/Medium/Low)
   |
4. Detailed investigation of high-impact areas (Service specification summary)
   |
5. Organize risks and concerns
   |
6. Implementation plan (Phase breakdown)
```

## Impact Severity Criteria

| Severity | Criteria | Response |
|----------|----------|----------|
| High | Code modification required (hardcoded values, switch statement additions, etc.) | Detailed investigation required |
| Medium | Verification needed (dynamic retrieval but requires validation) | Behavior verification needed |
| Low | Automatic handling (fully dynamic retrieval) | Confirmation only |

## Output Format

```markdown
# [Feature Name] Impact Analysis Report

## ADR (Architecture Decision Record)

### Decision
[Briefly describe the change]

### Context
[Reason for change / business requirements]

### Technical Decision
[Architectural judgment and rationale]

---

## Impact Scope Analysis

### Impact Summary

| Severity | Count | Percentage |
|----------|-------|------------|
| High (modification required) | X | XX% |
| Medium (verification needed) | X | XX% |
| Low (automatic handling) | X | XX% |

### Impact List by Category

#### 1. Database

| Table Name | Change Description | Severity | Notes |
|------------|-------------------|----------|-------|
| xxx | Column addition | High | ... |

#### 2. Model/Enum

| File | Change Description | Severity | Notes |
|------|-------------------|----------|-------|
| xxx.php | Constant addition | High | ... |

#### 3. Service/UseCase

| File | Change Description | Severity | Notes |
|------|-------------------|----------|-------|
| xxxService.php | Method modification | High | ... |

#### 4. Batch Processing

| Batch Name | Change Description | Severity | Notes |
|------------|-------------------|----------|-------|
| xxxBatch | ... | Medium | ... |

---

## High-Impact Area Detailed Analysis

### [Service Name 1]

Use Service specification summary format (/service-spec skill)

---

## Risks and Concerns

### High Risk (must resolve before implementation)

| Item | Description | Contact | Deadline |
|------|-------------|---------|----------|
| xxx | ... | Related department | Before Phase X |

### Medium Risk (verify during implementation)

| Item | Description | Contact |
|------|-------------|---------|
| xxx | ... | ... |

### Low Risk (can address after implementation)

| Item | Description |
|------|-------------|
| xxx | ... |

---

## Implementation Plan

### Phase 0: [Name]
- Objective: ...
- Scope: ...
- Completion criteria: ...

### Phase 1: [Name]
- Objective: ...
- Scope: ...
- Completion criteria: ...

---

## Checklist

### Phase 0
- [ ] Task 1
- [ ] Task 2

### Phase 1
- [ ] Task 1
- [ ] Task 2

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | YYYY-MM-DD | Initial version |
```

## Quality Checks

### 1. Completeness
- [ ] Investigated all repositories
- [ ] Covered DB, Model, Service, and batch processing
- [ ] Identified hardcoded locations

### 2. Accuracy
- [ ] Verified with actual code (not assumptions)
- [ ] Included file path:line numbers
- [ ] Checked cross-repository differences

### 3. Practicality
- [ ] Impact severity criteria are clear
- [ ] Change descriptions are specific
- [ ] Contacts and deadlines are specified

### 4. Service Specification Summary
- [ ] Created specification summaries for high-impact Services/UseCases
- [ ] Included all 4 items: role, features, dependencies, and notes

## Output Templates

### Risk Registry Template

Record risks and concerns discovered during impact analysis using the following template for tracking.

| ID | Risk Description | Discovery Date | Severity | Status | Mitigation |
|----|-----------------|----------------|----------|--------|------------|
| R001 | [Risk description] | YYYY-MM-DD | High/Medium/Low | Unresolved/In Progress/Resolved | [Mitigation] |

**Example**:

| ID | Risk Description | Discovery Date | Severity | Status | Mitigation |
|----|-----------------|----------------|----------|--------|------------|
| R001 | Data migration script not yet created (structural change due to Enum conversion) | 2026-03-15 | High | In Progress | Migration script planned (Phase 0) |
| R002 | Need to verify external integration partner specification changes | 2026-03-15 | Medium | Unresolved | Confirmation deadline set |
| R003 | Existing tests may fail (calculation logic change) | 2026-03-16 | Medium | In Progress | Test fix proposal created |

---

## Parallel Investigation with Scouts

When the impact scope is wide, use multiple scouts (Task tool) in parallel to improve investigation efficiency.

```
Example: Impact investigation for adding a product category
  -> Scout 1: ValidationService investigation
  -> Scout 2: PriceCalculationService investigation
  -> Scout 3: CatalogUseCase investigation
```

---

## I/O Specification

### INPUT
| Type | Description | Required/Optional | Example |
|------|-------------|-------------------|---------|
| Change description | Description of the feature being added/changed | Required | `New category addition`, `Price calculation logic change` |
| Prior investigation results | Output from /investigate or /service-spec | Optional | Reference investigation report |

### OUTPUT
| Type | Format | Destination |
|------|--------|-------------|
| Impact analysis report | ADR-format Markdown (affected files list, risks, implementation plan) | stdout (report to leader) |

### Prerequisites
- Change target specification has been understood (prior investigation with /service-spec recommended)
- Service responsibility definitions are accessible (`input/project/service_responsibilities.md` or `knowledge/system/04_change_impact/service_responsibilities.md`)

### Downstream Skills (Pipeline)
- None (final deliverable; handoff material for implementation phase)

### Quality Checkpoints
- [ ] Included path:line numbers for affected files
- [ ] Classified impact severity (High/Medium/Low)
- [ ] Organized risks and concerns
- [ ] Created phased implementation plan
