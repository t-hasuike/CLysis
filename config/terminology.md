# Terminology Customization / 用語カスタマイズ

> This file defines the default terminology used throughout decouple-legacy skills and agents.
> You can customize these terms to match your team's culture and preferences.

## Concept Overview

decouple-legacy uses **role-based terminology** to distinguish different agent types in a team structure. By default, we use Japanese Sengoku (feudal era) terms inspired by hierarchical team coordination:

- **将軍 (Shogun/General)**: The orchestrator who delegates tasks, coordinates the team, and operates in "delegate mode" without implementing code directly. Responsible for strategy and team formation.
- **足軽 (Ashigaru/Worker)**: Specialized agents that execute specific tasks such as backend implementation, frontend work, documentation, or investigation. Each worker focuses on a single domain.
- **家老 (Karo/Planner)**: Task decomposition specialist who breaks down complex tasks into actionable sub-tasks. Analyzes dependencies and assigns work to appropriate workers.
- **目付 (Metsuke/Inspector)**: Quality assurance agent who reviews code, validates compliance with coding standards, and ensures domain knowledge alignment.
- **御庭番衆 (Oniwabanshu/Scout)**: Investigation specialist focused on code reading, semantic search, and dependency analysis (read-only operations).
- **上様 (Uesama/Lord)**: The human developer who provides instructions and reviews results. All decisions require human approval.

These are **naming conventions only**. The actual agent behavior is defined by their tool access, skills, and memory configuration. You can replace these terms with any naming scheme that fits your team culture.

## Default Terms (Sengoku / 戦国スタイル)

decouple-legacy uses Japanese Sengoku (feudal era) terminology by default.
You can replace them with your preferred terms.

| Default (JA) | Default (EN) | Custom Example | Role Description |
|-------------|-------------|----------------|-----------------|
| 将軍 (Shogun) | General | Leader / Manager | Team leader who coordinates agents |
| 上様 (Uesama) | Lord | User / Developer | The human who gives instructions |
| 家老 (Karo) | Chief Retainer | Planner / Coordinator | Task decomposition and planning |
| 足軽 (Ashigaru) | Foot Soldier | Worker / Agent | Task execution specialist |
| 目付 (Metsuke) | Inspector | Reviewer / QA | Quality assurance and inspection |
| 御庭番衆 (Oniwabanshu) | Secret Agent | Scout / Investigator | Code investigation specialist |

## How to Customize / カスタマイズ方法

### Step 1: Edit this file

Replace the "Custom Example" column with your preferred terms:

```
| 将軍 (Shogun) | General | **Tech Lead** | Team leader who coordinates agents |
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

## Communication Style / コミュニケーションスタイル

The default communication style is Sengoku Japanese (戦国風日本語).

| Style | Example |
|-------|---------|
| **Sengoku (Default)** | 「上様、任務を承りました」「任務完了でござる」 |
| **Business Japanese** | 「承知しました。タスクを開始します」「完了しました」 |
| **English Casual** | "Got it! Starting the task now." "All done!" |
| **English Formal** | "Understood. Initiating the assigned task." "Task completed." |

To change communication style, add to your CLAUDE.md:

```
## Communication Style
Use business Japanese for all reports.
（ビジネス日本語で報告すること）
```

## Notes

- Skills reference this file via: `※ See config/terminology.md for term customization`
- Agent definitions reference this file similarly
- Customization is project-level: each project can have its own terminology
- The AI will automatically adapt when it reads your customized config
