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

Output: `reports/current-prd-{repo}-phase1.md`

### Phase 2: Module Analysis (Deep Dive)

For each significant module/service discovered in Phase 1:

1. **Controller → Service → Repository chain**: trace the call hierarchy
2. **Input/Output contracts**: request validation, response shapes, error handling
3. **Database operations**: which tables are read/written, JOIN patterns, transaction boundaries
4. **External integrations**: API calls, SFTP, S3, SQS, email
5. **Business rules**: conditional logic, flag-based branching, calculation formulas
6. **Cross-repository dependencies**: shared DB tables, API calls between repos

#### Analysis Item Execution Procedures

| # | Analysis Item | Execution Procedure | Extraction Target |
|---|-------------|---------------------|-------------------|
| 1 | Call hierarchy | Use Serena find_referencing_symbols to recursively enumerate all reference sites of the target Service/Controller | Upstream Controllers, Middleware, batch Commands, call chains from other Services |
| 2 | Input/Output contracts | Use Serena find_symbol to locate the target Controller's Request/FormRequest classes, then use Read to confirm validation rules and Response type/structure | Validation rules, response JSON structure, HTTP status codes, error response shapes |
| 3 | DB operations | Use grep to search within target Service for `DB::`, `->table(`, `->join(`, `->where(`, Eloquent model names. Search for transaction boundaries via `DB::transaction` / `DB::beginTransaction` | Read/write table names, JOIN conditions, WHERE conditions, transaction scope |
| 4 | External integrations | Use grep to search for keywords: `curl`, `Http::`, `sftp`, `S3`, `SqsQueue`, `Mail::`, `Storage::`, etc. | Connection target URLs/bucket names, data formats, error handling approach |
| 5 | Business rules | Use Read to examine conditional branches (if/switch/match) within the target Service. Use Serena find_symbol to locate Enum/constant classes | Branch conditions, flag names and meanings, calculation formulas, state transitions |

#### Scope Limitation

Analyzing all Services at the same depth wastes tokens. Narrow down detailed analysis targets using these criteria:

- **Detailed analysis**: Services from Phase 1 with high route count, high incoming coupling, or external integrations (guideline: top 30%)
- **Summary only**: Remaining Services get file list, endpoint list, and key table names only
- **Decision basis**: Use Phase 1 quantitative scan results (route count, file LOC, incoming coupling) as evidence

Output: `reports/current-prd-{repo}-phase2.md`

### Phase 3: Structured Output (PRD Assembly)

Assemble findings into PRD format, mapped to the project's knowledge structure:

1. **System Overview**: maps to `knowledge/system/01_overview/`
2. **Architecture & Structure**: maps to `knowledge/system/02_structure/`
3. **Data Flow & Behavior**: maps to `knowledge/system/03_behavior/`
4. **API Specification**: endpoint list with request/response schemas
5. **Database Model**: table relationships, key columns, business meaning
6. **Batch Process Specification**: schedule, input/output, dependencies
7. **Cross-Repository Dependency Map**: which repos read/write shared resources

Output: `reports/current-prd-{repo}-final.md`

## Scope Control

To manage token consumption on large codebases, scope can be limited:

- `full`: scan entire repository (use for small repos or initial baseline)
- `[module-name]`: scan specific module/feature area (e.g., "order-processing", "payment")

## Output Rules

- Output to `reports/` only. Never overwrite `knowledge/` directly
- Human reviews output, then uses `/doc-organize` to promote to `knowledge/`
- State observations only. No modification proposals (state assessment phase rule)
- Subject-first rule: always specify "whose/what's" for domain terms

## Integration with Existing Skills

| Existing Skill | Relationship |
|---------------|-------------|
| /current-spec | Point investigation and detailed specification. current-prd is the surface-level counterpart |
| /current-prd | Promotes bulk findings. current-spec promotes individual findings |
| /doc-organize | Transfers current-prd output from reports/ to knowledge/ |
| /current-legacy | Phase 0 auto-collection overlaps. current-prd extends with Module Analysis |

## I/O Specification

### INPUT
| Type | Content | Required |
|------|---------|----------|
| Repository path | Local path to target repository | Required |
| Scope | `full` or module name | Optional (default: full) |

### OUTPUT
| Type | Format | Destination |
|------|--------|-------------|
| Phase 1 report | Markdown (tech stack, endpoints, DB tables) | `reports/current-prd-{repo}-phase1.md` |
| Phase 2 report | Markdown (module analysis, dependencies) | `reports/current-prd-{repo}-phase2.md` |
| Final PRD | Markdown (assembled PRD with knowledge/ mapping) | `reports/current-prd-{repo}-final.md` |

### Downstream Skills (Pipeline)

| Skill | Condition | Instruction |
|-------|-----------|-------------|
| `/doc-organize` | After decision maker reviews and approves the PRD | Report to leader for approval, then execute `/doc-organize` to integrate into knowledge base |
| `/doc-update` | When depth adjustment is needed by target audience after promotion to knowledge/ | Propose to leader and await judgment |
| `/current-distortion` | When risks are discovered during PRD investigation | Do not propose fixes; record findings and report to leader, suggesting delegation to `/current-distortion` |

> **Fallback**: If prerequisites are not met, report to leader and await further instructions

## Quality Checklist (for Inspector)

| # | Check Item | Verification Method | Pass Criteria | Failure Response |
|---|-----------|-------------------|---------------|------------------|
| 1 | All endpoints discovered and documented | Read routes/api.php, web.php and cross-reference against PRD endpoint list. grep for `Route::` to check for omissions | Route definition endpoint count matches PRD count. Zero discrepancies | List missing endpoints and issue correction instructions for additional Phase 2 analysis |
| 2 | DB tables mapped to business domain | Extract table list from schema or migration files and cross-reference with PRD domain mapping | All tables are linked to a business domain (process name or entity name) | List unmapped tables and issue correction instructions for usage investigation |
| 3 | Cross-repository dependencies identified | grep for shared table names, API URLs, and shared Enum names in other repositories; cross-reference with PRD dependencies | PRD-listed dependencies are confirmed in actual code, and zero unlisted dependencies exist | List unlisted dependencies with impact scope and issue correction instructions |
| 4 | External integrations documented (SFTP, S3, API calls) | grep for `sftp`, `Storage::`, `S3Client`, `Http::`, `curl`, `Guzzle`, etc. and cross-reference with PRD | All external integration points in actual code are documented in PRD | List undocumented integrations with connection targets and data formats, and issue correction instructions |
| 5 | Batch processes with schedule and I/O documented | Read Console/Kernel.php schedule() and Console/Commands/ command list; cross-reference with PRD | All batch commands have schedule (cron expression), input source, and output destination documented | List items with missing details and issue correction instructions for detailed investigation |
| 6 | No modification proposals included (state assessment only) | Review full PRD text; grep for expressions like "should", "must change", "refactor", "recommend" | Zero modification instructions or improvement proposals. Composed entirely of factual descriptions and state records | Delete offending sections or rewrite as factual descriptions, and issue correction instructions |
