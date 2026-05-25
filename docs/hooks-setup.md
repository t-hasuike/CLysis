# Hooks Setup Guide

CLysis provides two hook scripts that enhance the AI agent experience through dynamic context injection and periodic reflection prompts.

## Scripts

| Script | Hook Event | Purpose |
|--------|-----------|---------|
| `scripts/context_inject.py` | `UserPromptSubmit` | Inject relevant feedback memory and knowledge file paths based on prompt keywords |
| `scripts/mini_reflection.py` | `PostToolUse` | Trigger a reflection prompt every 15 tool calls to encourage pattern recognition and skill creation |

---

## Dynamic Context Injection (UserPromptSubmit)

Add to your `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ./scripts/context_inject.py",
            "timeout": 3
          }
        ]
      }
    ]
  }
}
```

---

## Mini Reflection (PostToolUse)

Add to your `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ./scripts/mini_reflection.py",
            "timeout": 3
          }
        ]
      }
    ]
  }
}
```

---

## Combined Configuration

To enable both hooks simultaneously:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ./scripts/context_inject.py",
            "timeout": 3
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ./scripts/mini_reflection.py",
            "timeout": 3
          }
        ]
      }
    ]
  }
}
```

---

## How It Works

### context_inject.py

Analyzes the user's prompt keywords and automatically injects relevant feedback memories and knowledge file paths into the system context before each response.

**Keyword categories and mapped resources:**

| Keywords | Injected Resources |
|----------|--------------------|
| present, proposal, approval, option, decision | `feedback_decision_format.md`, `feedback_uesama_presentation_substantive_review.md` |
| delegate, worker, task, assign | `feedback_worker_stall.md`, `feedback_hallucination_prevention.md` |
| PR, pull request, commit, push | `feedback_metsuke_pr_check.md` |
| compare, analysis, impact | `feedback_comparison_task_karo.md` |
| KPT, retrospective | `feedback_kpt_parallel_task_identification.md` |
| mermaid, diagram, flowchart | `feedback_mermaid_syntax_pitfalls.md` |
| hypothesis, error, bug, debug | `feedback_hypothesis_check.md` |
| print, fulfillment, delivery | `knowledge/domain/pr3_fulfillment/` |
| contract, price, pricing | `knowledge/domain/pr2_contract/` |
| event, photo, upload | `knowledge/domain/pr3_service_use/` |
| sales, incentive, finance | `knowledge/domain/pr3_sales_incentive/` |

**Configuration via environment variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `CLYSIS_MEMORY_DIR` | Auto-detected from `~/.claude/projects/*/memory/` | Override memory directory path |
| `CLYSIS_KNOWLEDGE_DIR` | `./knowledge` (project root relative) | Override knowledge directory path |

### mini_reflection.py

Tracks tool usage count per session in `/tmp/clysis_reflection/` and triggers a reflection prompt every 15 tool calls.

**Reflection prompt content:**
- Recent 15-call tool pattern summary (top 3 most-used tools)
- Three reflection questions:
  - "Are you repeating the same work pattern? Consider creating a skill."
  - "Are you deviating from the original objective?"
  - "Is there a learning worth saving to feedback memory?"

**Counter storage:**
- Location: `/tmp/clysis_reflection/tool_count_<session_id>.json`
- Automatically cleaned up by the OS on reboot
- Resets per session (no cross-session accumulation)

---

## Inspiration

These hooks were inspired by the [Hermes Agent](https://github.com/NousResearch/hermes-agent) three-tier memory system and GEPA optimization approach described in the [Hermes Agent Masterclass](https://blog.dailydoseofds.com/p/hermes-agent-masterclass) by Akshay Pachaar.

The core idea: AI agents benefit from periodic self-reflection and contextual memory injection to maintain goal alignment and build reusable knowledge over time.
