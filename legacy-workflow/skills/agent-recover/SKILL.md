---
name: agent-recover
description: Diagnose and recover stalled async agent tasks. Performs viability check via output file inspection, then executes idempotent restart or work granularity analysis.
argument-hint: "[--phase1-only (viability check)] [--phase3-restart (idempotent restart)] [--full (full recovery flow)]"
---

> This is a generic skill from [CLysis](https://github.com/t-hasuike/CLysis).
> Terminology can be customized via `config/terminology.md`.
> Adapt paths and technology references to match your project.

# Async Agent Recovery Skill

## Overview

When async agents (field workers, strategist, auditor) do not respond or report completion for extended periods, this skill provides a unified recovery procedure: viability assessment from output file inspection → idempotent restart → work granularity analysis.

This skill operates on three core principles:
- **Output file path as viability source**: Determine wait vs. restart based on file existence and modification timestamp
- **Idempotence guarantee**: On restart, recover existing output file and prevent duplicate execution
- **Granularity splitting assessment**: After 2 failed restart attempts, evaluate whether task scope is too large and requires decomposition

---

## Target Scenarios

| Scenario | Condition | Assessment |
|----------|-----------|------------|
| **Abnormal Termination** | Agent returns internal error or silently exits | Dead state. Restart only option |
| **Hanging State** | Tool use ID returned but no completion report. No intermediate files | Dead state. Waiting is futile. Restart required |
| **Long-Running Task** | Output file partially generated, modification timestamp recent | Alive state. Waiting is correct. Provide additional time |

---

## Execution Flow

### Phase 1: Viability Assessment (Lightweight File Check)

**Objective**: Determine if agent is alive and making progress, or is dead

**Procedure**:
1. Confirm output file path specified at delegation time. Verify absolute path format and rule out memory error via redundant check
2. `ls <output_path>` to confirm file existence
3. On file existence: `ls -la <output_path>` to check modification timestamp (understand time elapsed since last update)
4. Classify result into one of the following:

| Check Result | Assessment | Next Phase |
|--------------|-----------|-----------|
| File exists, modification timestamp recent (≤5 min) | **Alive (Long-Running Task)** → Phase 2-A (Wait) |
| File exists, old timestamp (first check only), progress indicators in working directory (work_log etc.) | **Alive (Potential Hanging State)** → Phase 2-B (Progress Check) |
| File does not exist OR timestamp unchanged (≥5 min), no progress indicators | **Dead state** → Phase 3 (Idempotent Restart) |

**Key Point**: "Reasonable execution time" should reference time estimate at delegation. Typical agent tasks: 5–30 sec, large grep: 30 sec–2 min, multiple Reads: 1–5 min.

---

### Phase 2-A: Long-Running Task (Wait Assessment)

**Assessment**: File modification timestamp is recent, task is in progress

**Action**:
1. Check token consumption (leader can monitor via TaskList. For strategist/auditor, estimate from planned work content)
2. Calculate remaining time. If within token budget, continue waiting
3. If token budget low, evaluate granularity splitting: pause current execution and decompose into smaller subtasks to resubmit

**Completion Condition**: Agent reports normally (output file reaches final state, agent response received)

---

### Phase 2-B: Progress Indicator Check (Hanging State Verification)

**Assessment**: File timestamp is old but progress indicators exist (work_log, partial file generation)

**Procedure**:
1. List progress indicators: work_log, partial files, uncommitted git changes
2. Check last modification time of progress indicators. If extremely old (multiple hours), consider compaction collision or hanging state
3. Based on assessment:
   - Progress indicators still updating (log entries appending): Merge into Phase 2-A (Wait)
   - Progress halted, exceeds reasonable execution time: Proceed to Phase 3 (Idempotent Restart)

---

### Phase 3: Idempotent Restart (Dead State Recovery)

**Assessment**: Phases 1 and 2 confirmed dead state

**Prerequisite**: Delegation prompt specified output path, and [feedback_worker_stall] principle "always specify output path" is satisfied

**Restart Prompt Elements (Mandatory)**:
```
【Async Agent Restart】

Previous task execution appears unresponsive. Requesting retry under idempotent conditions.

【Output Path】
<originally specified path>

【Idempotence Guarantee】
- Step 1: ls output path to confirm file existence
- Step 2: If file exists, Read content and verify current state
- Step 3: If file exists, continue from current state (no overwrite, no duplicate append)
- Step 4: If file does not exist, execute fresh

【Original Delegation Content】
<original task description>

Thank you.
```

**Post-Restart Assessment** (Phase 4):
- After restart, wait same timeout as initial submission (typically 3–5 min)
- Confirm file update / agent response
- Assessment result:
  - **Success**: File updated OR completion report received → Continue normal flow (auditor invocation, leader report, etc.)
  - **No response again**: Proceed to Phase 5 (Granularity Splitting Assessment)

---

### Phase 4: Double Failure and Granularity Splitting Assessment

**Assessment**: Idempotent restart also resulted in no response

**Analysis Checklist**:
- [ ] Is output path correct? No typos or relative path misuse?
- [ ] Are filesystem permissions sufficient? Parent directory writable?
- [ ] Are tool invocations (Bash, Read, Write) constrained by timeout or limits?
- [ ] Is task scope appropriate? (e.g., repo-wide grep — can target be narrowed?)
- [ ] Has agent model / context limit been exceeded?

**Granularity Splitting Decision Matrix**:

| Indicator | Assessment | Action |
|-----------|-----------|--------|
| Output path exists and writable, no error reports | No functional issue. Task granularity may be too large | Split task and resubmit. Example: 1000-file grep → 10 batches of 100 files |
| Output directory missing OR permission denied | Environmental blocker | Create directory or confirm permissions. Outside this skill scope. Address separately |
| Tool call malformed / internal error | Agent framework bug or input format error | Simplify delegation prompt. Consolidate commands to single line. Remove shell comments (#) |
| 2 restart attempts both failed | Recovery impossible | Report to leader. Explore alternative approaches (manual implementation, skill integration, etc.) |

**Splitting Example** (Large grep into 3 parts):

```
Task: "Find 'specific keyword' in /path/to/repo, report count and matching lines"

Split plan:
  1) Target /path/to/repo/.claude/ only
  2) Target /path/to/repo/knowledge/ only
  3) Target /path/to/repo/reports/ only

Submit each split in parallel, leader aggregates results
```

---

## Checkpoints and Quality Verification

### Leader-Side Checklist

- [ ] Did you specify output path in absolute form at start of delegation prompt?
- [ ] Did you document idempotence requirement: "recover existing output file, continue from that state"?
- [ ] Are task definitions consistent between initial submission and restart (no condition changes)?
- [ ] Is timeout prediction realistic? (Avoid unjustified assumptions like "should complete in 30 seconds")

### Agent-Side Self-Check (At Restart)

- [ ] Output path verification: ls to confirm, assess file existence
- [ ] Idempotence check: understand existing file content, avoid overwrite risk
- [ ] Error handling: if tool call fails, consider alternative approach (different tool)
- [ ] Completion report: after file save, always include path in status message

---

## Prohibited Practices and Antipatterns

| Prohibited | Reason | Alternative |
|-----------|--------|------------|
| Resubmit same agent with same prompt 3+ times | Identical conditions won't succeed. Verify preconditions first (permissions, file state) | Granularity split OR verify permissions before retry |
| Inject new task without resolving stall (no stall recovery) | Resource double-consumption, confusion | Complete viability assessment before new task |
| Leave agent hanging and assume "it will respond eventually" | Hanging state never resolves. Time waste | Use viability assessment to confirm dead state, then restart |
| Attempt granularity split for blocker (permission denied) | Root cause won't resolve via split | Remove blocker first, then retry |

---

## Troubleshooting

### Q: Output file exists but content is old. Uncertain about viability assessment.

**A**: Follow this sequence:
1. `ls -la <file>` to check modification timestamp. Understand exactly when last update occurred
2. **Calculate elapsed time from now**: If ≤5 min (or within predicted task time), assess as alive; if beyond, investigate further
3. **Check partial files and work_log**: Look in same directory for progress files. If found, indicates alive state (possible mid-pause)
4. **Check git status**: If in git repo, verify for uncommitted changes (possible mid-process state)
5. **Document assessment rationale**: Record judgment reason in output file header (audit transparency)

---

### Q: Idempotent restart still has no response. How much should I decompose?

**A**:
1. **First split (after 2 failures)**: Reduce task volume to 50–70% (recommend 3-way split)
2. **If 3 failures emerge**: Further reduce. But excessive granularity creates overhead (more invocation calls)
3. **Judgment unclear**: Report to leader and request task redesign. Consider outside this skill scope

---

### Q: File exists, but agent returns an error. How should viability assessment change?

**A**:
- **internal error / malformed / framework errors**: Abnormal termination. Dead state. Phase 3 idempotent restart
- **Tool call timeout / permission denied**: Environmental blocker. Address via granularity split or permission check. Not resolvable within this skill
- **User input error (grep no match)**: Not abnormal termination; normal completion. Recipient handles result

---

## Update History

| Date | Version | Change |
|------|:-------:|--------|
| 2026-06-19 | 1.0 (EN) | English translation from generic skill base v1.0. Phases 1–4, checkpoints, prohibited practices, troubleshooting adapted to CLysis style |

