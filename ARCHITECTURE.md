# ARCHITECTURE

**Project**: decouple-legacy
**Version**: 1.0
**Last Updated**: 2026-03-06

---

## Design Philosophy

> **"Humans review and approve. AI investigates, analyzes, and proposes changes. Quality is maintained, users experience what they should expect."**

This is the core principle of decouple-legacy:

1. **AI does the heavy lifting** — Investigation, analysis, dependency tracking, report generation
2. **Humans retain control** — Review AI outputs, approve changes, verify quality
3. **Quality is non-negotiable** — AI proposes, humans approve, quality tools verify
4. **Legacy codebases become manageable** — Systematic workflows replace ad-hoc exploration

---

## Plugin Architecture

decouple-legacy is organized into **4 modular plugins**, each with specialized skills and commands:

```
legacy-investigation/      # Phase 1: Investigation & Understanding
├── .claude-plugin/
├── skills/               # project-guide, investigate, service-spec
├── commands/             # /investigate-flow, /bug-hunt, /understand
└── examples/

legacy-analysis/          # Phase 2: Analysis & Planning
├── .claude-plugin/
├── skills/               # impact-analysis, legacy-analyze
├── commands/             # /deep-dive
└── examples/

legacy-execution/         # Phase 3: Execution & Review
├── .claude-plugin/
├── skills/               # propose-changes, create-pr, code-review
├── commands/             # /implement, /review
└── examples/

legacy-knowledge/         # Knowledge Management
├── .claude-plugin/
├── skills/               # build-knowledge, templates
├── prompts/              # Domain knowledge templates
└── examples/
```

### Plugin Dependencies

```
legacy-knowledge (foundational)
    ↓ Provides domain knowledge templates
legacy-investigation
    ↓ Provides investigation results
legacy-analysis
    ↓ Provides impact analysis
legacy-execution
    ↓ Proposes changes and creates PRs
```

---

## Skill vs Command Design

### Skills
- **Purpose**: Atomic, reusable tasks (SKILL.md format)
- **Invocation**: `/skill-name [args]`
- **Location**: `{plugin}/skills/{skill-name}/SKILL.md`
- **Example**: `/investigate [target]` — Find and analyze specific code

### Commands
- **Purpose**: Multi-step workflows (pipeline of skills)
- **Invocation**: `/command-name [args]`
- **Location**: `{plugin}/commands/{command-name}.md`
- **Example**: `/investigate-flow [target]` → Runs `/project-guide` + `/investigate` + `/service-spec` + `/impact-analysis`

**Key Difference**: Commands orchestrate skills into end-to-end workflows with human checkpoints.

---

## Workflow Phases

decouple-legacy follows a three-phase workflow with **human checkpoints** at each transition:

```
Phase 0: Information Preparation (Human)
  │ Prepare domain knowledge & project context
  │ /build-knowledge, /project-guide
  │
  ├─ 【Human Checkpoint】Is the prepared information sufficient?
  │
  ▼
Phase 1: Investigation & Analysis (AI)
  │ /investigate-flow → pipeline: /investigate → /service-spec → /impact-analysis
  │
  ├─ 【Human Checkpoint】Are the investigation results correct?
  │
  ▼
Phase 2: Change Proposal & PR Creation (AI)
  │ /implement → pipeline: /propose-changes → (human review) → /create-pr
  │
  ├─ 【Human Checkpoint】Are the proposed changes appropriate?
  │
  │ /create-pr
  │
  ├─ 【Human Checkpoint】PR review & approval
  │
  ▼
Merge → Implementation Complete
```

### Phase 0: Information Preparation (Human)

**Purpose**: Prepare the foundation for AI-driven analysis.

**Human responsibilities**:
- Gather domain knowledge and business rules
- Define project structure and configuration
- Document schemas, constraints, and conventions
- Use `/build-knowledge` to extract and formalize information

**Checkpoint**: Is the prepared information sufficient for AI to proceed?

---

### Phase 1 (Current): Investigation → Analysis → Proposal

The current implementation focuses on **read-only analysis** with **human-approved changes**.

```
┌─────────────────────────────────────────────────────────────┐
│                  Phase 1 Workflow (Current)                  │
└─────────────────────────────────────────────────────────────┘

User defines task
   ↓
/project-guide → Context-aware document reference
   ↓
/investigate → Semantic code search
   ↓
/service-spec → Detailed specification
   ↓
/impact-analysis → ADR report with risks
   ↓
Human reviews report & decides next action
```

**Key characteristics**:
- AI investigates and analyzes
- AI generates structured reports (ADR format)
- Humans review and decide based on reports
- Domain knowledge accumulates over time

**Checkpoint**: Are the investigation results correct and complete?

---

### Phase 2 (Current): Automated Change Proposals

Extend Phase 1 with **AI-generated code proposals** for human review.

```
┌─────────────────────────────────────────────────────────────┐
│                  Phase 2 Workflow (Current)                  │
└─────────────────────────────────────────────────────────────┘

[Phase 1 investigation complete]
   ↓
/propose-changes → AI generates code diffs
   ↓
Human reviews proposed changes
   ↓ (if approved)
/create-pr → AI creates PR with ADR context
   ↓
Human merges after CI/CD passes
```

**Available skills**:
- `/propose-changes` — Generate code diffs with context
- `/create-pr` — Create PR with ADR summary and checklist

**Safety mechanisms**:
- All changes require explicit human approval
- PR includes full ADR report for review
- CI/CD must pass before merge

---

### Phase 3 (Future): Idea Refinement

Extend Phase 2 with **multi-agent deliberation** for high-stakes decisions.

```
┌─────────────────────────────────────────────────────────────┐
│                  Phase 3 Workflow (Future)                   │
└─────────────────────────────────────────────────────────────┘

User proposes idea (e.g., "Refactor authentication layer")
   ↓
Multi-agent team debates:
   • Agent A: Security perspective
   • Agent B: Performance perspective
   • Agent C: Maintainability perspective
   ↓
Agents generate competing proposals
   ↓
Leader synthesizes proposals → Best-of-breed recommendation
   ↓
Human reviews synthesis & selects approach
   ↓
[Phase 2 workflow for implementation]
```

**Use cases**:
- Architectural decisions
- Security-critical changes
- Large-scale refactoring

---

## Agent Team Architecture

### Roles (Sengoku / 戦国 Style by Default)

| Role (JA) | Role (EN) | Responsibility | Modifiable via config/terminology.md |
|-----------|-----------|----------------|-------------------------------------|
| **上様 (Uesama)** | Lord / User | The human who gives instructions | Yes |
| **将軍 (Shogun)** | General / Leader | Team coordination, task delegation | Yes |
| **家老 (Karo)** | Chief Retainer / Planner | Task decomposition, dependency management | Yes |
| **足軽 (Ashigaru)** | Foot Soldier / Worker | Task execution (backend, frontend, docs, investigation, devops) | Yes |
| **目付 (Metsuke)** | Inspector / QA | Quality assurance, compliance verification | Yes |

### Hierarchy & Communication

```
上様 (User)
  │
  ▼ Gives instructions
将軍 (Leader)
  │
  ├─ Requests team formation approval from User
  ├─ Creates agent team after approval
  ├─ Delegates tasks to workers
  ├─ Operates in delegate mode (Shift+Tab)
  │
  ▼ Natural language communication
┌────────────────────────────────────────┐
│         Agent Team Members             │
├────────────────────────────────────────┤
│  家老 (Planner) — Large task breakdown │
│  足軽 (Workers) — Execution            │
│  目付 (Inspector) — Quality audit      │
└────────────────────────────────────────┘
  │
  ▼ Shared resources
┌────────────────────────────────────────┐
│  • Shared task list (TaskCreate/Update)│
│  • Natural language messaging          │
│  • Domain knowledge (input/domain/)    │
│  • Reports (output/)                   │
└────────────────────────────────────────┘
```

---

## Domain Knowledge Separation

**Public vs. Private**:

| Directory | Visibility | Contents |
|-----------|-----------|----------|
| `legacy-*/skills/` | **Public** | Generic, reusable skills for any project |
| `legacy-*/commands/` | **Public** | Generic workflow pipelines |
| `agents/` | **Public** | Generic agent definitions (customize via CLAUDE.md) |
| `config/` | **Public** | Terminology customization |
| `input/domain/` | **Private** | Project-specific domain knowledge (NOT in repo) |
| `input/project/` | **Private** | Project-specific configuration (NOT in repo) |
| `output/` | **Private** | Generated reports (NOT in repo) |

**Why this separation?**

- **Generic skills and commands** work across projects (e.g., /investigate, /investigate-flow)
- **Project-specific knowledge** stays local (business rules, schema, constraints)
- `/build-knowledge` bridges the gap by extracting domain knowledge from investigations

---

## Terminology Customization

decouple-legacy uses **Sengoku (feudal Japanese)** terminology by default, but supports full customization.

### How to Customize

Edit `config/terminology.md`:

```markdown
| Default (JA) | Default (EN) | Your Custom | Role Description |
|-------------|-------------|-------------|-----------------|
| 将軍 (Shogun) | General | **Tech Lead** | Team leader who coordinates agents |
| 足軽 (Ashigaru) | Foot Soldier | **Engineer** | Task execution specialist |
```

All skills and agents reference this file for term adaptation.

### Communication Styles

| Style | Example |
|-------|---------|
| **Sengoku Japanese** (default) | 「上様、任務を承りました」 |
| **Business Japanese** | 「承知しました。タスクを開始します」 |
| **English Casual** | "Got it! Starting the task now." |
| **English Formal** | "Understood. Initiating the assigned task." |

To change style, add to your project's CLAUDE.md:

```markdown
## Communication Style
Use business Japanese for all reports.
```

---

## Extension Guide

### Adding New Skills

1. Choose the appropriate plugin:
   - **legacy-investigation**: Code understanding and exploration
   - **legacy-analysis**: Impact analysis and planning
   - **legacy-execution**: Code changes and PR workflows
   - **legacy-knowledge**: Knowledge extraction and templates

2. Create skill directory:
   ```
   {plugin}/skills/your-skill/
   ├── SKILL.md       # Skill definition with frontmatter
   ```

3. Frontmatter format:
   ```yaml
   ---
   name: your-skill
   description: Brief description
   argument-hint: <arg1> [arg2]
   ---
   ```

4. Keep generic:
   - Use placeholders like "Backend framework" instead of "Laravel"
   - Reference "input/domain/" without assuming project structure
   - Add note: `> This is a generic skill from decouple-legacy.`

5. Document I/O spec:
   - **INPUT**: What arguments does it take?
   - **OUTPUT**: What does it produce?
   - **Dependencies**: What does it require (Serena, GitHub MCP, etc.)?

6. Update plugin.json:
   - Add skill to the plugin's `plugin.json`
   - Run `python3 validate_plugins.py` to verify

### Adding New Commands

1. Create command file:
   ```
   {plugin}/commands/your-command.md
   ```

2. Frontmatter format:
   ```yaml
   ---
   name: your-command
   description: Brief description of the workflow
   ---
   ```

3. Define the pipeline:
   ```markdown
   ## Pipeline
   1. /skill-1 [args]
   2. 【Human Checkpoint】Review results
   3. /skill-2 [args]
   4. Output to output/your-command-report.md
   ```

4. Keep generic:
   - Reference skills by name, not file paths
   - Use placeholders for project-specific values
   - Document human checkpoints clearly

### Adding New Agents

1. Create agent definition:
   ```
   agents/your-agent.md
   ```

2. Frontmatter format:
   ```yaml
   ---
   name: your-agent
   description: Role description
   tools: Read, Write, Edit, Bash, Grep, Glob
   disallowedTools: (optional)
   model: sonnet | haiku
   skills: [skill1, skill2]
   memory: project
   ---
   ```

3. Keep generic:
   - Reference "Backend framework" instead of specific tech
   - Reference "input/domain/" and "input/project/" generically
   - Add note: `> This is a generic agent from decouple-legacy.`

4. Document communication:
   - **作業手順** (Workflow steps)
   - **報告形式** (Report format)
   - **言葉遣い** (Communication style, if applicable)

### Adding Examples

1. Create example directory:
   ```
   examples/your-example/
   ├── README.md       # Scenario description
   ├── input/          # Sample inputs
   └── output/         # Expected outputs
   ```

2. Anonymize project-specific details:
   - Replace real company names with placeholders
   - Redact sensitive business logic
   - Keep structure intact for learning

---

## Agent Pattern Mapping

decouple-legacy implements common AI agent patterns:

| Pattern | Implementation | Phase |
|---------|---------------|-------|
| **Advanced RAG** | schema.duckdb + Serena MCP | All phases |
| **ReAct** (Reasoning + Acting) | /investigate, /service-spec | Phase 1 |
| **Self-Reflection** | metsuke agent audit | Phase 2 (legacy-analyze) |
| **Multi-Agent Collaboration** | Leader + Workers + Inspector | All phases |
| **Plan-and-Execute** | /impact-analysis + Phase decomposition | Phase 1 |
| **Knowledge Graph Memory** | input/domain/ + diagrams/ | Phase 3 (legacy-analyze) |
| **Sequential Chain** | Phase 0→1→2→3 iteration | /legacy-analyze |

---

## Human Checkpoints

Every phase transition requires human confirmation. This ensures the core philosophy:
**"AI investigates, analyzes, and proposes — Humans review and approve."**

| Checkpoint | When | What to Verify |
|------------|------|-----------------|
| After Phase 0 | Information preparation complete | Domain knowledge is sufficient, project context is accurate |
| After Phase 1 | Investigation & analysis complete | Investigation results are correct, analysis is thorough |
| After /propose-changes | Change proposal ready | Proposed diffs are appropriate, test plan is adequate |
| After /create-pr | PR created | Code quality, test results, ready to merge |

**Why checkpoints matter**:
- **Prevents hallucinations** — Humans verify AI findings before proceeding
- **Maintains quality** — Human judgment ensures output meets standards
- **Preserves control** — Humans retain final decision authority
- **Builds trust** — Transparency at each step builds confidence in the workflow

---

## Quality & Safety

### Quality Gates

1. **Serena Memory Enforcement**:
   - `coding_standards` — Coding conventions
   - `security_guidelines` — OWASP Top 10, injection prevention
   - `code_style_conventions` — Style consistency
   - `task_completion_checklist` — Completion criteria

2. **Human Approval**:
   - Team formation requires user approval (F001)
   - File changes require user review before execution
   - PR creation requires explicit user consent

3. **Agent Audit**:
   - metsuke agent verifies all outputs
   - Checks for hallucinations (non-existent methods, files)
   - Validates compliance with project rules

### Safety Rules

| Rule ID | Rule | Enforcement |
|---------|------|-------------|
| F001 | Team formation requires user approval | Leader MUST request approval before creating team |
| F002 | Leader does NOT implement code | Leader delegates to workers |
| F003 | No simultaneous file edits by multiple agents | karo (planner) enforces file-level task splitting |

---

## Technology Requirements

### Required

- **Claude Code** (AI agent platform)

### Recommended

- **Serena MCP** — Semantic code analysis (symbol search, file overview)
  - Enables token-efficient code exploration
  - Avoids reading entire files unnecessarily

### Optional

- **GitHub MCP** — PR review, issue tracking
- **schema.duckdb** — Database schema analysis (generated via custom script)

---

## Future Directions

### Phase 2 Enhancements

- `/propose-changes` skill for AI-generated code diffs
- `/create-pr` skill for automated PR creation with ADR context
- Approval workflow: Human → AI proposes → Human reviews → CI/CD validates

### Phase 3 Enhancements

- Multi-agent deliberation for high-stakes decisions
- Competing proposals with synthesis
- Architectural Decision Log (ADL) generation

### Integration Ideas

- **IDE integration** — One-click skill invocation from editor
- **CI/CD hooks** — Auto-trigger /code-review on PR creation
- **Dashboard** — Visualize domain knowledge growth and "unknown" list shrinkage

---

## License

MIT

---

## Contributing

See [README.md](README.md) for contribution guidelines.

When extending decouple-legacy:
- Keep skills and agents generic
- Document customization points
- Add examples for new workflows
- Update plugin.json when adding skills/commands
- Run `python3 validate_plugins.py` before committing
