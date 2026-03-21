---
name: templates
description: Template collection for the leader (user inquiries, team launch examples, operation methods)
disable-model-invocation: true
user-invocable: true
argument-hint: template-name
---

> **Note: This is a reference template collection, not an executable skill. It provides ready-to-use templates for team leaders to copy and customize. AI agents do not invoke this skill directly.**

> This is a generic skill from [CLysis](https://github.com/t-hasuike/CLysis).
> Terminology can be customized via `config/terminology.md`.

# Leader Template Collection

See config/terminology.md for term customization

## User Approval Request

"Mission received.

[Mission] XXXX

[Analysis]
- Determined that YY is needed because of XX

[Team Composition]
- Worker A: XX assignment (Sonnet)
- Worker B: XX assignment (Sonnet)
- (Add as needed)

[Reason]
XXXX

Requesting approval."

## Team Launch Example

Create a team with TeamCreate and launch members with Tasks.

Specify the following for each member:
- subagent_type: Agent type (ashigaru-backend, ashigaru-frontend, etc.)
- team_name: Team name
- name: Member name
- model: sonnet (standard)
- prompt: Specific mission content

## Operation Methods

### Communicating with Team Members
- **Shift+Up/Down**: Select team member (in-process mode)
- **Shift+Tab**: Toggle delegate mode
- **Ctrl+T**: Toggle task list display

### Team Lifecycle

1. Team launch: Create team with TeamCreate -> Launch members with Tasks
2. During work: Monitor and adjust in delegate mode
3. After completion: Stop each member with SendMessage(type: shutdown_request) -> Delete resources with TeamDelete
