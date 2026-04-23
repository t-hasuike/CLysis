# legacy-workflow

Process improvement skills for legacy system teams.

## Skills

| Skill | Description |
|-------|-------------|
| `/kpt` | KPT (Keep/Problem/Try) retrospective with Five Whys for recurring problems |
| `/empirical-prompt-tuning` | Bias-free skill definition evaluation and iterative improvement |

## Installation

```bash
claude plugin install legacy-workflow@CLysis
```

## Usage

### KPT Retrospective

Run at session boundaries or milestone completions:

```bash
/kpt              # Full retrospective (default)
/kpt --light      # Minimal version (1 Keep, 1 Problem, 1 Try)
/kpt --analyze    # Trend analysis of past 3 months
```

### Empirical Prompt Tuning

Evaluate and improve a specific skill definition:

```bash
/empirical-prompt-tuning current-spec
/empirical-prompt-tuning review-code
```

## Dependencies

These skills work independently but integrate with other CLysis plugins:

- `/kpt` references `/session-start` (legacy-investigation) for Try execution tracking
- `/empirical-prompt-tuning` references `/kpt` (this plugin) for recording improvement outcomes
