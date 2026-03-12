# CLAUDE.md Template for decouple-legacy

This is a minimal template for integrating decouple-legacy skills into your project.

---

```markdown
# CLAUDE.md - [Your Project Name]

## Overview
[Brief description of your project]

## Tech Stack
| Area | Technology |
|------|-----------|
| Backend | [e.g., Laravel, Rails, Spring Boot] |
| Frontend | [e.g., React, Vue, Angular] |
| Database | [e.g., PostgreSQL, MySQL] |

## Required Rules
1. [Project-specific rules, e.g., soft delete checks, type safety]
2. [Coding standards]

## Agent Team Configuration
[See config/terminology.md for role customization]

## Domain Knowledge
| File | Content |
|------|---------|
| `input/domain/business_rules.md` | Core business rules |
| `input/domain/data_models.md` | Data model specifications |
| `input/domain/integrations.md` | External system integrations |

## Repositories
| Repository | Path |
|-----------|------|
| [repo-name] | `/path/to/repo` |

## Pipeline
```
/project-guide [task] → /investigate → /service-spec → /impact-analysis
→ /propose-changes → /create-pr → Merge
```

Each transition includes a Human Checkpoint for review.
```

---

## Usage

1. Copy this template to your project root as `CLAUDE.md`
2. Fill in the placeholders with your project-specific information
3. Add your domain knowledge files to `input/domain/`
4. Start using decouple-legacy skills
