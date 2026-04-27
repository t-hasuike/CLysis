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

## Role Assignment

| Role | Responsibility |
|------|---------------|
| **Leader** | Decides when to invoke this skill. Receives the report and determines today's priorities |
| **Planner** | Consulted if complex tasks (spanning 2+ areas) are found in the context summary |
| **Worker** | Executes this skill. Scans actual files to aggregate context information and generates/saves the report |
| **Inspector** | Verifies the output file exists, checks for hallucination, and confirms rule compliance |

> **File save mandatory**: Output must be saved to `reports/session_context/`. stdout-only output is prohibited.

## Trigger Conditions

- New session start
- Resume after long interruption
- Leader mentions "continue from last time"

## Usage

```
/session-start
/session-start --light
/session-start --full
```

### Usage Examples

| Timing | Command |
|--------|---------|
| New session start | `/session-start` (default --full) |
| Resume after interruption | `/session-start --full` |
| Lightweight (local info only) | `/session-start --light` |
| GitHub API unavailable | `/session-start --light` (fallback) |

## Execution Steps

### Step 1: Read knowledge/README.md

**Purpose**: Verify directory structure and references; detect major structural changes since the last session.

**Actions**:
- Read the full `knowledge/README.md` file
- Extract the Last Updated date from the Version section
- Check for directory structure discrepancies

**Output fields**:
- Last updated date
- Change detection result ("Changed since last session" / "No changes")

### Step 2: Read workspace/in_progress/ latest files

**Purpose**: Identify in-progress tasks and extract their current state and next actions.

**Actions**:
- List all `.md` files in `workspace/in_progress/`
- Sort by modification date (descending)
- Read up to 3 files
- Extract "Next Action" / "Status" / "Priority" sections from each

**Output fields**:
- Task name, priority, current status, reference file name
- Next Action (if explicitly stated)

### Step 3 (--full only): Check open issues

**Purpose**: Identify open GitHub Issues and their priorities.

**Actions**:
- Run `gh issue list --repo {your-project-repo} --state open`
- Extract title, labels, and priority from results
- Prioritize items with these labels:
  - `priority: high`
  - `priority: critical`
  - `blocked`

### Step 4 (--full only): Check project session memory

**Purpose**: Retrieve incomplete tasks and blockers recorded in the previous session.

**Actions**:
- Check the `{memory-directory}` directory
- Sort `project_session_*.md` files by modification date (descending)
- Read the latest 1 file
- Extract "Incomplete Tasks", "Blockers", "Next Steps" sections

**Output fields**:
- Previous session date
- Recorded priority tasks
- Blockers (including items awaiting action from others)

### Step 5: Generate and save context summary

**Purpose**: Integrate all collected information into a report and present it to the leader.

**Actions**:
- Integrate information from Steps 1-4
- Generate report using the standard format (below)
- Save to: `reports/session_context/{YYYYMMDD}-session-start.md`
- Deliver standard report to leader

## Mode Specification

| Mode | Steps Executed | Scope | Estimated Time | When to Use |
|------|---------------|-------|---------------|-------------|
| `--light` | Step 1 + Step 2 only (local file scan) | Local only | Short | GitHub API unavailable; quick status check |
| `--full` (default) | Steps 1-4 (includes GitHub API) | Full scope | Moderate | Standard session start; resume after interruption |

Default is `--full`. If GitHub API fails during `--full` execution, automatically falls back to `--light` results.

## Output Format

Generated file: `reports/session_context/{YYYYMMDD}-session-start.md`

```markdown
# Session Start Summary -- {YYYY-MM-DD}

## Overview
State aggregation at the start of this session. Summarizes progress, blockers, and open issues since the previous session.

## State Changes Since Last Session

### knowledge/ Update Status
- Last updated: {date}
- Changes: {Changed / No changes / {updated items}}

### In-Progress Tasks (workspace/in_progress/)

| Priority | Task | Status | Reference | Next Action |
|----------|------|--------|-----------|-------------|
| High | [task name] | Paused | workspace/in_progress/xxx.md | [next action] |
| Medium | ... | ... | ... | ... |

**Notes**: [blockers, dependencies if any]

### Open Issues (--full only, priority order)

| Repository | # | Title | Labels | Reference |
|-----------|---|-------|--------|-----------|
| {repo} | #NN | [title] | priority: high, blocked | [URL] |
| ... | ... | ... | ... | ... |

**Notes**: Only priority: high / critical shown. Other labeled issues noted if present.

### Previous Session Record
- Previous session date: {YYYY-MM-DD}
- Record file: {memory-directory}/project_session_*.md
- Incomplete tasks:
  - [item 1]
  - [item 2]
- Blockers: [if any]

## Recommendations for This Session

> **Question for Leader**
>
> Based on the above, what are today's priority tasks?
>
> Suggested priority order (for reference):
> 1. Issues with priority: high or critical labels
> 2. Previous session's incomplete tasks (no blockers)
> 3. New tasks

## Execution Environment

- Execution time: {ISO 8601}
- Mode: --light / --full
- GitHub API: Connected / Fallback (connection failed)

---

**Generated by**: /session-start skill
```

## Fallback Rules

### GitHub API Connection Failure

1. Upon detecting connection failure during `--full` mode, automatically fall back to `--light` mode
2. Record in output report: "GitHub API: Fallback (connection failed)"
3. Report to leader: "Could not check GitHub Issues. Reporting with local information only."
4. Processing continues -- complete the report with Step 1-2 information

### File Not Found

- If a target file is not found, output "No matching file found"
- Processing continues. Other steps are still executed

### Empty workspace/in_progress/

- If the directory is empty or does not exist, report "No in-progress tasks found"
- Processing continues with remaining steps

## I/O Specification

### INPUT

| Type | Content | Required | Example |
|------|---------|----------|---------|
| Mode | Execution mode | Optional | `--light`, `--full` (default) |

### OUTPUT

| Type | Format | Destination | Required |
|------|--------|-------------|----------|
| Session start summary | Markdown | `reports/session_context/{YYYYMMDD}-session-start.md` | Yes |
| Leader report text | Standard report format | stdout | Yes |

### Preconditions

- `workspace/in_progress/` directory exists (or can be empty)
- `reports/session_context/` directory exists (create if missing)
- Memory directory exists (--full only)

## Quality Checkpoints

- [ ] `reports/session_context/{YYYYMMDD}-session-start.md` was created
- [ ] File contains frontmatter (generation date, mode, API status)
- [ ] All information from Steps 1-4 is aggregated (for --full mode)
- [ ] No hallucination (no guessed or interpolated content)
- [ ] Complex tasks include planner consultation note
- [ ] Priority ordering is reasonable

## Important Notes

1. **Planner consultation**: If complex tasks (spanning 2+ areas) are found, note that planner consultation is required before execution
2. **File save mandatory**: Output must be saved to `reports/session_context/`. stdout-only output is prohibited
3. **Fallback**: If GitHub API fails, fall back to --light mode and report the failure
4. **No hallucination**: Report only facts confirmed by actual file scanning. Do not guess or interpolate task content

## Prohibited Actions

- Modifying files or editing code (this skill's purpose is information aggregation and reporting only)
- Guessing or interpolating task content (report only actual file facts)
- Returning stdout only without file save

## Subsequent Skills (Pipeline)

| Skill | Condition | Instruction |
|-------|-----------|-------------|
| `/project-guide` | Starting a new task | Report to leader, obtain approval before executing |
| `/current-spec` | Continuing previous investigation | Report to leader, obtain approval before executing |
| `/change-impact` | Impact analysis needed for complex task | Consult planner before executing |

> **Fallback**: If previous incomplete tasks cannot be identified, report to leader: "No previous session records found. Start as new task?" and await instructions.
