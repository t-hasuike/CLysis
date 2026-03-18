# Domain Knowledge Organization Template

## Usage

Use when organizing investigation reports (output/) into domain knowledge (input/domain/).

```
"Organize output/xxx.md according to the following template,
and save as input/domain/xxx.md"
```

---

## Template

```markdown
# [Domain Name]

**Last Updated**: YYYY-MM-DD
**Source**: [Investigation report path]

## Overview
[Explain in 1-2 sentences]

## Definitions

| Term | Definition |
|------|-----------|
| ... | ... |

## Mapping Table

| Name | Code | Value | Notes |
|------|------|-------|-------|
| ... | ... | ... | ... |

## Business Rules

1. [Rule 1]
2. [Rule 2]

## Constraints and Caveats

- [Constraint 1]
- [Constraint 2]

## Related Files

- `input/domain/related-domain.md`
- `input/project/related-project-info.md`
```

---

## Extraction Guidelines

### Information to Keep
- Definitions and terminology
- Mapping tables
- Business rules
- Constraints and exceptions
- Specific values and codes

### Information to Remove
- Investigation process and history
- Explanations like "we investigated..."
- Temporary analysis
- Duplicate information

---

## Example: Product Category Domain Knowledge

```markdown
# Product Categories

**Last Updated**: 2026-01-22
**Source**: output/sample_investigation.md

## Overview
Definitions and mapping table of product categories handled in the target system.

## Mapping Table

| Name | Code | Description | Notes |
|------|------|-------------|-------|
| Standard | STD | Standard plan | Default |
| Premium | PRM | Premium plan | With options |
| Enterprise | ENT | Corporate plan | Custom pricing |

## Business Rules

1. When selecting a category, reference the category master table
2. Prices are defined per category in the `price` table

## Constraints

- Enterprise is available only through specific sales channels
- When changing categories, related price tables must also be updated
```
