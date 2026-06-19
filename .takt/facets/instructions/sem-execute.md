<!-- This instruction facet is based on the TAKT framework (https://github.com/nrslib/takt), MIT License, Copyright (c) 2026 Masanobu Naruse. -->
# SEM Execute - SEM Document Creation Procedure

## Overview

Based on the plan in sem-plan.md, create the semantic model document (SEM-draft.md) following the steps of the /current-semantic skill (see legacy-knowledge/skills/current-semantic).

---

## Procedure

### Step 1: Confirm the plan

Read sem-plan.md and grasp the following before starting to write:
- The target table list and exclusions
- The boundary against existing SEMs
- Whether route differences exist
- Prerequisite knowledge (with sources)

### Step 2: Code investigation (extracting business meaning)

For each target table, Read the Model file and confirm:
- **All columns** of fillable / hidden / casts (no sampling of only the first rows)
- Constants and Enums (flag values, status values)
- Relations (HasOne, HasMany, BelongsTo)
- Business rules expressed via scope methods (scope*)

Investigate the UseCase files and confirm what changes in the registration/update flows.

When the domain spans multiple databases, always record the business meaning of the cross-system join keys.

**Evidence of all-column investigation**: Append the commands and results (count, matching lines) used in the investigation to the end of SEM-draft.md.

### Step 3: Create the 6-chapter structure

Create SEM-draft.md in the following 6-chapter structure:

| Chapter | Title | Required content |
| :--- | :--- | :--- |
| Chapter 1 | Overview | Domain purpose, route differences (if any), primary table list |
| Chapter 2 | ER diagram | erDiagram format (mermaid), business meaning on relationship lines |
| Chapter 3 | Per-table column definitions | "Business meaning" column for every table; follow the column selection criteria |
| Chapter 4 | Flag / pattern table | 3 columns: value, meaning, constant name |
| Chapter 5 | Business pitfalls | At least 3 entries; code source for each |
| Chapter 6 | SQL samples | Purpose comment required; soft-delete condition required |

**Axes to confirm (keep asking yourself while writing)**:
1. Why does this entity exist?
2. What does this value mean?
3. How does it differ across business routes (e.g., direct sales / teacher / partner; Route A / B / C)?
4. Has it become a bare list of columns?
5. Is the scope decided by the physical location of tables rather than business concepts?

### Step 4: mermaid validation

Validate the ER diagram (chapter 2) of the created SEM-draft.md with the mermaid CLI:

```bash
mmdc -i <path to SEM-draft.md> -o /tmp/sem_check.png
```

Fix any errors. **Confirm 0 errors before proceeding to the next step.**

**PK/FK notation rules**:
- Composite PK/FK: `int groupsno PK,FK` (comma-separated, no space)
- Single PK: `int id PK`
- Single FK: `int society_id FK`

### Step 5: Forbidden-keyword check

Confirm with grep that the following pattern is not contained in SEM-draft.md:

```bash
grep -rn "Users\/" <path to SEM-draft.md>
```

In addition, refer to the forbidden keywords defined for your project (internal names, service-specific terms, API keys, personal paths, etc.; see [your-project-standards-doc]) and similarly confirm 0 occurrences with grep.

Confirm 0 occurrences before submitting SEM-draft.md.

---

## File path of the deliverable (SEM-draft.md)

`[your-project-knowledge-dir]/semantic/SEM-XX_<domain-name>_domain_model.md`

Pre-submission checklist:
- [ ] Confirmed all columns with Read (no first-rows sampling)
- [ ] Every table has a "business meaning" column
- [ ] Chapter 5 has at least 3 pitfalls
- [ ] Chapter 6 SQL has purpose comments and the soft-delete condition (e.g., delflag='0')
- [ ] Confirmed 0 errors with the mermaid CLI
- [ ] Forbidden-keyword grep returned 0 (Users/ + project-specific terms from [your-project-standards-doc])
- [ ] Recorded the investigation trail (commands, results) at the end
