# CLAUDE.md Template for CLysis

This is a minimal template for integrating CLysis skills into your project.

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
| `knowledge/domain/business_rules.md` | Core business rules |
| `knowledge/domain/data_models.md` | Data model specifications |
| `knowledge/domain/integrations.md` | External system integrations |

## Repositories
| Repository | Path |
|-----------|------|
| [repo-name] | `/path/to/repo` |

## Pipeline
```
/project-guide [task] → /current-spec → /change-impact
→ /propose-changes → /create-pr → Merge
```

Each transition includes a Human Checkpoint for review.
```

---

## Usage

1. Copy this template to your project root as `CLAUDE.md`
2. Fill in the placeholders with your project-specific information
3. Add your domain knowledge files to `knowledge/domain/`
4. Start using CLysis skills
5. After completing Phase 0, refer to `docs/knowledge-system-guide.md` for the target file checklist.
