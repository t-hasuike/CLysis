---
name: current-semantic
description: Create a semantic model for a target business domain. Describes entities, relationships, ubiquitous language, and business rules as the meaning of the domain, producing a single file that developers open first when working in that domain.
argument-hint: "[domain-name] [primary-table-names (space-separated, multiple allowed)] [--db primary-db|secondary-db]"
---

# /current-semantic -- Semantic Domain Model Skill

> This is a generic skill from [CLysis](https://github.com/t-hasuike/CLysis).
> Terminology can be customized via `config/terminology.md`.

## Overview

Create a semantic model (SEM-XX file) for a specified business domain.

**Purpose declaration**: This skill produces a "file that conveys the meaning of business operations." It is NOT a data dictionary that enumerates every column of every table. The goal is to create a single file that a developer touching this domain opens first to understand the business meaning.

**Axes to verify (self-check before execution)**:
1. Can you explain "why this entity exists"?
2. Are you conveying "what this value means" through a flag table?
3. Are you showing "how Route A / Route B / Route C differ" through contrast?
4. Are you avoiding a mere column listing? (Omit columns that carry no business meaning)
5. Are you NOT defining scope by physical DB location or row count?

## Role Assignment

| Role | Responsibility |
|------|---------------|
| **Shogun (General)** | Specifies target domain, delegates to Ashigaru, receives deliverable. Does not read code directly (F002 rule) |
| **Karo (Chief Retainer / Planner)** | Task decomposition and pre-analysis of domain boundaries when handling multiple domains simultaneously |
| **Ashigaru (Foot Soldier / Worker)** | Executor of this skill: code investigation, semantic model creation, PR creation |
| **Metsuke (Inspector)** | Quality audit of deliverable (symbol existence verification, business meaning description check, axis compliance check) |

> **F002 Rule**: Shogun (General) must not read code directly. All investigation and creation must be delegated to Ashigaru.

### Tone

Use a polite and clear business reporting style. State OK / NG plainly. When something is unknown, say so explicitly.

## Usage

```
/current-semantic [domain-name] [primary-table-names]
```

### Examples

| Timing | Command |
|--------|---------|
| Organization domain ([your-entity] / [your-entities]) | `/current-semantic organization [your-entity] [your-entities]` |
| Contract domain | `/current-semantic contract [contract-table]` |
| Secondary system domain | `/current-semantic partner-organization --db [secondary-db]` |

## Workflow

### Step 1: Identify Domain Boundaries and Business Concepts

**Purpose**: First define "what business concepts does a developer touching this domain need to understand?" Do NOT start by listing tables.

**Actions**:
1. Verify existence of domain name and primary tables (Bash ls / Glob)
2. Check boundaries with existing SEM files (`ls knowledge/domain/semantic/` to confirm SEM-XX list)
3. Identify management subject and physical DB ([primary-db] / [secondary-db])
4. Check for route differences (do behaviors differ across Route A / Route B / Route C?)

**Axis check (required before completing Step 1)**:
- [ ] Can you state in one sentence "what does a developer in this domain need to know first"?
- [ ] Have you defined scope by "complete range of business concept" rather than "physical DB location"?
- [ ] If route differences exist, can you explain them as differences in business models?

**Output**: Step 1 completion report (written explanation of domain boundary, target table list, presence/absence of route differences)

---

### Step 2: Code Investigation (Extract Business Meaning)

**Purpose**: Extract "business meaning" from code. Do NOT simply retrieve column names; understand "why that column exists."

**Actions**:
1. Investigate Model files (Serena find_symbol or Bash grep)
   - Obtain the full list of fillable columns
   - Collect constants and Enums (flag values, status values)
   - Understand related entities from relationships (HasOne, HasMany, BelongsTo)
   - Extract business rules from scope methods (scope*)
2. Investigate UseCase files (what changes through create/update flows)
3. When spanning multiple DBs: identify cross-system join keys
   - Always record the join key AND its business meaning (example: `primary-db.groups.id = secondary-db.institutions.core_group_id` means "an organization registered by a partner is automatically reflected in the groups table on the primary side")

**Full column investigation obligation**:
- Confirm ALL columns in fillable, hidden, and casts via Read. Sampling only "representative columns" from the beginning is prohibited.
- However, columns with self-evident business meaning (id PK, created_at, and other generic management columns) may be described collectively as "generic management columns."

**Axis check (required before completing Step 2)**:
- [ ] Can you explain "why this column exists" for each column?
- [ ] Have you obtained the "meaning" of flag values (what each value represents) from constant definitions?
- [ ] Have you marked columns whose business meaning is not self-evident as "needs verification"?
- [ ] When spanning multiple DBs, can you explain the business meaning of join keys?

---

### Step 3: Draft the 6-Chapter Structure

**Purpose**: Describe business meaning in a 6-chapter structure. Chapter organization follows "the order in which a developer understands the business."

#### Chapter Design Guidelines

Chapter 1 (Overview) is the most important. The goal is that a developer who reads it can grasp "the business structure of this domain."

| Chapter | Title | Purpose | Writing Axis |
| :--- | :--- | :--- | :--- |
| Chapter 1 | Overview | Help the reader grasp the domain's purpose, routes, and primary entities | Start with "why this domain exists." Do NOT start with table names |
| Chapter 2 | ER Diagram | Visualize relationships between entities | erDiagram format (mermaid). Add business meaning to relationship lines |
| Chapter 3 | Column Definitions by Table | Explain business meaning of each table's columns | Always include a "Business Meaning" column. Reference constants/Enum values here (details in Chapter 4) |
| Chapter 4 | Flag / Pattern Table | Show correspondence between flag/status values and business meaning | Basic 3 columns: value, meaning, constant name |
| Chapter 5 | Business Pitfalls | Prevent mistakes developers actually make | Minimum 3 required. Attach code evidence to each pitfall |
| Chapter 6 | SQL Samples | Present typical business queries | "Purpose comment" is mandatory for each query. Include your project's soft-delete condition |

#### Chapter 3 Column Selection Criteria

Confirm all columns in the investigation phase (Step 2 full column obligation). In the writing phase, select columns based on business meaning using the following criteria:

| Category | Column Type | How to Describe |
| :--- | :--- | :--- |
| Required | Flag/enum/status columns / Foreign keys / Columns involved in business branching | Describe one line per column with "Business Meaning" |
| Batch description allowed | Generic management columns (id PK, created_at, updated_at, your project's soft-delete flag, etc.) | Combine into one line as "Generic management columns (id, created_at, updated_at, [soft-delete-flag])" |
| Omissible | Columns with little business meaning (e.g., mechanical sequence numbers) | May be omitted, but if omitted, always note "N additional columns exist (judged as no business meaning)" |

> **Note**: The above is a guide for the writing phase only. The obligation to confirm all columns in the investigation phase (Step 2 L82-84) remains unchanged. "Omissible" does NOT mean investigation can be skipped.

#### Symmetric Structure When Route Differences Exist

When behavior differs across Route A / Route B / Route C, the aim is NOT to align headings. The aim is to accurately convey the difference in business models.

**Guidelines**:
- Declare route differences upfront in Chapter 1 with a contrast table (3-route explanation table)
- In Chapter 3, write column definitions for route-specific entities in separate subsections (e.g., 3.1 [route-A-entity], 3.2 [route-B-entity])
- Flags common across routes are defined collectively in Chapter 4. Route-specific flags are explained within each route's subsection
- When route differences represent a fundamental business model difference (e.g., different core entities per route), do not force symmetry

**When multiple routes coexist within a single entity**:

When a single table manages multiple routes (e.g., a table uses a `type` column where type=1 means Route A and type=2 means Route B), follow these rules:

- In the "Business Meaning" column for the relevant column, describe the meaning per route (e.g., write "1=Route A contract / 2=Route B contract" in the meaning field for the `type` column)
- When business meaning diverges significantly by route, split the Chapter 3 subsection (e.g., 3.1.1 Route A / 3.1.2 Route B)

**Additional chapter for multi-DB domains**:

For domains spanning multiple DBs ([primary-db] / [secondary-db]), add a "Cross-System Join Keys" section before the ER diagram in Chapter 2:

```
Chapter 2: Cross-System Join Keys (only when multiple DBs are involved)
  2.1 Inter-DB join key list (physical DB, table name, join key, business meaning)
  2.2 ER Diagram (including cross-DB relationships)
```

**Axis check (required before completing Step 3)**:
- [ ] Can a developer who reads Chapter 1 explain "the business structure of this domain"?
- [ ] Does Chapter 3 have a "Business Meaning" column for all tables?
- [ ] Does Chapter 4's flag table describe the meaning of values (not just "0/1/2" but "what they mean")?
- [ ] Are there at least 3 pitfalls in Chapter 5?
- [ ] Do SQL samples in Chapter 6 have purpose comments?

---

### Step 4: mermaid Verification (Required)

**Purpose**: Detect mermaid syntax errors in the ER diagram before PR creation.

**Note**: This step is solely for mermaid syntax verification. Business quality checks are completed in Step 3 axis checks.

**Actions**:
```
mmdc -i [created SEM-XX file] -o /tmp/sem_check.png
```

**PK/FK notation rules**:
- Composite PK/FK: `int groupsno PK,FK` (comma-separated, no space)
- Single PK: `int id PK`
- Single FK: `int [table]_id FK`

**If errors exist, return to Step 3 and fix. PR creation is prohibited while errors remain.**

**Axis check (required before completing Step 4)**:
- [ ] Confirmed 0 errors with mmdc command?
- [ ] Do ER diagram relationship lines accurately represent business relationships (1:1, 1:N, N:M)?

---

### Step 5: Prohibited Term Check and PR Creation

**Purpose**: Prevent prohibited terms from being included before PR creation to the canonical repository, and create the PR.

**Actions**:
1. Prohibited term check (confirm 0 results):
   ```
   grep -rn "[prohibited-term-1]\|[prohibited-term-2]\|[personal-path]" [path-to-canonical-repo]/knowledge/domain/semantic/SEM-XX_*.md
   ```
2. Git operations (use git -C pattern):
   ```
   git -C [path-to-canonical-repo] checkout -b docs/sem[number]-[domain-name]-domain
   git -C [path-to-canonical-repo] add knowledge/domain/semantic/SEM-XX_[domain-name]_domain_model.md
   git -C [path-to-canonical-repo] commit -m "docs: SEM-XX [domain-name] semantic model creation"
   gh pr create --repo [your-repo] --title "docs: SEM-XX [domain-name] semantic model" --body "..."
   ```

**No `#` comments in Bash commands**: Do not include `#` comments in git or gh commands. Provide explanations as separate text.

**Axis check (required before completing Step 5)**:
- [ ] Confirmed prohibited term grep returns 0 results?
- [ ] Does the PR title and body explain the purpose of the semantic model (conveying business meaning)?

---

## Output Format (Chapter Structure Template)

Deliverable file path: `knowledge/domain/semantic/SEM-XX_[domain-name]_domain_model.md`

```markdown
# SEM-XX [Domain Name] Semantic Model

> **Semantic Model Number**: SEM-XX
> **Domain**: [Domain Name]
> **Created**: YYYY-MM-DD
> **Accuracy**: Based on actual code investigation ([investigated repository])
> **SSOT**: This file is the canonical source for SEM-XX conceptual model, ER diagram, and flag value definitions

---

## Chapter 1: Overview

### 1.1 Domain Purpose

[Why this domain exists from a business perspective. Explain "what concept this is for" in 1-3 sentences. Do NOT start from table names.]

### 1.2 [Primary Domain Vocabulary (optional)]

[As required by Axis 2 "Ubiquitous Language," describe primary domain terms (e.g., [EntityA] / [EntityB] / [EntityC]). Recommend one-line format explaining the business meaning of each term. This section may be omitted if terms are self-evident.]

### 1.3 [When route differences exist] Route-Based Management Model

| Route | Managed Entity | Management UI | Key Business Characteristics |
| :--- | :--- | :--- | :--- |
| Route A | [table name] | [management UI] | [business rule specific to this route] |
| Route B | [table name] | [management UI] | [business rule specific to this route] |
| Route C | [table name] | [management UI] | [business rule specific to this route] |

[If no route differences exist, omit this section and describe primary entity list in 1.3]

### 1.4 Primary Table List

| Table Name | Model File | Role | Physical DB | Managing Party |
| :--- | :--- | :--- | :--- | :--- |
| [table name] | [Model file] | [business role in one sentence] | [primary-db] / [secondary-db] | [managing party] |

**Out-of-scope tables** (another SEM is SSOT):
- [table name]: [why it is out of scope]. See [SEM-XX] for details

---

## Chapter 2: [Multi-DB only] Cross-System Join Keys

### 2.1 Inter-DB Join Keys

| DB A | Table.Column | DB B | Table.Column | Business Meaning |
| :--- | :--- | :--- | :--- | :--- |

### 2.2 ER Diagram

[If no multi-DB span, write the entire Chapter 2 as "Chapter 2: ER Diagram" with only the ER diagram]

```mermaid
erDiagram
    [TableA] {
        int id PK
        int [foreign-key] FK
        string [column-name]
    }
    [TableB] {
        int [tableA_id] PK,FK
    }
    [TableA] ||--o{ [TableB] : "[business relationship description]"
```

---

## Chapter 3: Column Definitions by Table

### 3.1 [Table Name] ([one-word business role])

[Supplement the business role of this table in 1-2 sentences]

| Column | Type | Business Meaning | Source |
| :--- | :--- | :--- | :--- |
| id | int PK | [business meaning] | [Model file L[line]] |
| [column] | [type] | [business meaning: what the value represents, under what conditions it changes, etc.] | [source] |

**[When supplementary notes are needed]**: [Special notes on soft-delete, timestamp naming conventions, etc.]

---

## Chapter 4: Flag / Pattern Table

### 4.1 [table].[column] ([one-word business role of the flag])

| Value | Business Meaning | Constant Name | Source |
| :--- | :--- | :--- | :--- |
| 0 | [meaning] | [CONSTANT_NAME or "no constant"] | [source] |
| 1 | [meaning] | [CONSTANT_NAME or "no constant"] | [source] |

**Note**: [Business notes when using this flag]

---

## Chapter 5: Business Pitfalls

### T-1: [Pitfall Title]

[Detailed explanation of the pitfall. Describe "why it is a pitfall" and "how to avoid it." Attach code evidence (Model file L[line])]

| [Comparison Axis] | [Option A] | [Option B] | Source |
| :--- | :--- | :--- | :--- |

### T-2: [Next Pitfall]

[Minimum 3 required. T-1 through T-3 are mandatory. Additional pitfalls in order of business importance]

---

## Chapter 6: SQL Samples

The following are all raw PostgreSQL SQL. Laravel's Eloquent global scopes are not automatically applied to raw SQL, so always manually add your project's soft-delete condition (e.g., `[soft-delete-flag] = '0'`).

### SQL-1: [purpose in one phrase]

[Purpose description: why this query is needed]

```sql
SELECT
    [columns]
FROM [table]
WHERE [table].[soft-delete-flag] = '0'
  AND [business condition]
ORDER BY [table].id ASC;
```

---

## Related Domains

- [Relative path to related SEM-XX file]: [description of relationship]

---

## Change History

| Date | Description |
| :--- | :--- |
| YYYY-MM-DD | Initial creation |
```

---

## Quality Checklist (Checklist to Ensure Axis Compliance)

Ashigaru confirms all items below before submitting deliverable to Shogun. Submit only when all items are "done."

### 6.1 Axis Compliance Check (Most Important)

| # | Check Item | Verification Method |
| --- | --- | --- |
| 1 | Can a developer who reads Chapter 1 explain "the business structure of this domain"? | Self-check: After reading Chapter 1, can you explain "why this entity exists"? |
| 2 | Is it avoiding a column listing (data dictionary)? | Verify: Does every column of every table have a "Business Meaning" column? Is the explanation not just "[column] column of [table]"? |
| 3 | Is ubiquitous language (business terminology) defined? | Verify: Does Section 1.2 of Chapter 1 define primary domain terms, or does the column explanation in Chapter 3 include definitions of business terms? |
| 4 | Are business rules described? | Verify: Are flag conditions, state transitions, and mandatory conditions described in Chapters 4 and 5? |
| 5 | Are route differences presented as differences in business models? | Verify: Are the differences across Route A / Route B / Route C explained as "differences in business meaning"? Not just "different tables"? |
| 6 | Is scope NOT defined by physical DB location or row count? | Self-check: Have you avoided the reasoning "this table is in [primary-db] therefore in scope"? Are you judging by "can the business concept be understood completely"? |
| 7 | When cross-system integration exists, is the business meaning explained? | Verify: Do multi-DB join keys have "Business Meaning" described? |

### 6.2 Technical Quality Check

| # | Check Item | Verification Method |
| --- | --- | --- |
| 8 | Were all columns actually confirmed (front-sampling prohibited)? | Verify: Is there evidence that all columns in fillable, hidden, and casts were confirmed via Read? |
| 9 | Were flag values confirmed from actual code? | Verify: Is there evidence that values were confirmed from constant definitions (const in Model file)? |
| 10 | Is mermaid PK,FK notation correct? | Verify: Is it `PK,FK` (comma-separated, no space)? |
| 11 | Was 0 errors confirmed by mmdc verification? | Verify: Is the mmdc command execution result included as-is in the report? |
| 12 | Were prohibited terms confirmed at 0? | Verify: Is the grep command execution result (0 results) included in the report? |
| 13 | Are there at least 3 pitfalls in Chapter 5? | Verify: Are T-1, T-2, and T-3 all written? |
| 14 | Do SQL samples in Chapter 6 have purpose comments? | Verify: Does each SQL have an explanation containing "Purpose:" as a comment? |
| 15 | Do SQL samples in Chapter 6 include your project's soft-delete condition? | Verify: For tables with soft-delete, is the soft-delete condition manually added in all SQL? |
| 16 | When columns with little business meaning are omitted, is the omission noted? | Verify: If omitted, is there a note like "N additional columns exist (judged as no business meaning)"? (See Step 3 column selection criteria) |
| 17 | When multiple routes coexist within a single entity, is the business meaning per route described? | Verify: When routes differ by a flag (e.g., type), is the meaning written as "1=[Route A] / 2=[Route B]" in the "Business Meaning" column? |

---

## I/O Specification

### INPUT

| Type | Content | Required/Optional | Example |
|------|---------|-------------------|---------|
| Domain name | Name of the target business domain | Required | `organization`, `contract` |
| Primary table names | Core table names (multiple allowed) | Required | `[entity-table] [related-table]` |
| --db option | Target DB (specify when spanning multiple DBs) | Optional | `--db [secondary-db]` |
| SEM number | Assigned number (assigned by Shogun) | Optional | `01`, `10` |

### OUTPUT

| Type | Format | Destination |
|------|--------|-------------|
| Semantic model | 6-chapter Markdown (ER diagram, column definitions, flag table, pitfalls, SQL samples) | Canonical repo's `knowledge/domain/semantic/SEM-XX_[domain-name]_domain_model.md` |
| Work report | Completion report including executed commands and verification results | stdout (report to Shogun) |

### Prerequisites

- Serena MCP is running
- Canonical repository clone is up to date (`git -C [path/to/repo] pull origin main`)
- Canonical repository clone is on main branch (no work branch remaining)

### Follow-up Skills (Pipeline)

| Skill | Condition | Instruction |
|-------|-----------|-------------|
| `/doc-check` | After SEM-XX PR is merged | Propose to Shogun to run consistency check with skill list in CLAUDE.md |

> **Fallback**: If mmdc command is unavailable, report to Shogun and request manual review. PR creation must be done only after mmdc verification.
