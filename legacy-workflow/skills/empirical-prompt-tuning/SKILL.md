---
name: empirical-prompt-tuning
description: Experimentally evaluate and improve skill definition quality. Uses bias-free separated evaluation and iterative improvement until convergence.
argument-hint: "<target skill name>"
---

> This is a generic skill from [CLysis](https://github.com/t-hasuike/CLysis).
> Terminology can be customized via `config/terminology.md`.
> Adapt paths and technology references to match your project.

# Empirical Prompt Tuning Skill

## Overview

Optimize skill definitions (SKILL.md) through bias-free separated evaluation and iterative improvement.

## Role Differentiation from Inspector

| Aspect | empirical-prompt-tuning | Inspector |
|--------|------------------------|-----------|
| Target | Skill definition files (SKILL.md) | Worker deliverables (reports, code) |
| Timing | During skill improvement | After deliverable creation |
| Criteria | Skill clarity, completeness, feasibility | Rule compliance, quality, accuracy |

## F002 Compliance

The leader receives and judges results only. All evaluation and improvement work is delegated to workers.

## Execution Steps

### Step 1: Baseline Evaluation (Worker A: Evaluator)

Read the target skill's SKILL.md and score on 5 axes (0-10):

| Axis | Description |
|------|-------------|
| Clarity | Instructions are unambiguous; workers can execute without hesitation |
| Completeness | All steps, criteria, and output formats are defined |
| Feasibility | Prerequisites, tools, and permissions are realistically available |
| Quality Guards | Prohibitions, checklists, and fallbacks are in place |
| Integration | Pre/post pipeline connections are clearly defined |

**Output**: Scores + weakness rationale (1-2 sentences per axis)

#### 1a. Weakness Rationale guidance

For axes scored < 7, follow this pattern:
- State what is missing or ambiguous (observation only)
- Reference a specific section or step in the SKILL.md
- Do NOT propose solutions (that is Worker B's responsibility in Step 2)

**Example (correct)**: "Step 2 does not specify how to select among multiple low-scoring axes"
**Example (incorrect)**: "Add a priority matrix to Step 2" (this is a recommendation, not an observation)

### Step 2: Improvement Proposal (Worker B: Improver)

Receive Step 1 evaluation results and create improvement proposals focusing on low-scoring axes:

#### 2a. Prioritization criteria

| Priority | Criteria | Action |
|----------|----------|--------|
| P1 (highest) | Axes with score < 5 | Must address |
| P2 | Axes with score 5-6 | Should address |
| P3 | Axes with score 7-8 | Address only if capacity remains |

Select up to 3 changes targeting P1 first, then P2, avoiding P3 unless critical.

#### 2b. Data inheritance from Step 1

Worker B must extract from Step 1 output:
- Axis scores → determine priority tier
- Weakness Rationale → identify specific gaps to address
- Section references → locate problem areas in SKILL.md

- Proposals must be specific additions/modifications to the SKILL.md
- Maximum 3 changes per improvement round (prevent over-engineering)
- Include rationale for each change
- Each change must trace back to a specific Step 1 weakness

#### 2c. Feasibility check before proposal

- [ ] Proposed change does not alter skill purpose/scope
- [ ] Change location exists in current SKILL.md
- [ ] Proposed text is actionable (not vague aspirational language)

**Output**: Improvement diff (old → new comparison) with traceability to Step 1 weakness

### Step 3: Re-evaluation (Worker C: Re-evaluator)

Re-evaluate the improved SKILL.md using the same 5 axes as Step 1.

**Important**: Worker C must be a separate agent from Workers A and B, evaluating without knowledge of the improvement process (bias prevention).

#### 3a. Quality gate checklist

Before scoring, Worker C must verify:
- [ ] Improved SKILL.md is syntactically valid Markdown
- [ ] New text does not contradict existing guidance
- [ ] Examples are concrete and actionable
- [ ] No circular dependencies in instruction flow

#### 3b. Re-evaluation focus

- Compare whether improvements directly address Step 1 weaknesses
- Flag "superficial" vs. "structural" improvements
- Provide detailed rationale for any axis still below 7

**Output**: Scores + weakness rationale for remaining < 7 axes

### Step 4: Convergence Check (Leader)

| Condition | Decision |
|-----------|----------|
| All axes >= 7 AND total improvement < 3 points | Converged → Step 5 |
| Any axis < 7 | Not converged → Return to Step 2 (max 3 rounds) |
| After 3 rounds still not converged | Force stop → Save current best |

#### 4a. Convergence criteria rationale

- **All axes >= 7**: No critical gaps remain
- **Total improvement < 3 points**: Signals diminishing returns
- **Max 3 rounds**: Follows Pareto principle — 80% of gains achieved in first 2 rounds

### Step 5: Save Results (Worker)

Save to `reports/YYYY.MM.DD_ept_{skill_name}.md` (F006 mandatory).

## Output Format

Save to: `reports/YYYY.MM.DD_ept_{skill_name}.md`

```markdown
# Empirical Prompt Tuning — {skill_name}

> Date: YYYY-MM-DD
> Target skill: {skill_name}
> Iterations: {N}

## Baseline Evaluation

| Axis | Score | Weakness Rationale |
|------|-------|-------------------|

## Improvement History

### Round {N}
| Location | Change | Rationale |
|----------|--------|-----------|

## Final Evaluation

| Axis | Baseline | Final | Improvement |
|------|----------|-------|-------------|

## Convergence
- Result: Converged / Not converged (force stopped)
- Total improvement: {N} points
```

## Prohibited Actions

- Leader performing evaluation or improvement directly (F002)
- Same worker handling both evaluation and improvement (bias risk)
- More than 3 iterations (diminishing returns)
- Changing the skill's purpose or scope (this is definition improvement, not redesign)

## Subsequent Skills

| Skill | Condition | Instruction |
|-------|-----------|-------------|
| `/kpt` | After improvement cycle completes | Record improvement effectiveness in KPT Keep or Try |

> **Fallback**: If the target skill does not exist, report to leader and await instructions.
