# ARCHITECTURE

**Project**: decouple-legacy
**Version**: 1.2
**Last Updated**: 2026-03-18

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
├── skills/               # impact-analysis, legacy-analyze, distortion-analysis
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

### Roles (Sengoku Style by Default)

| Role (JA) | Role (EN) | Responsibility | Modifiable via config/terminology.md |
|-----------|-----------|----------------|-------------------------------------|
| **Uesama** | Lord / User | The human who gives instructions | Yes |
| **Shogun** | General / Leader | Team coordination, task delegation | Yes |
| **Karo** | Chief Retainer / Planner | Task decomposition, dependency management | Yes |
| **Ashigaru** | Foot Soldier / Worker | Task execution (backend, frontend, docs, investigation, devops) | Yes |
| **Metsuke** | Inspector / QA | Quality assurance, compliance verification | Yes |

### Hierarchy & Communication

```
Uesama (User)
  │
  ▼ Gives instructions
Shogun (Leader)
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
│  Karo (Planner) — Large task breakdown │
│  Ashigaru (Workers) — Execution            │
│  Metsuke (Inspector) — Quality audit   │
└────────────────────────────────────────┘
  │
  ▼ Shared resources
┌────────────────────────────────────────┐
│  • Shared task list (TaskCreate/Update)│
│  • Natural language messaging          │
│  • Domain knowledge (input/domain/)    │
│  • Reports (output/ or reports/)       │
└────────────────────────────────────────┘
```

### Leader (Shogun) Operational Protocol

The leader follows a structured workflow for every mission:

1. Receive instructions from the user
2. Analyze the nature of the task
3. **[Required]** Determine whether to consult the planner (karo) -- see "Planner Engagement Criteria" below
4. Consult the planner (if applicable)
5. Decide team composition (headcount, roles, model)
6. **[Required]** Request user approval for team formation
7. After approval, create and launch the agent team
8. Operate in delegate mode -- coordinate, do not implement
9. Report results to the user upon completion

> **Note**: Steps 3-4 must not be skipped. When in doubt, consult the planner.

### Planner (Karo) Engagement Criteria

| Situation | Decision | Reason |
|-----------|----------|--------|
| Large-scale task (10+ files changed) | Consultation required | Task decomposition, dependency management |
| Complex impact analysis (cross-repository) | Consultation required | Identify affected scope, surface risks |
| Directory structure or knowledge management changes | Consultation required | Requires holistic design judgment |
| Before presenting proposals to the user | Consultation required | Improve proposal quality and accuracy |
| Error resolution (unknown cause, multi-file) | Consultation recommended | Root cause identification |
| Small-scale investigation (single feature) | Not needed | Task tool is sufficient |
| Minor documentation edits | Not needed | Delegate directly to workers |

### Team Composition Guidelines

| Scale | Team Structure | When to Use |
|-------|---------------|-------------|
| **Small investigation** | Task tool (sub-agent) | Single-shot investigation or code analysis |
| **Medium task (compound)** | Karo (planner) then workers | Multi-step tasks (e.g., investigation + documentation update) |
| **Medium task (parallel)** | 2 team members | Parallel work across 2 domains |
| **Large task** | 3-4 team members | Parallel work across multiple domains with review |
| **Investigation + deliberation** | 3-5 team members | Competing hypothesis validation, code review |

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
| Shogun | General | **Tech Lead** | Team leader who coordinates agents |
| 足軽 (Ashigaru) | Foot Soldier | **Engineer** | Task execution specialist |
```

All skills and agents reference this file for term adaptation.

### Communication Styles

| Style | Example |
|-------|---------|
| **Sengoku Japanese** (default) | "My lord, I have received the mission." |
| **Business Japanese** | "Understood. Starting the task now." |
| **English Casual** | "Got it! Starting the task now." |
| **English Formal** | "Understood. Initiating the assigned task." |

To change style, add to your project's CLAUDE.md:

```markdown
## Communication Style
Use business Japanese for all reports.
```

---

## Distortion Analysis Framework

The Distortion Analysis Framework provides a systematic approach to detecting and organizing code-level risks ("distortions") in legacy systems. It is implemented as the `/distortion-analysis` skill in the `legacy-analysis` plugin.

### Part A/B/C Framework

Every distortion analysis produces a structured report with three complementary perspectives:

| Part | Perspective | Purpose | Key Output |
|------|-----------|---------|------------|
| **Part A** | Business Process-driven | Map risks to business processes | Process-risk matrix with severity distribution |
| **Part B** | Root Cause-driven | Classify risks by problem pattern | Remediation priority table with ROI |
| **Part C** | Mermaid Overview | Visualize risk relationships | 3 diagrams: flow, causality, remediation impact |

**Why three parts?** The same set of risks is viewed from different angles. Part A answers "which business processes are affected?", Part B answers "what root causes should we fix first?", and Part C answers "how do the risks relate to each other?"

Risk counts MUST match across all three parts -- they represent the same risk set, just organized differently.

### Distortion Patterns (A/B/C)

Distortion patterns classify HOW a code defect manifests at runtime:

| ID | Pattern | Description | Typical Example |
|----|---------|-------------|-----------------|
| **A** | Invalid value passes through | Insufficient validation allows values that should be rejected to flow downstream | Expired items included in checkout processing |
| **B** | Stops midway | Some processing succeeds but downstream processing fails or becomes inconsistent | Order confirms but fulfillment routing errors |
| **C** | No check exists | Required validation logic does not exist at all | No expiration check during payment |

### Problem Patterns (P1-P6)

Problem patterns classify the ROOT CAUSE of a distortion:

| ID | Pattern | Description | Detection Focus |
|----|---------|-------------|-----------------|
| **P1** | Implicit shared flag dependency | Multiple processes reference the same flag with different assumptions | Cross-search flag references; record "whose/what" flag |
| **P2** | Constant/Enum mismatch | Code constant definitions differ from DB stored values or cross-repository definitions | Compare Enum definitions, `const` declarations, DB data |
| **P3** | Type comparison traps | Language-specific loose comparison pitfalls | Loose equality, missing strict parameters, switch type matching |
| **P4** | Soft-delete/JOIN condition gaps | Missing logical deletion or JOIN conditions | Search SQL, ORM scopes, raw queries |
| **P5** | Implicit value conversion | Unintended type/value conversions affecting results | Track casts, conversion functions, date parsing |
| **P6** | Insufficient branching | Unhandled cases, missing else/default branches | Branch coverage, missing error handling |

### Subject-First Rule

When documenting risks involving flags, variables, or columns, always explicitly state **"whose/what"** as the subject. This prevents ambiguity and ensures readers understand the context without cross-referencing.

```
Bad:  "delflag is 0..."
Good: "Event table's delflag (event logical deletion flag) is 0..."

Bad:  "publication_end_date is not checked"
Good: "Event's publication end date (event.publication_end_date) is not checked in PaymentProcessor's payment processing"
```

**Where to apply the Subject-First Rule:**
- Distortion analysis reports (Part A/B/C)
- Code review comments involving domain-specific flags or variables
- Investigation reports referencing shared state across services
- Any documentation describing cross-repository data dependencies

### Cross-Cutting Risk View

When analyzing multiple repositories, risks that span boundaries require a two-layer management approach:

```
L1: Component-Level View (per repository)
    Individual distortion reports for each repository
    ↓ synthesize after 2+ repos analyzed
L2: Cross-Cutting View (across repositories)
    Shared flags with different assumptions across repos
    Data flow integrity across service boundaries
    Inconsistent validation between layers
```

| Layer | Scope | When to Create | Example |
|-------|-------|---------------|---------|
| **L1** | Single repository/component | Always (default output) | Checkout flow risks in EC repo |
| **L2** | Multiple repositories | After 2+ L1 analyses for related areas | Flag referenced differently in EC vs Backend |

**L2 risks are often the most dangerous** because no single team owns them and they cross deployment boundaries.

### 2-Phase Execution Model

```
Phase 1: Risk Collection
    5 workers in parallel
    → Worker A: Integrate existing investigation results
    → Worker B-E: 4 distortion investigation perspectives
    → Leader: Deduplicate & integrate (no file output)

Phase 2: Part A/B/C Creation
    3 workers in parallel
    → Worker F: Part A (Business Process-driven)
    → Worker G: Part B (Root Cause-driven)
    → Worker H: Part C (Mermaid Overview)
    → Leader: Integrate into single report file
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
   - **Workflow steps**
   - **Report format**
   - **Communication style** (if applicable)

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
| **Knowledge Graph Memory** | domain knowledge dir + diagrams/ | Phase 3 (legacy-analyze) |
| **Sequential Chain** | Phase 0→1→2→3 iteration | /legacy-analyze |

### Phase 3 Mandatory Rule

After completing `/legacy-analyze` Phase 1-2 investigations, Phase 3 (map update) MUST be executed. Without Phase 3:
- Knowledge remains trapped in the session and is lost
- Subsequent investigations re-cover the same ground
- The "unknown" list does not shrink

Phase 3 ensures that investigation results are persisted as updated diagrams and domain knowledge.

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

## Visualization Standards

State and structure visualization uses **mermaid format** as the default. The leader (or assigned agent) should select the appropriate diagram type based on the situation.

| Diagram Type | Use Case | Example |
|-------------|----------|---------|
| flowchart | Bird's-eye view, dependency maps, cascading impact maps | Module dependency relationships |
| sequenceDiagram | Processing flows, API call chains, batch processes | Order-to-delivery flow |
| stateDiagram | Status transitions | Order status lifecycle |
| erDiagram | Table relationships, data models | Entity-relationship diagrams |

Investigation reports should include at least one visualization diagram to make findings accessible at a glance.

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
| F002 | Leader does NOT implement code | Leader delegates to workers -- investigation, analysis, and file reading are also included |
| F003 | No simultaneous file edits by multiple agents | karo (planner) enforces file-level task splitting |
| F004 | Leaving team unattended (risk of wasted work) | Leader MUST monitor progress and steer as needed |
| F005 | Skipping karo for large-scale tasks (causes rework) | Leader MUST consult karo before delegating to workers |
| F006 | Investigation results must be saved to files | Task tool delegation MUST include output file path; stdout-only return is prohibited |

### Worker Delegation Rules

#### Role Clarification in Prompts

When delegating to workers, the leader MUST include role clarification at the beginning of the prompt:

```
**Important: You are a worker (executor). You are not the leader. Execute the task yourself.**
```

This prevents workers from attempting to delegate further or behaving as coordinators.

#### Agent Type Selection

| Agent Type | Capabilities | Use When |
|------------|-------------|----------|
| ashigaru-investigator | Read-only (cannot write files) | Pure investigation, code analysis |
| ashigaru-scribe | Can create documents (but may trigger approval waits) | Documentation tasks |
| general-purpose | Can write files without approval waits | Investigation tasks that require file output (F006 compliance) |

**Key rule**: When a task requires both investigation AND file output, use `general-purpose` instead of `ashigaru-investigator`.

### Investigation Phase Constraints

During investigation/analysis phases (before implementation decisions are made), the following constraints apply:

| Action | Allowed | Prohibited |
|--------|---------|-----------|
| Code reading and analysis | Yes | -- |
| Report writing | Yes | -- |
| Domain knowledge updates | Yes | -- |
| Diagram updates (mermaid) | Yes | -- |
| Code modification proposals | -- | Yes (defer to /propose-changes) |
| Direct code edits | -- | Yes (always prohibited during investigation) |
| Configuration changes | -- | Yes (defer to implementation phase) |

This separation ensures that investigation produces clean, unbiased analysis without premature solution commitment.

### Configuration Change Reference Check

When directory structure or knowledge management configuration changes, the leader MUST verify that all reference paths in the following files remain valid:

- Agent definitions (`agents/*.md`) -- reference paths in "References" sections
- Skill definitions (`legacy-*/skills/*/SKILL.md`) -- I/O specification paths
- CLAUDE.md -- directory references
- ARCHITECTURE.md -- path examples

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

## Implemented Features

### Phase 2: Automated Change Proposals (Implemented)

- `/propose-changes` skill — Generate code diffs with context
- `/create-pr` skill — Automated PR creation with ADR context
- Approval workflow: Human → AI proposes → Human reviews → CI/CD validates

## Future Directions

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
