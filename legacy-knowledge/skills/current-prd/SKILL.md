---
name: current-prd
description: Reverse-engineer PRD (Product Requirements Document) from existing codebase. Scans code structure, APIs, services, and DB schema to generate structured specification documents.
argument-hint: "[repository-name] [scope: full | module-name]"
---

# /current-prd -- Code-to-PRD Generation Skill

> This is a generic skill from [CLysis](https://github.com/t-hasuike/CLysis).
> Terminology can be customized via `config/terminology.md`.

## Overview

Generate a PRD (Product Requirements Document) by reverse-engineering an existing codebase. Instead of writing specs from scratch, extract the actual behavior from code and organize it into structured documentation that can be maintained as a living document.

## When to Use

- Onboarding to a legacy codebase with no documentation
- Updating outdated specifications to match current implementation
- Creating a baseline spec before refactoring
- Bridging the gap between code reality and documented expectations

## Three-Phase Workflow

### Phase 1: Global Scan (Automated Collection)

Collect facts that can be extracted without human input:

1. **Technology Stack**: package managers (composer.json, package.json, go.mod), framework versions, language versions
2. **Entry Points**: routes/api.php, web.php, console commands (Artisan), batch scripts
3. **Infrastructure**: docker-compose.yml, Dockerfile, .env.example
4. **Database**: schema files, migration history, table/column inventory
5. **Directory Structure**: top-level organization, naming patterns

Output: `reports/prd-generate-{repo}-phase1.md`

### Phase 2: Module Analysis (Deep Dive)

For each significant module/service discovered in Phase 1:

1. **Controller → Service → Repository chain**: trace the call hierarchy
2. **Input/Output contracts**: request validation, response shapes, error handling
3. **Database operations**: which tables are read/written, JOIN patterns, transaction boundaries
4. **External integrations**: API calls, SFTP, S3, SQS, email
5. **Business rules**: conditional logic, flag-based branching, calculation formulas
6. **Cross-repository dependencies**: shared DB tables, API calls between repos

Output: `reports/prd-generate-{repo}-phase2.md`

### Phase 3: Structured Output (PRD Assembly)

Assemble findings into PRD format, mapped to the project's knowledge structure:

1. **System Overview**: maps to `knowledge/system/01_overview/`
2. **Architecture & Structure**: maps to `knowledge/system/02_structure/`
3. **Data Flow & Behavior**: maps to `knowledge/system/03_behavior/`
4. **API Specification**: endpoint list with request/response schemas
5. **Database Model**: table relationships, key columns, business meaning
6. **Batch Process Specification**: schedule, input/output, dependencies
7. **Cross-Repository Dependency Map**: which repos read/write shared resources

Output: `reports/prd-generate-{repo}-final.md`

## Scope Control

To manage token consumption on large codebases, scope can be limited:

- `full`: scan entire repository (use for small repos or initial baseline)
- `[module-name]`: scan specific module/feature area (e.g., "order-processing", "payment")

## Output Rules

- Output to `reports/` only. Never overwrite `knowledge/` directly
- Human reviews output, then uses `/archive-reports` to promote to `knowledge/`
- State observations only. No modification proposals (state assessment phase rule)
- Subject-first rule: always specify "whose/what's" for domain terms

## Integration with Existing Skills

| Existing Skill | Relationship |
|---------------|-------------|
| /current-spec | Point investigation and detailed specification. current-prd is the surface-level counterpart |
| /current-prd | Promotes bulk findings. current-spec promotes individual findings |
| /archive-reports | Transfers prd-generate output from reports/ to knowledge/ |
| /legacy-analyze | Phase 0 auto-collection overlaps. prd-generate extends with Module Analysis |

## I/O Specification

### INPUT
| Type | Content | Required |
|------|---------|----------|
| Repository path | Local path to target repository | Required |
| Scope | `full` or module name | Optional (default: full) |

### OUTPUT
| Type | Format | Destination |
|------|--------|-------------|
| Phase 1 report | Markdown (tech stack, endpoints, DB tables) | `reports/prd-generate-{repo}-phase1.md` |
| Phase 2 report | Markdown (module analysis, dependencies) | `reports/prd-generate-{repo}-phase2.md` |
| Final PRD | Markdown (assembled PRD with knowledge/ mapping) | `reports/prd-generate-{repo}-final.md` |

### Post-processing
- Human reviews final PRD
- `/archive-reports` promotes relevant sections to `knowledge/`
- `/doc-update` adjusts depth for target audience

## Quality Checklist

- [ ] All endpoints discovered and documented
- [ ] Database tables mapped to business domain
- [ ] Cross-repository dependencies identified
- [ ] External integrations documented (SFTP, S3, API calls)
- [ ] Batch processes with schedule and I/O documented
- [ ] No modification proposals included (state assessment only)
