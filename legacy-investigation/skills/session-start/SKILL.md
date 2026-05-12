---
name: session-start
description: Automate session context recovery. Aggregate previous incomplete tasks, in-progress work, and open issues to present today's priority tasks.
argument-hint: "[--light (lightweight)] [--full (full, default)]"
---

# Session Start Skill

## Overview

Recovers context from previous sessions at the start of a new session. Aggregates the following information and reports to Shogun (General) so today's tasks can be prioritized efficiently:

- Previous session's incomplete tasks
- Current project state
- Open issues and their priorities
- Changes to knowledge/ since last session

## Role Assignment

| Role | Responsibility |
|------|---------------|
| **Shogun (General)** | Decides when to invoke this skill, receives the report, and determines today's priorities |
| **Ashigaru (Foot Soldier / Worker)** | Executes this skill. Scans actual files to aggregate context information and generates / saves the report |
| **Metsuke (Inspector)** | Verifies the output file exists and checks for hallucination |

> **File save mandatory**: Output must be saved to `reports/session_context/`. stdout-only output is prohibited.

## Trigger Conditions

- New session start
- Resume after long interruption
- Uesama (Lord) mentions "continue from last time"

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

### Step 3 (--full only): Check open Issues in the project repository

**Purpose**: Identify open GitHub Issues and their priorities.

**Actions**:
- Run `gh issue list --repo <owner>/<repo> --state open`
- Extract title, labels, and priority from results
- Prioritize items with these labels:
  - `priority: high`
  - `priority: critical`
  - `blocked`

**Fallback (A-006)**:
- On GitHub API failure: automatically fall back to `--light` mode
- Error message: "Could not check GitHub Issues. Reporting with local information only."

### Step 4 (--full only): Check project session memory

**Purpose**: Retrieve incomplete tasks and blockers recorded in the previous session.

**Actions**:
- Check the `~/.claude/projects/<project-id>/memory/` directory
- Sort `project_session_*.md` files by modification date (descending)
- Read the latest 1 file
- Extract "Incomplete Tasks", "Blockers", "Next Steps" sections

**Output fields**:
- Previous session date
- Recorded priority tasks
- Blockers (including items awaiting action from others)

### Step 4.5 (--full only): Verify execution of Try items from previous KPT

**Purpose**: Surface the execution status of Try items (improvement actions) recorded in the previous KPT retrospective so Shogun (General) can judge whether they were carried out.

**Actions**:
- Locate the latest KPT file (e.g., `ls -t reports/*_kpt.md | head -1`)
- Extract the `## Try` section from that file
- Pull the following columns from the Try table:
  - Try ID (e.g., T1, T2)
  - Linked Problem ID (e.g., P1, P2)
  - Try content
  - Owner (e.g., Shogun, Karo, ashigaru-scribe, ashigaru-investigator)
  - Deadline (milestone-style: before next session start, before Phase 4 kickoff, etc.)
  - Completion verification method (file existence check, grep pattern, git log check, etc.)

**Fallback**:
- KPT file not found: output "No previous KPT" and continue
- Try section empty: output "No previous Try items"

**Output fields**:
- Try table
- Note for Shogun (General): "Status judgment (completed / partially executed / not executed / no effect) is performed by Shogun in line with the KPT skill definition. Do not auto-classify."

### Step 5: Generate and save context summary

**Purpose**: Integrate all collected information into a report and present it to Shogun (General).

**Actions**:
- Integrate information from Steps 1-4 (and Step 4.5 in --full mode)
- Generate report using the standard format (below)
- Save to: `reports/session_context/{YYYYMMDD}-session-start.md`
- Deliver standard report to Shogun (General)

**Output file**:
- `reports/session_context/{YYYYMMDD}-session-start.md` (required, file save mandatory)

## Mode Specification

| Mode | Steps Executed | Scope | Estimated Time |
|------|---------------|-------|---------------|
| `--light` | Step 1 + Step 2 only (local file scan) | Local only | Short |
| `--full` (default) | Steps 1-4 + Step 4.5 (includes GitHub API) | Full scope | Moderate |

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
| <owner>/<repo> | #NN | [title] | priority: high, blocked | [URL] |
| ... | ... | ... | ... | ... |

**Notes**: Only priority: high / critical shown. Other labeled issues noted if present.

### Previous Session Record
- Previous session date: {YYYY-MM-DD}
- Record file: MEMORY.md > project_session_*.md
- Incomplete tasks:
  - [item 1]
  - [item 2]
- Blockers: [if any]

### Previous KPT Try Execution Status (--full only)

| Try ID | Linked Problem | Try Content | Owner | Deadline | Verification Method | Status (filled in by Shogun) |
|--------|---------------|-------------|-------|----------|---------------------|------------------------------|
| T1 | P1 | [summary] | ashigaru-scribe | before next session | [method] | not yet executed |
| T2 | P2 | [summary] | Karo | before Phase 4 kickoff | [method] | not yet executed |

**Note**: Status judgment (completed / partially executed / not executed / no effect) is performed by Shogun (General) in line with the KPT skill definition. Do not auto-classify; defer to Shogun's visual judgment.

## Recommendations for This Session

> **Question for Shogun (General)**
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
**Version**: 1.0
```

## Notes (Inspector Findings Reflected)

### A-003: Planner consultation note

If complex tasks (spanning 2+ areas, multiple repositories, or requiring impact analysis) are found in the output summary, append the following note:

> **Important**: Consult Karo (Chief Retainer / Planner) before executing this task. Decomposing complex tasks and impact analysis are Karo's responsibility.

### A-004: Mandatory file save (file save mandatory)

- Output must be saved to `reports/session_context/{YYYYMMDD}-session-start.md`
- A stdout report text is also produced, but file save is required
- A session start without a saved file is treated as a failure

### A-006: GitHub API fallback

On GitHub API failure:

1. Detect the failure and automatically fall back to `--light` mode
2. Record "GitHub API: Fallback (connection failed)" in the output report
3. Report to Shogun (General): "Could not check GitHub Issues. Reporting with local information only."
4. Continue processing -- complete the report with Step 1-2 information

### Hallucination Prevention

- Record only facts confirmed by actual file scanning
- Do not interpolate incomplete tasks or task content with guesses
- If a file is not found, explicitly state "No matching file found"
- Do not record uncertain information

---

## Prohibited Actions

- Modifying files or editing code (this skill's purpose is information aggregation and reporting only)
- Guessing or interpolating task content (report only actual file facts)
- Returning stdout only without file save (file save mandatory)

---

## I/O Specification

### INPUT

| Type | Content | Required | Example |
|------|---------|----------|---------|
| Mode | Execution mode | Optional | `--light`, `--full` (default) |

### OUTPUT

| Type | Format | Destination | Required |
|------|--------|-------------|----------|
| Session start summary | Markdown | `reports/session_context/{YYYYMMDD}-session-start.md` | Yes (file save mandatory) |
| Shogun (General) report text | Standard report format | stdout | Yes |

### Preconditions

- `workspace/in_progress/` directory exists
- `reports/session_context/` directory exists (create if missing)
- MEMORY.md exists (--full only)

### Subsequent Skills (Pipeline)

| Skill | Condition | Instruction |
|-------|-----------|-------------|
| `/project-guide` | Starting a new task | Report to Shogun (General), obtain approval before executing |
| `/current-spec` | Continuing previous investigation | Report to Shogun (General), obtain approval before executing |
| `/change-impact` | Impact analysis needed for complex task | Consult Karo (Chief Retainer / Planner) before executing |

### Fallback Rules

**GitHub API connection failure**:
- During `--full` execution, on detecting a connection failure, automatically fall back to `--light` mode results
- Record "GitHub API: Fallback" in the output report
- Continue processing

**File not found**:
- If a target file is not found, output "No matching file found"
- Continue processing. Other steps still execute

## Quality Checkpoints

- [ ] `reports/session_context/{YYYYMMDD}-session-start.md` was created
- [ ] File contains frontmatter (generation date, mode, API status)
- [ ] All information from Steps 1-4 and Step 4.5 is aggregated (for --full mode)
- [ ] No hallucination (no guessed or interpolated content)
- [ ] Complex tasks include the Karo (Planner) consultation note (A-003)
- [ ] Priority ordering is reasonable

> Note: See `config/terminology.md` for term customization.
