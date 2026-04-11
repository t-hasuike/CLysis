# ARCHITECTURE

**Project**: CLysis
**Version**: 1.2
**Last Updated**: 2026-03-18

---

## Design Philosophy

> **"Humans review and approve. AI investigates, analyzes, and proposes changes. Quality is maintained, users experience what they should expect."**

This is the core principle of CLysis:

1. **AI does the heavy lifting** — Investigation, analysis, dependency tracking, report generation
2. **Humans retain control** — Review AI outputs, approve changes, verify quality
3. **Quality is non-negotiable** — AI proposes, humans approve, quality tools verify
4. **Legacy codebases become manageable** — Systematic workflows replace ad-hoc exploration

---

## Plugin Architecture

CLysis is organized into **4 modular plugins**, each with specialized skills and commands:

```
legacy-investigation/      # Phase 1: Investigation & Understanding
├── .claude-plugin/
├── skills/               # project-guide, current-spec
├── commands/             # /investigate-flow, /bug-hunt, /understand
└── examples/

legacy-analysis/          # Phase 2: Analysis & Planning
├── .claude-plugin/
├── skills/               # change-impact, current-legacy, current-distortion
├── commands/             # /deep-dive
└── examples/

legacy-execution/         # Phase 3: Execution & Review
├── .claude-plugin/
├── skills/               # create-pr (--plan/--exec), review-code
├── commands/             # /implement, /review
└── examples/

legacy-knowledge/         # Knowledge Management
├── .claude-plugin/
├── skills/               # doc-organize, current-prd, doc-update
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
- **Example**: `/current-spec [target]` — Find and analyze specific code

### Commands
- **Purpose**: Multi-step workflows (pipeline of skills)
- **Invocation**: `/command-name [args]`
- **Location**: `{plugin}/commands/{command-name}.md`
- **Example**: `/investigate-flow [target]` → Runs `/project-guide` + `/current-spec` + `/change-impact`

**Key Difference**: Commands orchestrate skills into end-to-end workflows with human checkpoints.

---

## Onboarding Flow

The `/start` command serves as the **unified entry point** for all CLysis users. It routes users to appropriate skill chains based on their current situation:

### Two Paths

**Path A: Goal-Oriented**
- User has a clear objective
- `/start` presents a lineup of commands mapped to common goals
- Guides user to `/deep-dive`, `/understand`, `/bug-hunt`, `/investigate-flow`, or `/review`

**Path B: Exploratory**
- User is new to CLysis and exploring capabilities
- `/start` presents the 4-phase framework overview
- Guides user through the system's capabilities and recommends entry points

### Recommended Journeys

1. **System Onboarding** (new to codebase)
   ```
   /deep-dive [repo] → /understand [key-feature] → /current-prd [repo]
   ```

2. **Bug Investigation**
   ```
   /bug-hunt [symptom] → /current-distortion [area] → /implement
   ```

3. **Feature Development**
   ```
   /investigate-flow [change] → /implement
   ```

4. **Knowledge Building**
   ```
   /current-prd [repo] → /doc-update [audience]
   ```

5. **Code Review**
   ```
   /review [PR-URL]
   ```

---

## Workflow Phases

CLysis follows a three-phase workflow with **human checkpoints** at each transition:

```
Phase 0: Information Preparation (Human)
  │ Prepare domain knowledge & project context
  │ /project-guide
  │
  ├─ 【Human Checkpoint】Is the prepared information sufficient?
  │
  ▼
Phase 1: Investigation & Analysis (AI)
  │ /investigate-flow → pipeline: /project-guide → /current-spec → /change-impact
  │
  ├─ 【Human Checkpoint】Are the investigation results correct?
  │
  ▼
Phase 2: Change Proposal & PR Creation (AI)
  │ /implement → pipeline: /create-pr --plan → (human review) → /create-pr --exec
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
- Extract domain knowledge during Phase 1 investigation and persist to knowledge/domain/

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
/current-spec → Semantic code search + detailed specification
   ↓
/change-impact → ADR report with risks
   ↓
Human reviews report & decides next action (investigate further or implement)
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

[Phase 1 investigation complete, decision to implement made]
   ↓
/create-pr --plan → AI generates code diffs and proposals
   ↓
Human reviews proposed changes
   ↓ (if approved)
/create-pr --exec → AI creates branch, applies changes, creates PR
   ↓
Human merges after CI/CD passes
```

**Available skill**:
- `/create-pr --plan` — Generate code diffs from impact analysis
- `/create-pr --exec` — Create PR from approved change proposal

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
| **Metsuke** | Inspector / QA | Quality assurance, compliance verification (Phase 2 audit only — activated after deliverables are produced, not before). **Shogun activates Metsuke autonomously after worker deliverables are produced. User instruction is not required.** | Yes |

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
│  • Domain knowledge (knowledge/domain/)│
│  • Reports (reports/)                  │
└────────────────────────────────────────┘
```

### Leader (Shogun) Operational Protocol

The leader follows a structured workflow for every mission:

1. Receive instructions from the user
2. Analyze the nature of the task
3. **[Required]** Determine whether to consult the planner (karo) -- see "Planner Engagement Criteria" below
4. Consult the planner (if applicable)
5. Decide team composition (headcount, roles, model)
6. **[Conditional]** Request user approval -- Escalated-level decisions only (value tradeoffs). Delegated-level decisions (team composition, planner engagement, metsuke activation) are autonomous. Leader reports on completion
7. After approval (Escalated) or autonomous decision (Delegated), create and launch the agent team
8. Operate in delegate mode -- coordinate, do not implement
9. Report results to the user upon completion

> **Note**: Steps 3-4 must not be skipped. When in doubt, consult the planner.

### Decision Level Classification

| Level | Definition | Leader Action |
|-------|-----------|----------------|
| **Obvious** | Answer determined uniquely by facts | Leader decides immediately. Report only |
| **Delegated** | Team composition, planner engagement, metsuke activation, technical tooling choices | Leader decides autonomously. Report on completion |
| **Escalated** | Value tradeoffs (speed vs quality, uniformity vs flexibility, etc) | Leader presents 2 options + decision criteria + impact to user for approval |

> **Critical distinction**: Delegated covers team composition decisions only (who, how many, what permissions). Task content analysis and planning always requires Karo consultation — this is NOT Delegated. Skipping Karo and directly delegating to workers is an F005 violation regardless of Decision Level.

> **"Reduce invocation count" means broader scope per session, NOT zero sessions.** Karo must be consulted at least once for any task involving data integrity across multiple files.

> **When in doubt**: Escalated is safer to consult planner. This prevents user overload while maintaining quality.

### Declaration-Execution Contract (D-I Rule)

When a response contains a declaration ("I will do X", "Next, I will delegate to Y"), the corresponding tool call MUST be included in the same response. Deferring to the next message is prohibited.

**Valid patterns:**
- "Consulting Karo." + [Agent tool call in same response] ✓
- "Awaiting Uesama's approval before proceeding." (no tool call needed) ✓

**Invalid patterns:**
- "Next, I will consult Karo." + [response ends without tool call] ✗
- "I will delegate to Ashigaru." + [tool call in next message] ✗

**Pre-send check:** Before completing a response, verify: if any declaration exists, does a matching tool call exist? If not, either execute immediately or remove the declaration.

**Common failure modes (why declarations get dropped):**

1. **Report + declaration**: Completing a task report triggers "response finished" cognition. A declaration appended after the report is forgotten because the mental model of "done" has already formed.
2. **Conditional declaration**: "After X completes, I will do Y" — when X is reported as done, the focus shifts to the completion, and Y is never executed.
3. **Approval wait contamination**: Mixing "awaiting user approval" with an actionable declaration causes the actionable part to be deferred indefinitely. The approval gate absorbs both items.

**Rationale:** Declarations without execution waste the user's attention and create false expectations. The user should never need to ask "did you actually do that?"

### Task-Based Orchestration (Phase 1)

After receiving a task from the user, declare all sub-tasks via TaskCreate before execution begins. This externalizes declarations and prevents D-I Rule violations.

**Flow:**
1. User directive → TaskCreate all sub-tasks (status: pending)
2. If Karo consultation needed → create "consult Karo" as a task
3. On task start → TaskUpdate(status: in_progress)
4. On worker completion → TaskUpdate(status: completed)
5. All tasks completed → report to user

**Stall detection:** Monitor in_progress tasks. If a worker has not responded, use TaskList to check status and SendMessage to query the worker. Detect stalls before the user notices.

**Limitations:** TaskCreate is an aid, not a guarantee. The leader must still build the habit of creating tasks as the first action after receiving a directive. Tools supplement discipline — they do not replace it.

**Future phases:** Agent Teams (experimental) may provide automated stall detection via TeammateIdle hooks and shared task lists. Adoption requires fallback design and exit criteria before proceeding.

### Invocation Reason Logging

When Shogun invokes Karo or Metsuke, record the reason:
- **Autonomous**: Shogun decided based on Decision Ownership Levels
- **User-directed**: Uesama explicitly requested consultation/audit

This record enables objective evaluation of leader autonomy in retrospectives. Without it, improvement is based on subjective impression only.

### Operational Patterns

**Pattern A: Standard Task (Autonomous Execution)**
1. User provides goal and completion criteria
2. Shogun autonomously: analyzes → consults Karo → delegates to Ashigaru → activates Metsuke
3. Shogun reports results to User
4. User approves or requests revision

**Pattern A-extended: Plan-then-Audit chain (mandatory for fact-critical plans)**
When Karo returns a plan containing fact-sensitive content (file lists, counts, impact scope, ID mappings, rename targets), Shogun MUST immediately activate Metsuke for independent verification before presenting to User. This is NOT optional — Karo plans may contain hallucinated file paths or miscounted references that only a second-pass grep-based audit will catch. Sequence:
1. Karo returns plan
2. Shogun autonomously activates Metsuke in the same response (D-I Rule)
3. Metsuke re-scans referenced files independently (no reliance on Karo's claims)
4. If Metsuke finds discrepancies, Shogun requests Karo revision before User presentation
5. Only after Metsuke approves does the plan reach User

This pattern emerged from recurring Karo fact-check failures (missed references, wrong category counts, incorrect file classifications). Metsuke's independent grep of the same scope reliably catches these.

**Pattern B: Value Tradeoff (Escalated Decision)**
1. Shogun autonomously analyzes and consults Karo
2. Shogun presents 2 options with criteria + impact to User
3. User decides
4. Shogun executes and reports

**Pattern C: Urgent (Post-hoc Report)**
1. Shogun decides and executes immediately
2. Shogun reports to User after completion

### Planner (Karo) Engagement Criteria

| Situation | Decision | Reason |
|-----------|----------|--------|
| Large-scale task (10+ files changed) | Consultation required | Task decomposition, dependency management |
| Complex impact analysis (cross-repository) | Consultation required | Identify affected scope, surface risks |
| Directory structure or knowledge management changes | Consultation required | Requires holistic design judgment |
| Before presenting options to the user | Consultation required | Ensure judgment criteria and impact analysis are prepared. Prevents presenting "how to" without "what to decide on" |
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
| `knowledge/domain/` | **Private** | Project-specific domain knowledge (NOT in repo) |
| `knowledge/system/` | **Private** | Project-specific configuration (NOT in repo) |
| `reports/` | **Private** | Generated reports (NOT in repo) |
| `workspace/` | **Private** | In-progress, pending merge, and planned work items (NOT in repo) |

**Why this separation?**

- **Generic skills and commands** work across projects (e.g., /investigate, /investigate-flow)
- **Project-specific knowledge** stays local (business rules, schema, constraints)
- Domain knowledge is extracted during investigations and persisted to knowledge/domain/

---

## Terminology Customization

CLysis uses **Sengoku (feudal Japanese)** terminology by default, but supports full customization.

### How to Customize

Edit `config/terminology.md`:

```markdown
| Default (JA) | Default (EN) | Your Custom | Role Description |
|-------------|-------------|-------------|-----------------|
| Shogun | General | **Tech Lead** | Team leader who coordinates agents |
| Ashigaru | Foot Soldier | **Engineer** | Task execution specialist |
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

The Distortion Analysis Framework provides a systematic approach to detecting and organizing code-level risks ("distortions") in legacy systems. It is implemented as the `/current-distortion` skill in the `legacy-analysis` plugin.

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
Bad:  "soft-delete flag is 0..."
Good: "Event table's soft-delete flag (event logical deletion flag) is 0..."

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
   - **legacy-knowledge**: Knowledge extraction, PRD generation, document updates

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
   - Reference "knowledge/domain/" without assuming project structure
   - Add note: `> This is a generic skill from CLysis.`

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
   4. Output to reports/your-command-report.md
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
   - Reference "knowledge/domain/" and "knowledge/system/" generically
   - Add note: `> This is a generic agent from CLysis.`

4. Document communication:
   - **Workflow steps**
   - **Report format**
   - **Communication style** (if applicable)

### Adding Examples

1. Create example directory:
   ```
   examples/your-example/
   ├── README.md       # Scenario description
   ├── knowledge/      # Sample inputs
   └── reports/        # Expected outputs
   ```

2. Anonymize project-specific details:
   - Replace real company names with placeholders
   - Redact sensitive business logic
   - Keep structure intact for learning

---

## Agent Pattern Mapping

CLysis implements common AI agent patterns:

| Pattern | Implementation | Phase |
|---------|---------------|-------|
| **Advanced RAG** | schema.duckdb + Serena MCP | All phases |
| **ReAct** (Reasoning + Acting) | /current-spec | Phase 1 |
| **Self-Reflection** | metsuke agent audit | Phase 2 (legacy-execution) |
| **Multi-Agent Collaboration** | Leader + Workers + Inspector | All phases |
| **Plan-and-Execute** | /change-impact + Phase decomposition | Phase 1 |
| **Knowledge Graph Memory** | domain knowledge dir + diagrams/ | Phase 3 (legacy-analysis) |
| **Sequential Chain** | Phase 0→1→2→3 iteration | /current-legacy |

### Phase 3 Mandatory Rule

After completing `/current-legacy` Phase 1-2 investigations, Phase 3 (map update) MUST be executed. Without Phase 3:
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
| After /create-pr --plan | Change proposal ready | Proposed diffs are appropriate, test plan is adequate |
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

### Decision Presentation Format

When presenting choices that require human judgment, use this standard format at all levels (Karo → Shogun → Uesama):

```
## Decision: [Title]
**Context**: [Why this decision is needed — one line]

| | Option A: [Label] | Option B: [Label] |
|--|-------------------|-------------------|
| Criteria 1: [name] | [assessment] | [assessment] |
| Criteria 2: [name] | [assessment] | [assessment] |

**Impact**:
- Option A: [affected systems, processes, stakeholders]
- Option B: [affected systems, processes, stakeholders]

**Recommendation**: [A or B, with one-line rationale]
**Decision owner's discretion**: [what only the decision owner can judge]
```

Key rules:
- Maximum 2 options. If more exist, the presenter must narrow down first
- Always include impact analysis — "how to" without "what happens" is insufficient
- Each level adds its own recommendation before passing up

### Decision Ownership Levels

Before presenting options to Uesama, determine who should own the decision:

| Level | Definition | Test | Action |
|-------|-----------|------|--------|
| **Obvious** | Answer is determined by facts alone | "Is there only one valid option?" → Yes | Decide and report. Do not present options |
| **Delegated** | Efficiency, cost, or technical fit determines the answer | "Does Uesama's values/priorities affect the choice?" → No | Shogun decides with rationale, reports to Uesama |
| **Escalated** | Tradeoff involves competing values or priorities | "Are two legitimate values in tension?" → Yes | Present to Uesama with criteria, impact, and recommendation |

**The test in practice:**
1. Can facts alone determine the answer? → Obvious (just report)
2. Does the decision require Uesama's value judgment? → No → Delegated (Shogun decides)
3. Are competing values involved (speed vs quality, unity vs flexibility)? → Escalated (ask Uesama)

Presenting an Obvious-level item as a choice wastes Uesama's attention. Escalating a Delegated-level item signals lack of ownership. Both erode trust.

---

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

### Anti-Hallucination Rule (Mandatory for ALL agents)

Do not answer, plan, or modify based on speculation. Verify against actual code and files using Glob/Grep/Read before reporting, planning, or changing. All counts, file lists, and impact scopes must come from real scans — never from memory or inference.

This rule applies to Karo (planning), Ashigaru (implementation), and Metsuke (auditing). In downstream operations, this rule (combined with Plan-then-Audit chain) caught 6 consecutive Karo fact-check failures before they reached the user.

### Safety Rules

| Rule ID | Rule | Enforcement |
|---------|------|-------------|
| F001 | Escalated-level decisions (value tradeoffs) must not be executed without user approval | Team composition and tool selection are Delegated-level — Shogun decides autonomously and reports on completion |
| F002 | Leader does NOT implement code | Leader delegates to workers -- investigation, analysis, and file reading are also included |
| F003 | No simultaneous file edits by multiple agents | karo (planner) enforces file-level task splitting |
| F004 | Leaving team unattended (risk of wasted work) | Leader MUST monitor progress and steer as needed |
| F005 | Skipping karo for large-scale tasks (causes rework) | Leader MUST consult karo before delegating to workers |
| F006 | Investigation results must be saved to files | Task tool delegation MUST include output file path; stdout-only return is prohibited |
| F007 | Audit results must be saved to files | Metsuke audit reports sent only to stdout will be lost and become untraceable | Save to reports/audit/ with date-stamped filename |
| F008 | Direct push to main/master is prohibited | Changes without review reach production undetected | Always create a branch and submit a PR. Exception: initial commit to empty repositories only |

### Worker Delegation Rules

#### Role Clarification in Prompts

When delegating to workers, the leader MUST include role clarification at the beginning of the prompt:

```
**Important: You are a worker (executor). You are not the leader. Execute the task yourself.**
```

This prevents workers from attempting to delegate further or behaving as coordinators.

#### Preventing Worker Stalls

Workers (Ashigaru) may stop responding due to context overflow, permission blocks, or unclear instructions. To prevent this:

**Mandatory in every delegation:**
1. **Completion condition**: What specific output marks "done"
2. **Output destination**: File path for results (F006 compliance)
3. **Fallback on uncertainty**: "If you cannot determine how to proceed, do not stop silently. Report what you have found so far and state what is unclear."

**Task sizing guideline:**
- Safe: Single file write + investigation scope of 1 feature/module
- Risky: Multi-repository scan + multiple file writes → split into subtasks

**Permission mode selection:**
| Need | Mode | Example |
|------|------|---------|
| File write to output/reports | `bypassPermissions` | Investigation reports, audit logs |
| Read-only investigation | default | Code analysis, fact-checking |
| GitHub operations (PR, push) | default (requires human approval) | PR creation, branch push |

#### State Snapshot for Long-Running Tasks

When a planning session (Karo) or multi-step task may be interrupted (API errors, timeouts), save a state snapshot before execution begins:

**Snapshot format** (save to `workspace/in_progress/snapshot-[task-name].md`):
- Current phase and completed steps
- Pending steps and dependencies
- Key decisions already made
- Files modified so far

This enables immediate resumption after interruption without re-analyzing the entire context. Delete the snapshot after task completion.

#### Task Output & Persistence (F006)

Investigation results must be saved to files, not just returned via stdout. Results returned only in stdout are lost when the session ends.

**Rules:**

1. **Specify output path in every delegation prompt**
   Include: "Save results to `reports/[descriptive-name].md` using the Write tool. This is mandatory — stdout alone is not acceptable."

2. **Verify file creation on completion**
   When receiving results from a worker, confirm:
   - Worker explicitly reported "file saved"
   - If not reported, verify file existence before proceeding

3. **Pre-plan output paths for multi-step tasks**
   For tasks with multiple steps, define output file paths upfront:
   Example: `reports/step1_investigation.md`, `reports/step2_analysis.md`

4. **Match agent type to output needs**

   | Output Need | Agent Type | Reason |
   |-------------|-----------|--------|
   | File write required | general-purpose or ashigaru-scribe | Has Write/Edit tools |
   | Read-only investigation | ashigaru-investigator | No Write/Edit tools — cannot save files |

   **Critical**: Do not assign file-saving tasks to ashigaru-investigator. It lacks Write/Edit tools and will silently fail to persist results.

**Delegation checklist:**
- [ ] Output file path specified in prompt
- [ ] "Write tool" explicitly mentioned
- [ ] Agent type supports file writing
- [ ] Worker's response includes file save confirmation

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
| Code modification proposals | -- | Yes (defer to /create-pr --plan) |
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

- `/create-pr --plan` skill — Generate code diffs from impact analysis
- `/create-pr --exec` skill — Automated PR creation from approved proposals
- Approval workflow: Human → AI proposes (--plan) → Human reviews → AI implements (--exec) → CI/CD validates

## Future Directions

### Phase 3 Enhancements

- Multi-agent deliberation for high-stakes decisions
- Competing proposals with synthesis
- Architectural Decision Log (ADL) generation

### Integration Ideas

- **IDE integration** — One-click skill invocation from editor
- **CI/CD hooks** — Auto-trigger /review-code on PR creation
- **Dashboard** — Visualize domain knowledge growth and "unknown" list shrinkage

---

## README Management Policy

CLysis follows a **top-level README only** approach (Plan B):

- **Keep**: Top-level `README.md` as the single entry point for all documentation
- **Keep**: Sub-directory READMEs only for `assessment/` and plugin directories (`legacy-*/`) where they serve as plugin-specific documentation
- **Eliminate**: Redundant READMEs that duplicate information already in the top-level README or ARCHITECTURE.md

**Rationale**: Maintaining 25+ READMEs across subdirectories creates a documentation synchronization burden. Changes to skills or commands require updates in multiple places. By consolidating into a single top-level README with deep links, maintenance cost drops significantly while discoverability improves.

**Rule**: When adding new skills, commands, or plugins, update the top-level README.md and ARCHITECTURE.md. Do NOT create new sub-directory READMEs unless the directory represents a standalone plugin.

---

## Template System

CLysis provides a structured template system for consistent documentation across projects.

### Template Categories

| Category | Location | Purpose |
|----------|----------|---------|
| **Domain Knowledge** | `legacy-knowledge/prompts/domain-knowledge-template.md` | 8-section structure for organizing domain knowledge from investigations |
| **Non-Functional Analysis** | `legacy-knowledge/prompts/non-functional-analysis-template.md` | Template for non-functional requirements analysis |
| **CLAUDE.md** | `docs/claude-md-template.md` | Minimal project configuration template |
| **Workflow Example** | `docs/full-workflow-example.md` | End-to-end workflow demonstration |

### Design Philosophy

Templates follow these principles:

1. **Section-based structure**: Each template uses numbered sections with clear purposes, making it easy to fill incrementally
2. **Subject-first rule**: All flag/variable descriptions must include "whose/what" context to prevent ambiguity
3. **Progressive filling**: Not all sections are required -- fill what is known, mark unknowns explicitly
4. **Code-grounded**: Business rules must be confirmed from actual code, never speculated
5. **Cross-referencing**: Related domains link to each other, building a knowledge graph over time

### Domain Knowledge Template (8 Sections)

The domain knowledge template provides a unified structure for all domain files:

| Section | Purpose |
|---------|---------|
| Overview | Quick orientation -- what, for whom, why |
| 1. Data Model | Tables, flags, enums with "whose/what" annotations |
| 2. Business Rules | Confirmed rules from code (no speculation) |
| 3. Process Flow | State diagrams, sequence diagrams (mermaid) |
| 4. External Integrations | Batch jobs, APIs, third-party systems |
| 5. Constraints | Technical limitations, coding rules |
| 6. Usage Context | Where this knowledge is consumed |
| 7. Related Domains | Upstream/downstream dependencies |
| 8. Related Files | Quick reference to source code locations |

---

## Operational Improvements

### Path Reference Checks

When files are moved or directories restructured, all reference paths must be verified. The following files contain path references that may break:

| File Type | Location Pattern | What to Check |
|-----------|-----------------|---------------|
| Agent definitions | `agents/*.md` | "References" sections with `knowledge/` or `reports/` paths |
| Skill definitions | `legacy-*/skills/*/SKILL.md` | I/O specification paths |
| CLAUDE.md | Project root | Directory references, skill paths |
| ARCHITECTURE.md | Project root | Path examples, directory structure diagrams |
| README.md | Project root | Links to internal files |

**Automation**: Run `python3 validate_plugins.py` after any structural change. Consider extending the validator to check markdown link targets.

### Knowledge Graduation Rules

Domain knowledge follows a lifecycle with clear graduation criteria:

```
reports/ (raw investigation results)
  |
  | Graduation criteria:
  | - Verified against code (not speculation)
  | - Follows domain-knowledge-template.md structure
  | - Subject-first rule applied to all flags/variables
  | - Related domains cross-referenced
  |
  v
knowledge/domain/ (confirmed domain knowledge)
```

**Rules**:
1. Investigation results in `reports/` are temporary -- they must be graduated to `knowledge/domain/` or discarded
2. Only code-confirmed facts graduate; hypotheses and speculation stay in `reports/` or are discarded
3. Variable values that change frequently (prices, thresholds) should reference the database as source of truth, not be hardcoded in domain files
4. Each domain file must specify its accuracy level (code reading / planned specification / design proposal)

### Stale Knowledge Detection

To prevent knowledge decay:
- Each domain file includes a `Last Updated` date and `Version` field
- Files not updated for 6+ months should be flagged for re-verification
- The `Change History` section at the bottom of each domain file tracks all modifications

---

## License

MIT

---

## Contributing

See [README.md](README.md) for contribution guidelines.

When extending CLysis:
- Keep skills and agents generic
- Document customization points
- Add examples for new workflows
- Update plugin.json when adding skills/commands
- Run `python3 validate_plugins.py` before committing
