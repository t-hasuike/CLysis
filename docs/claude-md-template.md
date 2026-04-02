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

## Leadership Flow (Shogun Protocol)

### Task-List Management (Orchestration)
- On receiving a directive, declare all sub-tasks first via TaskCreate
- Treat "consult Karo" as a task (F005 prevention)
- On each task start: TaskUpdate(in_progress); on completion: TaskUpdate(completed)
- Monitor in_progress tasks via TaskList to detect stalls before the user notices

## Safety Rules

| Rule ID | Rule | Enforcement |
|---------|------|-------------|
| F001 | [Project-specific escalation rule] | [How escalations are handled] |
| F002 | Leader does NOT implement code | Leader delegates to workers |
| F003 | No simultaneous file edits by multiple agents | Assign files to single owner |
| F004 | Leaving team unattended | Leader monitors progress and steers |
| F005 | Skip karo (planner) for large tasks | Leader MUST consult before delegating |
| F006 | Investigation results must be saved to files | Include output file path in delegations |
| F007 | Audit results must be saved to files | Save reports to reports/ directory |
| F008 | Direct push to main/master is prohibited | Always use branch + PR. Exception: initial commit only |

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
→ /create-pr --plan → /create-pr --exec → Merge
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
