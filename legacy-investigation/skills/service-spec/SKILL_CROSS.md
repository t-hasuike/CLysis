---
name: service-spec (CROSS)
description: Cross-repository service specification analysis. Documents features spanning multiple repositories, focusing on data flow, synchronization points, and consistency rules.
argument-hint: <Feature name> <Repository A> <Repository B>
---

> This is a generic skill from [decouple-legacy](https://github.com/t-hasuike/decouple-legacy-skills).
> Terminology can be customized via `config/terminology.md`.

# [Feature Name: e.g., Batch Processing] Cross-Repository Specification Summary

## 1. Business Domain Overview
[Describe the business problem this feature solves and its overall picture in 3 lines]
- **Key Actors**: System administrators, end users, external systems
- **Related Domain**: Domain knowledge under input/domain/

## 2. System Architecture / Component Diagram

| Component | Repository | Primary Role |
|-----------|-----------|-------------|
| `OrderService` | backend | Order data aggregation and evaluation |
| `NotificationSync` | frontend | Front-end notification |

---

## 3. Cross-Repository Processing Flow (Sequence)
1. **[Core]** `ProcessingService::execute()` extracts target data
2. **[Core]** Updates `DataModel` and creates processing instructions
3. **[API]** Sends request to external API
4. **[Frontend]** Calls `UpdateService` via Webhook to synchronize status

---

## 4. Impact Scope / Dependency Matrix (Matrix)
[Extend existing "dependent classes" to feature-level scope]

### Related Service/Model List
- [ ] `app/Services/Processing/MainService.php` (logic core)
- [ ] `app/Models/Data.php` (Scope: add `eligibleForProcessing`)

---

## 5. Data Consistency and Differences (Important)
- **Source of Truth**: Status is held by `backend`
- **Synchronization Timing**: Async Job reflects to `frontend` upon processing completion
- **Inconsistency Behavior**: Backend side takes priority; frontend side recovers via re-sync batch

---

## 6. Notable Items / Technical Debt
[Reuse existing "hardcoded" and "debt" sections as-is]

---

## I/O Specification

### INPUT
| Type | Description | Required/Optional | Example |
|------|-------------|-------------------|---------|
| Feature name | Cross-repository feature name | Required | `Batch processing`, `Order sync` |
| Repository A | First repository | Required | `backend`, `core` |
| Repository B | Second repository | Required | `frontend`, `api` |

### OUTPUT
| Type | Format | Destination |
|------|--------|-------------|
| Cross-repository specification summary | Cross-repository specification document with data flow, sync points, and consistency rules | stdout (report to leader) |

### Prerequisites
- Serena MCP is running
- Both repositories are accessible
- Prior understanding of each repository's individual specification via /investigate or /service-spec is recommended

### Downstream Skills (Pipeline)
- `/impact-analysis` -- Cross-repository change impact analysis
- `/build-knowledge` -- Persist cross-repository patterns to domain knowledge

### Quality Checkpoints
- [ ] Documented data consistency rules
- [ ] Identified Source of Truth clearly
- [ ] Documented synchronization timing and inconsistency behavior
- [ ] Confirmed implementations in both repositories (not assumptions)
