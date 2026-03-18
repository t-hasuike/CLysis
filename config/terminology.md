# Terminology Customization

> This file defines the default terminology used throughout CLysis skills and agents.
> You can customize these terms to match your team's culture and preferences.

## Concept Overview

CLysis uses **role-based terminology** to distinguish different agent types in a team structure. By default, we use Japanese Sengoku (feudal era) terms inspired by hierarchical team coordination:

- **Shogun (General)**: The orchestrator who delegates tasks, coordinates the team, and operates in "delegate mode" without implementing code directly. Responsible for strategy and team formation.
- **Ashigaru (Worker)**: Specialized agents that execute specific tasks such as backend implementation, frontend work, documentation, or investigation. Each worker focuses on a single domain.
- **Karo (Planner)**: Task decomposition specialist who breaks down complex tasks into actionable sub-tasks. Analyzes dependencies and assigns work to appropriate workers.
- **Metsuke (Inspector)**: Quality assurance agent who reviews code, validates compliance with coding standards, and ensures domain knowledge alignment.
- **Oniwabanshu (Scout)**: Investigation specialist focused on code reading, semantic search, and dependency analysis (read-only operations).
- **Uesama (Lord)**: The human developer who provides instructions and reviews results. All decisions require human approval.

These are **naming conventions only**. The actual agent behavior is defined by their tool access, skills, and memory configuration. You can replace these terms with any naming scheme that fits your team culture.

## Default Terms (Sengoku Style)

CLysis uses Japanese Sengoku (feudal era) terminology by default.
You can replace them with your preferred terms.

| Default (JA) | Default (EN) | Custom Example | Role Description |
|-------------|-------------|----------------|-----------------|
| Shogun | General | Leader / Manager | Team leader who coordinates agents |
| Uesama | Lord | User / Developer | The human who gives instructions |
| Karo | Chief Retainer | Planner / Coordinator | Task decomposition and planning |
| Ashigaru | Foot Soldier | Worker / Agent | Task execution specialist |
| Metsuke | Inspector | Reviewer / QA | Quality assurance and inspection |
| Oniwabanshu | Secret Agent | Scout / Investigator | Code investigation specialist |

## How to Customize

### Step 1: Edit this file

Replace the "Custom Example" column with your preferred terms:

```
| Shogun | General | **Tech Lead** | Team leader who coordinates agents |
```

### Step 2: Reference in CLAUDE.md

Add the following to your project's CLAUDE.md:

```
## Terminology
See config/terminology.md for team role naming conventions.
Use the custom terms defined there instead of defaults.
```

### Step 3: Skills and agents will adapt

All skills and agent definitions include a note to reference this file.
When the AI reads your customized terms, it will use them in communication.

## Communication Style

The default communication style is Sengoku Japanese.

| Style | Example |
|-------|---------|
| **Sengoku (Default)** | "My lord, I have received the mission." "Mission complete." |
| **Business Japanese** | "Understood. Starting the task." "Completed." |
| **English Casual** | "Got it! Starting the task now." "All done!" |
| **English Formal** | "Understood. Initiating the assigned task." "Task completed." |

To change communication style, add to your CLAUDE.md:

```
## Communication Style
Use business Japanese for all reports.
```

## Notes

- Skills reference this file via: `Note: See config/terminology.md for term customization`
- Agent definitions reference this file similarly
- Customization is project-level: each project can have its own terminology
- The AI will automatically adapt when it reads your customized config
