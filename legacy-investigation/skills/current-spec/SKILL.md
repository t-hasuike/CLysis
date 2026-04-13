---
name: current-spec
description: Systematically investigate Service/UseCase/Model specifications and organize them in Service specification summary format. Combines investigative discovery with detailed specification documentation. Deploy scouts (Explore agents) for rapid initial investigation.
argument-hint: <Service/UseCase/Model name> [repository name]
---

> This is a generic skill from [CLysis](https://github.com/t-hasuike/CLysis).
> Terminology can be customized via `config/terminology.md`.

# Service Specification Summary Skill

## Overview

Investigate the specification of the specified Service/UseCase/Model and organize it in a unified format. This skill combines rapid investigative discovery (scout mode) with comprehensive detailed specification documentation.

## Investigation Target

$ARGUMENTS

## Investigation Procedure

1. **Context check**: Review CLAUDE.md to understand project overview, repository structure, and tech stack
2. **Domain knowledge check**: Check domain knowledge files under knowledge/domain/ to understand knowledge related to the investigation target
   - Check the file list under knowledge/domain/
   - Read files related to the task keywords
   - Start investigation with understanding of known business rules and constraints
3. **Target file identification**: Identify file paths using Serena's find_symbol
4. **Symbol overview retrieval**: Get method list using get_symbols_overview
5. **Dependency investigation**: Identify callers/callees using find_referencing_symbols
6. **Detailed reading**: Read only important method bodies using find_symbol
7. **Survival check**: Verify the investigation target is still actively used

   | Check Item | Method | Criteria |
   |------------|--------|----------|
   | Caller existence | Serena find_referencing_symbols | At least 1 reference must exist. If 0, record as "dead code candidate" |
   | Last commit date | `git log -1 --format=%ci [file_path]` | If >1 year since last update, record as "low activity". Record fact only — do not propose deletion |
   | Runtime usage | Check route definitions, cron schedules, queue registrations | May be used at runtime even without static references |

   **Note**: Dead code candidate / low activity judgments are factual records only. Do not propose deletion or refactoring (state-comprehension phase rule).

8. **Diff check**: If the same class exists in multiple repositories, check differences

## Output Format

```markdown
# [Service/UseCase Name] Specification Summary

**File Path**: `app/Services/xxx/xxxService.php`
**Repository**: [Target repository (each repository if multiple)]
**Last Investigation Date**: YYYY-MM-DD

---

## 1. Role (Responsibility)

[Explain the responsibility of this Service/UseCase in 1-2 sentences]

**Callers**:
- [Controller/UseCase name]: [Purpose]
- [Batch name]: [Purpose]

---

## 2. Key Feature List

| Method Name | Description | Visibility | Line Numbers |
|-------------|-------------|------------|--------------|
| `methodA()` | ... | public | 45-67 |
| `methodB()` | ... | private | 70-85 |

> **Checkpoint**: After completing the key feature list, report progress to the leader and confirm the investigation scope before proceeding to dependency and side-effect analysis.

### Key Method Details

#### methodA()
- **Description**: ...
- **Parameters**: `$param1` (type), `$param2` (type)
- **Return value**: type
- **Processing flow**:
  1. ...
  2. ...

---

## 3. Dependent Classes/Modules

### Internal Dependencies (same repository)

| Type | Class Name | Purpose | File Path |
|------|-----------|---------|-----------|
| Model | xxx | ... | app/xxx.php |
| Enum | xxx | ... | app/Enums/xxx.php |

### External Dependencies (other repositories / external services)

| Type | Name | Purpose |
|------|------|---------|
| API | xxx | ... |
| DB | xxx table | ... |

---

## 4. Notable Items (Legacy Code / Technical Debt)

### Hardcoded Locations

| Line Number | Content | Impact | Improvement Proposal |
|-------------|---------|--------|---------------------|
| 25-30 | Category array | Requires modification when adding new categories | Dynamic retrieval from DB/Enum |

### Technical Debt

| Item | Details | Priority |
|------|---------|----------|
| typo | Typo in `ClassName` | Medium |
| duplication | Processing duplication between xxx and yyy | Low |

### Cross-Repository Differences

| Item | Repository A | Repository B | Response Policy |
|------|-------------|-------------|-----------------|
| xxx | Present | Absent | No action needed |

---

## Change History

| Date | Description |
|------|-------------|
| YYYY-MM-DD | Initial version |
```

## Quality Checks

Upon investigation completion, verify the following:

- [ ] Confirmed with actual code (not assumptions)
- [ ] Included file path:line numbers
- [ ] Checked cross-repository differences
- [ ] Identified hardcoded locations

## Reporting Guidelines

1. **Distinguish facts from speculation**: Use "X is Y" for confirmed findings; use "X appears to be Y (needs verification)" for unconfirmed items
2. **Include code references**: Always cite in `filename:line_number` format
3. **Be concise and accurate**: Avoid verbose explanations; emphasize key findings

---

## I/O Specification

### INPUT
| Type | Description | Required/Optional | Example |
|------|-------------|-------------------|---------|
| Target class | Service/UseCase/Model name | Required | `OrderService`, `CreateOrderUseCase` |
| Repository | Target repository specification | Optional | `backend`, `frontend` |

### OUTPUT
| Type | Format | Destination |
|------|--------|-------------|
| Service specification summary | Detailed Markdown (method list, dependencies, business rules) | stdout (report to leader) |

### Prerequisites
- Serena MCP is running
- Target file has been identified (prior investigation with /current-spec recommended)

### Downstream Skills (Pipeline)
- `/change-impact` -- Impact analysis with specification understanding

### Quality Checkpoints
- [ ] Covered all public methods
- [ ] Documented dependencies (DI)
- [ ] Extracted business rules and validations
- [ ] Included file path:line numbers
