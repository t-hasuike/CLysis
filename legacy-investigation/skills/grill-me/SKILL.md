---
name: grill-me
description: Act purely as a "questioner" against tasks, plans, and designs. Surface undecided decisions, unnoticed assumptions, and avoided trade-offs through the power of questions alone. No code is written.
argument-hint: "<task summary or file path>"
---

# Grill Me Skill

## Overview

AI acts strictly as a **questioner** (not a reviewer). Instead of providing answers or recommendations, it uses questions to force articulation of:

- Undecided decisions
- Unnoticed assumptions
- Avoided trade-offs

## Key Principles

- **Question only**: Never provide answers, suggestions, or recommendations
- **Respectful tone**: "Let me confirm..." style, not aggressive
- **Forced exit**: User can say "enough" or "done" to immediately end
- **7-8 questions max**: Present all at once (not one-by-one)

## Trigger Conditions

- User presents a new task, requirement, or design
- Before large-scale changes or new features
- User says "I want to validate requirements" or "let's check assumptions"

## Execution Steps

### Step 1: Context Collection
- Read the task summary or referenced files
- Scan related knowledge/ files
- Check related GitHub Issues

### Step 2: Generate Questions (7-8 questions)

One question per category:

| Category | Question Intent |
|----------|----------------|
| Scope | "What is included/excluded from the scope?" |
| Assumptions | "Is this assumption correct: ...?" |
| Priority | "What is most important? What trade-off would you accept?" |
| Risk | "What is the worst case? What is the fallback?" |
| Dependencies | "What must be completed before this?" |
| Completion criteria | "What defines 'done'?" |
| Stakeholders | "Who is affected by this change?" |
| Technical constraints | "Are there performance/compatibility/security constraints?" |

**Important**: Skip questions already answered by context. Note "Skipped: already confirmed from context."

### Step 3: Await User Responses

### Step 4: Save Results

Output format:
```markdown
# Grill Results — {task summary}

> Date: {YYYY-MM-DD}
> Target: {task summary}

## Confirmed Items (Q&A pairs)

### 1. Scope
**Q**: {question}
**A**: {user's answer}

(continue for each category)

## Skipped Questions
- {question}: {reason}

## Handoff to Subsequent Skills
- Scope: {confirmed}
- Assumptions: {confirmed}
- Priority: {confirmed}
- Risk: {confirmed}
- Completion criteria: {confirmed}
```

Save to: `reports/grill/{YYYYMMDD}-{topic}.md`

## Prohibited Actions

- Writing or editing code
- Providing solutions, improvements, or recommendations
- Denying or evaluating user's answers
- Asking more than 8 questions
- One-by-one Q&A format (must present all at once)

## Subsequent Skills (Pipeline)

| Skill | Condition | Instruction |
|-------|-----------|-------------|
| `/create-pr --plan` | Modification task | Report to leader with grill results file, obtain approval |
| `/change-impact` | Impact analysis needed | Report to leader with grill results file, obtain approval |
| `/project-guide` | Task type undetermined | Propose to leader, await judgment |

> **Fallback**: If user says "enough" or "done", immediately save results at that point and propose subsequent skills.
