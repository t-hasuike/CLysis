---
name: session-start
description: Automate session context recovery. Aggregate previous incomplete tasks, in-progress work, and open issues to present the leader with "today's priority tasks."
argument-hint: "[--light (lightweight)] [--full (full, default)]"
---

# Session Start Skill

## Overview

Recovers context from previous sessions at the start of a new session. Aggregates the following information and reports to the leader:

- Previous session's incomplete tasks
- Current project state
- Open issues and their priorities
- Changes to knowledge/ since last session

## Trigger Conditions

- New session start
- Resume after long interruption
- Leader mentions "continue from last time"

## Execution Steps

### Step 1: Read knowledge/README.md
- Verify directory structure and references
- Check version/Last Updated for change detection

### Step 2: Read workspace/in_progress/ latest files
- Sort by modification date, read up to 3 files
- Extract "Next Action" / "Status" / "Priority" sections

### Step 3 (--full only): Check open issues
- Run `gh issue list --state open` for the knowledge repository
- Prioritize items with high-priority labels

### Step 4 (--full only): Check project session memory
- Find the latest `project_session_*.md` in memory
- Extract incomplete tasks and blockers

### Step 5: Generate and save context summary
- Generate report following the output format
- **Save to `reports/session_context/{YYYYMMDD}-session-start.md`** (mandatory)

## Modes

| Mode | Content | Scope |
|------|---------|-------|
| `--light` | Step 1 + Step 2 only (local files) | Local only |
| `--full` (default) | Step 1-4 (includes GitHub API) | Full scope |

## Output Format

```markdown
# Session Start Summary — {YYYY-MM-DD}

## Previous Incomplete Tasks
| Priority | Task | Status | Reference |
|----------|------|--------|-----------|

## Open Issues (priority order)
(--full only)

## knowledge/ Change Detection
- Last updated: {date}

## Question for Leader
"What are today's priority tasks?"
```

## Important Notes

1. **Planner consultation**: If complex tasks (spanning 2+ areas) are found, note that planner consultation is required before execution
2. **File save mandatory**: Output must be saved to `reports/session_context/`. stdout-only output is prohibited
3. **Fallback**: If GitHub API fails, fall back to --light mode and report the failure
4. **No hallucination**: Report only facts confirmed by actual file scanning

## Subsequent Skills (Pipeline)

| Skill | Condition | Instruction |
|-------|-----------|-------------|
| `/project-guide` | Starting a new task | Report to leader, obtain approval before executing |
| `/current-spec` | Continuing previous investigation | Report to leader, obtain approval before executing |

> **Fallback**: If previous incomplete tasks cannot be identified, report to leader: "No previous session records found. Start as new task?" and await instructions.
