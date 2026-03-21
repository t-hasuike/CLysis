# Legacy System Investigation Document Quality Assessment Criteria

> **Version**: 1.1
> **Last Updated**: 2026-03-02
> **Author**: ashigaru-scribe

## Overview

This document defines criteria for evaluating whether **investigation documents output by the leader team** meet the quality needed for **"a person to grasp the legacy system overview and proceed to the next action or plan."**

Unlike the system maturity assessment (`legacy_system_maturity_model.md`), this evaluates the **completeness and actionability of the document itself**.

---

## Definition of "Ready for Next Action"

A state where a person reading the investigation document can answer the following 5 questions:

| Question | Content | Required Information |
|----------|---------|---------------------|
| **What** | Can identify files/methods to change | File names, class names, method names listed |
| **Where** | Knows exact file paths and line numbers | Absolute paths, line numbers, links |
| **How** | Can judge implementation method options | Implementation patterns, technology selections presented |
| **Risk** | Can evaluate impact scope and side effects | Affected files, tables, APIs listed |
| **Next** | Can plan implementation order/Phase breakdown | Phase breakdown proposal, dependency organization |

---

## Perspective Checklists

### Tier 1 (Required) - Cannot grasp overview without these

#### 1. System Overview

| Item | Criteria | Rating |
|------|----------|--------|
| Repository structure | Related repositories (when 2+) listed with roles | O/T/X |
| Technology stack | Languages, frameworks, versions documented | O/T/X |
| Directory structure | Roles of key directories (app/, services/, config/, etc.) explained | O/T/X |
| Entry points | API/batch/frontend entry points listed | O/T/X |

**Rating criteria**:
- O: All items documented; understandable by others
- T: Partially documented; some areas insufficient or ambiguous
- X: Not documented or too fragmented to understand

#### 2. Business Logic

| Item | Criteria | Rating |
|------|----------|--------|
| Business flow | Key business flows (ordering, payment, delivery, etc.) diagrammed or explained | O/T/X |
| Service/UseCase responsibilities | Responsibilities of each Service/UseCase class explained | O/T/X |
| Data flow | Data input -> processing -> output is traceable (where it comes from, where it goes) | O/T/X |
| Business rules | Important business rules (price calculation, inventory checks, etc.) documented | O/T/X |

#### 3. Data Model

| Item | Criteria | Rating |
|------|----------|--------|
| Table list | Key tables listed with roles | O/T/X |
| Table relationships | Inter-table relationships (1:N, N:N, etc.) diagrammed or explained | O/T/X |
| Important columns | Business-critical columns (prices, statuses, dates, etc.) explained | O/T/X |
| Constraints/indexes | Foreign key constraints, unique constraints, indexes explained | O/T/X |

#### 4. Key Components

| Item | Criteria | Rating |
|------|----------|--------|
| Component responsibilities | Responsibilities of each component (Controller/Service/Repository, etc.) are clear | O/T/X |
| Dependencies | Inter-component dependencies (call direction) explained | O/T/X |
| Entry point identification | Controller/Route/command handlers identified | O/T/X |
| Layer structure | Architecture layers (Presentation/Application/Domain/Infrastructure) explained | O/T/X |

#### 5. External Dependencies

| Item | Criteria | Rating |
|------|----------|--------|
| External API list | List of integrated external APIs (payment, delivery, notification, etc.) | O/T/X |
| API specification overview | Overview of each API (purpose, authentication method, endpoint) documented | O/T/X |
| Batch list | Batch processing list with execution schedule and content | O/T/X |
| Failure impact | Impact scope of external service failures documented | O/T/X |

#### 6. Change Impact Analysis

| Item | Criteria | Rating |
|------|----------|--------|
| Affected files listed | Files/methods affected by changes are listed | O/T/X |
| Impact severity classified | Impact classified as High/Medium/Low | O/T/X |
| File paths specified | File path:line numbers specified (e.g., `app/Services/Foo.php:123`) | O/T/X |
| Side effects explained | Side effects of changes (impact on other features) explained | O/T/X |

#### 7. Actionability

| Item | Criteria | Rating |
|------|----------|--------|
| Phase breakdown | Implementation divided into Phase 1/Phase 2/... | O/T/X |
| Phase dependencies | Dependencies between Phases documented (e.g., start Phase 2 after Phase 1) | O/T/X |
| Risks organized | Technical and business risks organized | O/T/X |
| Verification checklist | Implementation verification items listed in checklist format | O/T/X |

#### 8. Local Development Environment

Information needed to "get it running." Investigation and changes are impossible without a working environment.

| Item | Criteria | Rating |
|------|----------|--------|
| Required tools/versions | Docker, PHP, Node.js version requirements documented | O/T/X |
| Environment setup procedure | Complete first-time setup procedure documented | O/T/X |
| Environment variables/config files | .env sample, required configuration items listed | O/T/X |
| Database initialization | Migration/seed execution procedure documented | O/T/X |
| Start/stop method | Service start/stop commands documented | O/T/X |
| Operational verification | Normal startup criteria (URL, log verification, etc.) documented | O/T/X |
| Known issues and fixes | Common errors and solutions documented | O/T/X |

---

### Tier 2 (Recommended) - Enables deeper understanding

#### 1. Technical Debt

| Item | Criteria | Rating |
|------|----------|--------|
| Hardcoded locations | Magic numbers and hardcoded strings identified | O/T/X |
| Duplicate code | Duplicate code locations identified with consolidation proposals | O/T/X |
| Cross-repository differences | When same functionality exists in multiple repos, differences organized | O/T/X |
| Anti-patterns | Deprecated coding patterns (global variables, SQL injection, etc.) identified | O/T/X |

#### 2. Known Issues

| Item | Criteria | Rating |
|------|----------|--------|
| Bugs/defects | Known bugs and defects listed | O/T/X |
| Performance concerns | N+1 problems, slow queries, etc. documented | O/T/X |
| Security concerns | SQL injection, XSS, authentication gaps, etc. documented | O/T/X |

#### 3. Detailed Data Flow

| Item | Criteria | Rating |
|------|----------|--------|
| Data flow diagram | Data flow diagrammed (sequence diagram, flowchart, etc.) | O/T/X |
| State transitions | Entity state transitions (order status, etc.) diagrammed or explained | O/T/X |
| Error flow | Error flow (retries, compensation transactions, etc.) documented | O/T/X |

#### 4. Local Development Environment (Advanced)

| Item | Criteria | Rating |
|------|----------|--------|
| Debugging methods | Breakpoint setup, log output methods documented | O/T/X |
| Test execution | Unit test and integration test execution procedures documented | O/T/X |
| Performance measurement | Profiling tool usage documented | O/T/X |

---

### Tier 3 (Supplementary) - Useful for future maintenance

| Item | Criteria | Rating |
|------|----------|--------|
| Historical context | Explanation of why it's implemented this way (past decisions, constraints) | O/T/X |
| Unused code | Dead code and deprecated features identified | O/T/X |
| Test status | Test coverage and test strategy documented | O/T/X |
| Future extensibility | Design considerations for future extensions documented | O/T/X |

---

## Maturity Assessment (6 Levels)

| Level | State | Description | Tier 1 | Tier 2 | Tier 3 |
|-------|-------|-------------|--------|--------|--------|
| **Level 0** | Not started | No document exists | - | - | - |
| **Level 1** | Initial investigation | Only system structure and tech stack documented | 1-2 categories only | X | X |
| **Level 2** | Basic completion | All Tier 1 (required) items documented | All 8 categories O/T | T | X |
| **Level 3** | Comprehensive | Tier 2 (recommended) items also included | All 8 categories O | O/T | X |
| **Level 4** | Actionable | Ready to proceed to next steps (implementation plan and impact analysis complete) | All 8 categories O | O | T |
| **Level 5** | Complete | Tier 3 (supplementary) included; durable for future maintenance | All 8 categories O | O | O |

**Criteria for proceeding to next steps: Level 4 or above**

---

## Blocker Detection (Critical Defects)

If any of the following are missing, **cannot proceed to next steps** (additional investigation required):

| Blocker ID | Content | Detection Method |
|-----------|---------|-----------------|
| **B001** | Files/methods to modify not identified | Tier 1-6 "Affected files listed" is X |
| **B002** | Impact scope not listed | Tier 1-6 "Impact severity classified" and "Side effects explained" are X |
| **B003** | File path:line numbers not specified | Tier 1-6 "File paths specified" is X |
| **B004** | Risks and concerns not organized | Tier 1-7 "Risks organized" is X |
| **B005** | No implementation plan (Phase breakdown) | Tier 1-7 "Phase breakdown" is X |
| **B006** | Environment setup procedure missing or startup method unknown | Tier 1-8 "Environment setup procedure" and "Start/stop method" are X |

**If even 1 blocker exists**: Cannot proceed to next steps (additional investigation required)

---

## How to Conduct Assessments

### Assessment Timing

| Timing | Purpose | Evaluator |
|--------|---------|-----------|
| Document completion | Understand maturity, identify gaps | Leader |
| Pre-implementation review | Final actionability confirmation | User (human) |
| Phase completion retrospective | Verify document quality vs implementation alignment | Development team |

### Assessment Process

```
1. Read the document
   |
2. Check each Tier 1 (required) category -> record O/T/X
   |
3. Blocker detection (B001-B005) -> NG if any
   |
4. Check Tier 2 (recommended) and Tier 3 (supplementary)
   |
5. Determine maturity level (Level 0-5)
   |
6. If below Level 4 -> identify gaps -> request additional investigation
   |
7. If Level 4 or above -> implementation can begin
```

### Improvement Cycle

```
Conduct assessment
  |
Identify gaps (which Tier 1-3 items are X)
  |
Conduct additional investigation (request leader for more investigation)
  |
Update document (scribe reflects changes)
  |
Re-assess (repeat until Level 4 reached)
```

---

## Comparison with Other Assessment Criteria

| Assessment Criteria | Evaluation Target | Usage Timing | Users |
|--------------------|-------------------|-------------|-------|
| **legacy_document_quality.md** (this document) | Investigation document quality | Document completion, pre-implementation review | Leader, user |
| **legacy_system_maturity_model.md** | Legacy system maturity | System improvement planning, progress tracking | Management, development team |
| **evaluation_criteria_matrix.md** | System maturity quantitative criteria | Quantitative maturity evaluation | Development team |

**Usage guidelines**:
- **Planning system improvements**: Use `legacy_system_maturity_model.md` + `evaluation_criteria_matrix.md`
- **Reviewing investigation documents**: Use `legacy_document_quality.md` (this document)

---

## Assessment Example

### Target Document: `reports/investigation/sample_investigation.md`

#### Tier 1 Check Results

| Category | Rating | Reason |
|----------|--------|--------|
| 1. System Overview | O | Repository structure, tech stack, directory structure documented |
| 2. Business Logic | T | Service responsibilities documented but data flow unclear |
| 3. Data Model | O | Table list, relationships, important columns documented |
| 4. Key Components | O | Component responsibilities, dependencies documented |
| 5. External Dependencies | O | Batch list, API integrations documented |
| 6. Change Impact Analysis | O | Affected files, file path:line numbers specified |
| 7. Actionability | T | Phase breakdown exists but risk organization insufficient |

#### Blocker Detection Results

| Blocker ID | Judgment | Reason |
|-----------|----------|--------|
| B001 | O (OK) | Target files and methods identified |
| B002 | O (OK) | Impact scope listed |
| B003 | O (OK) | File path:line numbers specified |
| B004 | X (NG) | Risks and concerns not organized |
| B005 | O (OK) | Phase breakdown exists |

#### Maturity Level Determination

- **Result**: Level 2 (Basic completion)
- **Reason**: 5 of 7 Tier 1 categories are O, 2 are T. However, B004 (risk organization) is a blocker.
- **Next steps**: **Cannot start implementation**. Re-assess after additional risk organization investigation.

---

## Related Documents

- **legacy_system_maturity_model.md**: System maturity assessment (different evaluation target)
- **evaluation_criteria_matrix.md**: System maturity quantitative criteria

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2026-03-02 | Added local development environment category to Tier 1, added debug/test items to Tier 2, added environment setup procedure gap to blocker detection |
| 1.0 | 2026-03-02 | Initial version. Defined Tier 1-3 checklists and 6-level maturity assessment |
