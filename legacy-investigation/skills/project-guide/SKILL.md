---
name: project-guide
description: Present a reference guide for project documentation tailored to the task. Used at mission start and during impact investigation.
argument-hint: <task overview>
---

> This is a generic skill from [CLysis](https://github.com/t-hasuike/CLysis).
> Terminology can be customized via `config/terminology.md`.

# /project-guide Skill

## Overview

A guide skill that analyzes the nature of the task and presents the optimal reference order from input/project/ and input/domain/.
Helps the leader's team reach "the knowledge needed for the current mission" as quickly as possible.

See config/terminology.md for term customization

## Usage

/project-guide [task overview]

### Generic Usage Examples (applicable to any legacy system)

| Example | Task Type |
|---------|-----------|
| /project-guide Order processing bug investigation | Bug fix |
| /project-guide Adding a new API endpoint | New feature addition |
| /project-guide External API specification change response | Specification change |
| /project-guide Understanding batch processing specifications | Investigation & analysis |
| /project-guide Local development environment setup | Environment setup |
| /project-guide Consolidating duplicate code | Refactoring |

### Project-Specific Usage Examples

For project-specific usage examples, keyword mappings, and notes, see `PROJECT_EXAMPLES.md`.
Create this file per project to document domain-specific settings.

## Investigation Target

$ARGUMENTS

## Execution Steps

### Step 1: Determine Task Type

Classify the task overview into one of the following:

| Type | Determination Criteria |
|------|----------------------|
| New feature addition | Category addition, screen addition, API addition, etc. |
| Bug fix | Error correction, defect resolution |
| Specification change | Rule changes, external API changes |
| Investigation & analysis | Impact investigation, specification understanding, code reading |
| Environment setup | Local development environment, Docker, DB |
| Refactoring | Code improvement, technical debt resolution |

### Step 2: Generate Reference Guide

Output in the following format:

```
# Project Guide - [Task Overview]

## Recommended Reference Order

### Phase 1: System Understanding (required reading)
[Always presented regardless of task type]
1. input/project/overview.md - Project overview
2. input/project/repositories.md - Repository responsibility boundaries

### Phase 2: Task-Specific Knowledge
[Dynamically selected based on task type]

### Phase 3: Implementation Preparation
[Presented only when applicable]

### Phase 4: Impact Analysis
[Presented only when changes are involved]

## Related Domain Knowledge
[Present applicable files from input/domain/]

## Notes
[Extract relevant notes from environment.md "common pitfalls"]
```

### Step 3: Guide Mapping by Task Type

#### New Feature Addition
- **Phase 2**: environment.md (business rules) -> service_responsibilities.md (related Services) -> tech_stack.md (technical constraints)
- **Phase 3**: typical_change_patterns.md (check similar patterns) -> schema_database.md (DB verification)
- **Phase 4**: impact_analysis_template.md -> impact_analysis_example.md

#### Bug Fix
- **Phase 2**: service_responsibilities.md (identify cause location) -> environment.md (verify business rules)
- **Phase 3**: schema_database.md (data verification) -> non_functional_requirements.md (constraint verification)
- **Phase 4**: None (when fix scope is limited)

#### Specification Change
- **Phase 2**: environment.md (current specification) -> service_responsibilities.md (affected Services) -> diagrams/data_flow.md (data flow)
- **Phase 3**: typical_change_patterns.md -> schema_database.md
- **Phase 4**: impact_analysis_template.md -> impact_analysis_example.md

#### Investigation & Analysis
- **Phase 2**: service_responsibilities.md -> diagrams/system_overview.md -> diagrams/data_flow.md -> diagrams/io_interfaces.md
- **Phase 3**: schema_database.md -> environment.md
- **Phase 4**: None

#### Environment Setup
- **Phase 2**: local_dev.md -> tech_stack.md
- **Phase 3**: None
- **Phase 4**: None
- **Note**: Reference detailed knowledge under input/local_dev/

#### Refactoring
- **Phase 2**: service_responsibilities.md (verify responsibilities) -> non_functional_requirements.md (constraints) -> todo_list.md (known issues)
- **Phase 3**: typical_change_patterns.md -> schema_database.md
- **Phase 4**: impact_analysis_template.md

### Step 4: Domain Knowledge Mapping

Present relevant files from input/domain/ based on keywords in the task overview.

**Project-specific mappings**: Define keyword-to-file mappings in `PROJECT_EXAMPLES.md`.

### Step 5: Extract Notes

Extract task-related notes from the "common pitfalls" section of environment.md.

**Common notes (always presented)**:
- Include project-specific soft-delete conditions (e.g., delflag='0') in all queries
- Verify project-specific type safety rules (e.g., PHP strict_types)
- Synchronize duplicate code across multiple repositories

**Project-specific notes**: Document in `PROJECT_EXAMPLES.md`.

## Document Quality Evaluation Integration

After task completion, it is recommended to evaluate documents output to output/ against the criteria in input/assessment/legacy_document_quality.md.

**"Ready for next action" 5W Check**:
- **What**: Change target has been identified
- **Where**: File path:line number is known
- **How**: Implementation method has been determined
- **Risk**: Impact scope and side effects have been evaluated
- **Next**: Phase-divided plan exists

## Report Format

```
# Project Guide - [Task Overview]

> **Task Type**: [New feature addition / Bug fix / Specification change, etc.]
> **Created**: YYYY-MM-DD

---

## Recommended Reference Order

### Phase 1: System Understanding (required reading)
1. `input/project/overview.md` - Project overview
2. `input/project/repositories.md` - Repository responsibility boundaries

### Phase 2: Task-Specific Knowledge
1. `input/project/environment.md` - [Reference reason]
2. `input/project/service_responsibilities.md` - [Reference reason]
...

### Phase 3: Implementation Preparation
1. `input/project/typical_change_patterns.md` - [Reference reason]
2. `input/project/schema_database.md` - [Reference reason]
...

### Phase 4: Impact Analysis
1. `input/project/impact_analysis_template.md` - [Reference reason]
2. `input/project/impact_analysis_example.md` - [Reference reason]

---

## Related Domain Knowledge

- `input/domain/xxx.md` - [Relevance reason]

---

## Notes

### Common (required)
- Include project-specific soft-delete conditions (e.g., delflag='0') in all queries
- Project-specific type safety rules (e.g., PHP strict_types) required
- Synchronize duplicate code across multiple repositories

### Task-Specific
- [Task-specific notes extracted from environment.md]
```

## Prohibited Actions

- Do not specify documents by assumption (present only after confirming input/ contents)
- Do not modify files (guide presentation is the primary mission)

---

## I/O Specification

### INPUT
| Type | Description | Required/Optional | Example |
|------|-------------|-------------------|---------|
| Task overview | Description of the task to be performed | Required | `Order processing bug investigation`, `New API endpoint addition` |

### OUTPUT
| Type | Format | Destination |
|------|--------|-------------|
| Reference guide | Document reference order and related file list | stdout (report to leader) |

### Prerequisites
- Documents in input/project/ exist
- Domain knowledge in input/domain/ exists

### Downstream Skills (Pipeline)
- `/investigate` -- Detailed investigation of targets identified by the guide
- `/service-spec` -- Create specification for Services identified by the guide
- `/impact-analysis` -- Analyze impact scope identified by the guide

### Quality Checkpoints
- [ ] Correctly classified task type
- [ ] Reference order has logical rationale
- [ ] Presented all related domain knowledge without omission
