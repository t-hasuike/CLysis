<!-- This output-contract facet is based on the TAKT framework (https://github.com/nrslib/takt), MIT License, Copyright (c) 2026 Masanobu Naruse. -->
# SEM Document - Semantic Model Document Format

## Overview

Format definition for the SEM document (SEM-draft.md) output by the execute_sem step. It conforms to the output format (6-chapter structure) of the /current-semantic skill (see legacy-knowledge/skills/current-semantic).

---

## File-Naming Rule

`[your-project-knowledge-dir]/semantic/SEM-XX_<domain-name>_domain_model.md`

---

## 6-Chapter Structure (required)

### Chapter 1 Overview (required)

| Section | Content | Required/optional |
| :--- | :--- | :--- |
| 1.1 Domain purpose | Why this domain exists (do not write from table names) | Required |
| 1.2 Primary domain terms | Definition of the ubiquitous language | Optional (may be omitted if terms are self-evident) |
| 1.3 Per-route management model | Comparison table across business routes (e.g., direct sales / teacher / partner) | Required when route differences exist |
| 1.4 Primary table list | Table name, model file, role, physical DB, managing party | Required |

### Chapter 2 ER diagram (required)

- erDiagram format (mermaid)
- Business meaning on the relationship lines
- PK/FK notation: `int id PK`, `int society_id FK`, composite is `int groupsno PK,FK`
- When spanning multiple databases, add a "cross-system join keys" section

### Chapter 3 Per-table column definitions (required)

- A "business meaning" column for every required column
- Column selection criteria: required (flags, foreign keys, business branching) / batch-describable (general management) / omittable (no business meaning)
- When omitted, state the fact of omission

### Chapter 4 Flag / pattern table (required)

- 3 columns: value, business meaning, constant name
- Describe not only "0/1/2" but also "what it means"

### Chapter 5 Business pitfalls (required)

- At least 3: T-1, T-2, T-3
- Attach a code source (file path:line number) to each

### Chapter 6 SQL samples (required)

- Purpose comment required
- Soft-delete condition required (every soft-deletable table; e.g., delflag='0')
- PostgreSQL syntax

---

## Header Format

```markdown
# SEM-XX <domain-name> Semantic Model

> **Semantic model number**: SEM-XX
> **Domain**: <domain-name>
> **Created**: YYYY-MM-DD
> **Precision**: real code investigation (<investigated repository>)
> **SSOT**: this file is the source of truth for the conceptual model, ER diagram, and flag-value definitions of SEM-XX
```

---

## Quality Criteria

| Item | Criterion |
| :--- | :--- |
| Business meaning | Every required column of every table has a "business meaning" column |
| ER diagram | 0 errors in mermaid validation |
| Pitfalls | At least 3, each with a code source |
| SQL | Every query has a purpose comment and the soft-delete condition |
| Forbidden keywords | 0 |
| Unicode symbols | 0 outside code blocks |
