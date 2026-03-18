---
name: build-knowledge
description: Extract domain knowledge from investigation results and systematically accumulate it in input/domain/. Used for knowledge retention after code reviews and investigations.
argument-hint: <investigation result summary or file path> [category]
---

# /build-knowledge Skill

> This is a generic skill from [CLysis](https://github.com/t-hasuike/CLysis).
> Terminology can be customized via `config/terminology.md`.

## Overview

Extract domain knowledge from investigation results (/investigate, /service-spec, /impact-analysis, /code-review outputs) and accumulate it as files under `input/domain/`.

**Important**: Domain knowledge is project-specific information and is NOT included in the public repository. Each project independently manages its own `input/domain/`.

## Why This Skill Is Needed

Insights gained from investigations and reviews tend to be lost. This skill enables:
- Establishing investigation results as **reusable domain knowledge**
- **Referencing as prior knowledge** in subsequent investigations, reviews, and implementations
- **Accumulating and sharing domain understanding** across the team

## Target

$ARGUMENTS

## Category List

| Category | Content | File Naming Example |
|----------|---------|-------------------|
| business-rules | Business rules and logic | `order_validation_rules.md` |
| data-structure | Data structures, DB design, Enum definitions | `product_categories.md` |
| integration | External API integration, external service specifications | `payment_gateway_spec.md` |
| architecture | System architecture, Service responsibilities, dependencies | `service_responsibilities.md` |
| constraints | Technical constraints, known limitations | `legacy_constraints.md` |

## Execution Steps

### Step 1: Analyze Investigation Results

Extract the following from input investigation results:
- **Confirmed specifications and business rules** (confirmed facts, not assumptions)
- **Discovered patterns** (code conventions, implicit rules)
- **Constraints and limitations** (technical constraints, external service limitations)

### Step 2: Check Existing Domain Knowledge

Search existing files under `input/domain/` to avoid duplication:

```
input/domain/
|- [check existing file list]
|- decide: new creation or update existing
```

**Decision criteria**:
- Within scope of existing file -> **Append to existing file**
- Outside scope of existing file -> **Create new file**
- Uncertain -> Confirm with leader

### Step 3: Generate/Update Domain Knowledge File

#### New Creation

Create file under `input/domain/` in the following format:

```markdown
# [Domain Knowledge Title]

> **Category**: [business-rules / data-structure / integration / architecture / constraints]
> **Created**: YYYY-MM-DD
> **Last Updated**: YYYY-MM-DD
> **Source**: [Source (PR number, investigation report name, etc.)]

## Overview

[1-3 sentence summary]

## Details

[Details of business rules, specifications, data structures, etc.]

### [Subsection]

[Structure with subsections as needed]

## Caveats

[Usage notes, exception cases, etc.]

## Change History

| Date | Description | Source |
|------|-------------|--------|
| YYYY-MM-DD | Initial version | [Source] |
```

#### Updating Existing

1. Append to appropriate section of existing file
2. Update `Last Updated`
3. Add to change history

### Step 4: Quality Check

- [ ] Documented only confirmed facts, not assumptions
- [ ] No contradictions with existing domain knowledge (report contradictions to leader)
- [ ] Category classification is appropriate
- [ ] Format is easily referenceable from other skills (/investigate, /code-review, etc.)

## Report Format

```
# Domain Knowledge Accumulation Report

## Accumulated Content

| Operation | File | Category | Content |
|-----------|------|----------|---------|
| New creation | input/domain/xxx.md | business-rules | Business rules for XX |
| Append | input/domain/yyy.md | data-structure | Data structure addition for YY |

## Source
- [Investigation report name or PR number]

## Implications for Future Investigations/Reviews
- [Suggest scenarios where this knowledge will be useful]
```

## Position in Pipeline

```
/investigate or /service-spec or /code-review
  -> Investigation/review complete
  |
/build-knowledge [investigation result summary]
  -> Established as domain knowledge
  |
Next /investigate or /code-review
  -> Referenced as prior knowledge from input/domain/
```

**Recommended timing**:
- After code review completion (when new business rules are discovered)
- After impact analysis completion (when system architecture and constraints become clear)
- After investigation completion (when implicit rules and patterns are discovered)

## Prohibited Actions

- Do not record assumptions or unverified information as domain knowledge
- Do not include personal opinions in domain knowledge
- Do not copy-paste code as domain knowledge (extract concepts and rules)

---

## I/O Specification

### INPUT
| Type | Description | Required/Optional | Example |
|------|-------------|-------------------|---------|
| Investigation results | Skill output or summary text | Required | `/investigate output`, `Price rules discovered in PR#123 review` |
| Category | Domain knowledge category | Optional | `business-rules`, `data-structure` |

### OUTPUT
| Type | Format | Destination |
|------|--------|-------------|
| Domain knowledge file | Markdown | New creation or update under `input/domain/` |
| Accumulation report | Markdown | stdout (report to leader) |

### Prerequisites
- `input/domain/` directory exists
- Investigation results are based on confirmed facts

### Downstream Skills (Pipeline)
- None (domain knowledge is referenced by all other skills)

### Quality Checkpoints
- [ ] Documented only confirmed facts
- [ ] No contradictions with existing domain knowledge
- [ ] Category classification is appropriate
- [ ] Source is documented
