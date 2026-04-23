# CLysis

> AI-powered framework for understanding, analyzing, and modernizing legacy systems.

Systematic support for investigation, analysis, and modernization of legacy systems using AI agent teams.
13 domain-specific skills and 7 workflow commands across 5 plugins.

## Repository Structure

```
CLysis/
├── .claude-plugin/            # Marketplace manifest
├── agents/                    # Agent definitions (karo, metsuke, ashigaru-*)
├── assessment/                # Quality evaluation criteria & maturity model
├── config/                    # Terminology customization
├── docs/                      # Templates, workflow examples, migration guide
├── legacy-analysis/           # Plugin: change-impact, current-legacy, current-distortion
│   ├── .claude-plugin/
│   ├── commands/
│   ├── examples/
│   └── skills/
├── legacy-execution/          # Plugin: create-pr, review-code
│   ├── .claude-plugin/
│   ├── commands/
│   ├── examples/
│   └── skills/
├── legacy-investigation/      # Plugin: project-guide, current-spec
│   ├── .claude-plugin/
│   ├── commands/
│   ├── examples/
│   └── skills/
├── legacy-knowledge/          # Plugin: doc-organize, current-prd, doc-update, templates
│   ├── .claude-plugin/
│   ├── examples/
│   ├── prompts/
│   └── skills/
├── legacy-workflow/           # Plugin: kpt, empirical-prompt-tuning
│   ├── .claude-plugin/
│   └── skills/
├── ARCHITECTURE.md
├── LICENSE
├── README.md
└── validate_plugins.py
```

## Plugins

| Plugin | Skills | Commands | Description |
|--------|--------|----------|-------------|
| [legacy-investigation](./legacy-investigation/) | 2 | 4 | Investigation & understanding (project-guide, current-spec) |
| [legacy-analysis](./legacy-analysis/) | 3 | 1 | Analysis & planning (change-impact, current-legacy, current-distortion) |
| [legacy-execution](./legacy-execution/) | 2 | 2 | Execution & review (create-pr, review-code) |
| [legacy-knowledge](./legacy-knowledge/) | 4 | 0 | Knowledge accumulation (doc-organize, current-prd, doc-update, templates) |
| [legacy-workflow](./legacy-workflow/) | 2 | 0 | Process improvement (kpt, empirical-prompt-tuning) |

## Prerequisites

- **Claude Code** — Required
- **Serena MCP** — Recommended. Enables semantic code search for `/current-spec`. Skills work without it but with reduced accuracy.
- **GitHub MCP** — Optional. Required for `/create-pr` and `/review-code`.

## Quick Start

### Choose your installation method

- **Marketplace** (recommended) — Using Claude Code with internet access
- **Local** — Running locally or in a restricted environment
- **Manual** — Just want to try individual skills

### Installation Methods

#### Marketplace Installation (Recommended)

Register the marketplace and install plugins:

```bash
# Register the marketplace
claude plugin marketplace add t-hasuike/CLysis

# Install individual plugins
claude plugin install legacy-investigation@CLysis
claude plugin install legacy-analysis@CLysis
claude plugin install legacy-execution@CLysis
claude plugin install legacy-knowledge@CLysis
```

Or install all plugins at once:

```bash
# Install all 4 plugins in one command
claude plugin install legacy-investigation@CLysis legacy-analysis@CLysis legacy-execution@CLysis legacy-knowledge@CLysis legacy-workflow@CLysis

# Verify installation
claude plugin list
```

#### Local Installation

If running locally or adding to an existing marketplace:

```bash
# Add this repository to the marketplace
claude plugin marketplace add CLysis /path/to/CLysis

# Then install plugins as above
claude plugin install legacy-investigation@CLysis legacy-analysis@CLysis legacy-execution@CLysis legacy-knowledge@CLysis legacy-workflow@CLysis

# Verify installation
claude plugin list
```

#### Manual Installation

Clone the repository and copy individual skills to your project:

```bash
# Clone the repository
git clone https://github.com/t-hasuike/CLysis.git
cd CLysis

# Copy skills from a specific plugin
cp -r legacy-investigation/skills/* /path/to/your/project/.claude/skills/

# Or copy commands
cp -r legacy-investigation/commands/* /path/to/your/project/.claude/commands/
```

### Available Plugins

| Plugin | Skills | Description |
|--------|--------|-------------|
| **legacy-investigation** | project-guide, current-spec | Code exploration, service specification, documentation reference |
| **legacy-analysis** | change-impact, current-legacy, current-distortion | Impact analysis, system overview, code quality patterns |
| **legacy-execution** | create-pr, review-code | Change proposals and PR creation (--plan/--exec), automated code review |
| **legacy-knowledge** | doc-organize, current-prd, doc-update, templates | Knowledge extraction, PRD generation, document updates |
| **legacy-workflow** | kpt, empirical-prompt-tuning | KPT retrospectives, skill quality optimization |

### Skill Chain Patterns

Common workflows for analyzing and modernizing legacy systems:

#### Impact Analysis Chain

Investigate the full impact of proposed changes:

```bash
/project-guide [your task]
  → /current-spec [target service or area]
  → /change-impact [change description]
```

**Use case**: Before implementing a change, understand its ripple effects across the codebase.

#### Bug Investigation Chain

Locate and understand the root cause of defects:

```bash
/project-guide [bug description]
  → /current-spec [suspected area]
  → /current-distortion [repository] [area]
```

**Use case**: Systematically identify code quality patterns and risk areas.

#### System Understanding Chain

Build comprehensive domain knowledge:

```bash
/project-guide [feature or module]
  → /current-spec [target service]
```

**Use case**: Document and archive understanding of critical legacy components.

### First Steps

1. Use the skills in your Claude Code session:

```bash
/project-guide my-legacy-feature
/current-spec AccountService
/change-impact [describe your planned change]
```

2. Use the execution skills to propose and review changes:

```bash
/create-pr --plan [change-impact-report]
/create-pr --exec [change-proposal]
/review-code [PR number]
```

## Plugin Dependencies and Recommended Setup

### Dependency Matrix

Some commands reference skills from other plugins. Ensure required plugins are installed:

| Command | Required Plugins | Purpose |
|---------|-----------------|---------|
| `/investigate-flow` | legacy-investigation + legacy-analysis | Full investigation pipeline with change impact analysis |
| `/bug-hunt` | legacy-investigation + legacy-analysis | Bug root cause analysis |
| `/deep-dive` | legacy-analysis (+ others for context) | System-wide analysis |
| `/implement` | legacy-execution + legacy-investigation | End-to-end change implementation |
| `/review` | legacy-execution + legacy-investigation | PR review with context |

### Recommended Setup

**For all users**: Install all 5 plugins to unlock full functionality and workflow chains:

```bash
claude plugin install legacy-investigation@CLysis legacy-analysis@CLysis legacy-execution@CLysis legacy-knowledge@CLysis legacy-workflow@CLysis
```

**By team role**:

| Team Role | Required Plugins | Install Command |
|-----------|-----------------|-----------------|
| **Investigators** (understand legacy code) | legacy-investigation + legacy-analysis | `legacy-investigation@CLysis legacy-analysis@CLysis` |
| **Implementers** (make changes) | legacy-execution + legacy-investigation | `legacy-execution@CLysis legacy-investigation@CLysis` |
| **Reviewers** (validate changes) | legacy-execution + legacy-analysis | `legacy-execution@CLysis legacy-analysis@CLysis` |
| **Knowledge Architects** (document systems) | legacy-knowledge + legacy-investigation | `legacy-knowledge@CLysis legacy-investigation@CLysis` |
| **Process Leads** (improve workflows) | legacy-workflow | `legacy-workflow@CLysis` |
| **Full Teams** | All 5 plugins | `legacy-investigation@CLysis legacy-analysis@CLysis legacy-execution@CLysis legacy-knowledge@CLysis legacy-workflow@CLysis` |

## Workflow Commands

| Command | Plugin | Description |
|---------|--------|-------------|
| `/start` | legacy-investigation | Interactive getting started guide. Entry point for all CLysis workflows |
| `/investigate-flow` | legacy-investigation | Impact investigation flow (4-skill chain) |
| `/bug-hunt` | legacy-investigation | Bug investigation flow |
| `/understand` | legacy-investigation | Code comprehension flow |
| `/deep-dive` | legacy-analysis | In-depth system-wide analysis |
| `/implement` | legacy-execution | Change proposal to PR creation (2-stage human approval) |
| `/review` | legacy-execution | PR review flow |

## Skills Overview

| Skill | Plugin | Description |
|-------|--------|-------------|
| `/project-guide` | legacy-investigation | Context-aware documentation reference guide |
| `/current-spec` | legacy-investigation | Code investigation and service specification documentation |
| `/change-impact` | legacy-analysis | Impact analysis with ADR-format reports |
| `/current-legacy` | legacy-analysis | Legacy codebase understanding workflow (Phase 0->1->2->3) |
| `/current-distortion` | legacy-analysis | Detect code distortion patterns and organize in Part A/B/C framework |
| `/create-pr` | legacy-execution | Generate code diffs (--plan) and create PR (--exec) from approved proposals |
| `/review-code` | legacy-execution | PR review with code quality and domain knowledge validation |
| `/doc-organize` | legacy-knowledge | Archive investigation outputs for knowledge reuse |
| `/current-prd` | legacy-knowledge | Reverse-engineer PRD from existing codebase (Phase 1-3 workflow) |
| `/doc-update` | legacy-knowledge | Update knowledge documents for target audience (developer, PM, onboarding) |
| `/kpt` | legacy-workflow | KPT (Keep/Problem/Try) retrospective with Five Whys for recurring problems |
| `/empirical-prompt-tuning` | legacy-workflow | Bias-free skill definition evaluation and iterative improvement |

## Initial Setup

After installing the plugins, set up your project structure:

### 1. Create directory structure

```bash
# Knowledge, reports, and workspace directories (not tracked by git)
mkdir -p knowledge/{domain,system,adr,archive}
mkdir -p workspace/{in_progress,pending_merge,planned}
mkdir -p reports
```

### 2. Configure .gitignore

```bash
cp CLysis/.gitignore.template .gitignore
```

Review and customize the `.gitignore` based on your project's needs.

### 3. Create CLAUDE.md

See `docs/claude-md-template.md` for a minimal template. Key sections:

- **Repositories**: Define your repository paths (referenced by agents)
- **Tech Stack**: Define your technology stack (referenced by agents)
- **Required Rules**: Project-specific coding rules
- **Domain Knowledge**: Map your `knowledge/domain/` files
### 4. Start accumulating knowledge

```
/project-guide [your first task]
/current-spec [target service or module]
(Domain knowledge is now integrated into the investigation/analysis workflow)
```

Each investigation builds your domain knowledge in `knowledge/domain/` and saves reports to `reports/`.

## Workflow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                      User (Developer)                         │
│              Defines task, reviews, approves                  │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼ Task assignment
┌─────────────────────────────────────────────────────────────┐
│                   Leader (Shogun / General)                  │
│  • Analyzes task complexity                                  │
│  • Requests user approval for team formation                 │
│  • Coordinates agent team in delegate mode                   │
│  • Does NOT implement code directly (F002 rule)              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ├─ Small task → Task tool (subagent)
                     │
                     └─ Large task → Create agent team
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ Worker A│◄──►│ Worker B│◄──►│ Worker C│
    │(backend)│    │(frontend)│   │(scribe)│
    └─────────┘    └─────────┘    └─────────┘
         │              │              │
         └──────────────┴──────────────┘
                       │
                       ▼ Results & artifacts
    ┌────────────────────────────────────────────────────┐
    │              Task System & Outputs                  │
    │  • Shared task list for coordination               │
    │  • Natural language messaging between agents       │
    │  • Reports generated to reports/                   │
    │  • Domain knowledge persisted to knowledge/domain/ │
    └────────────────────────────────────────────────────┘
```

## Investigation Flow

Commands provide pre-configured pipelines for common workflows:

```
/investigate-flow [target]
   → /project-guide + /current-spec + /change-impact
   → All-in-one investigation pipeline
```

## Distortion Analysis Flow

Detect code-level risks ("distortions") and organize them systematically:

```
/current-distortion [repository] [area]
   → Phase 1: 5 parallel workers detect risks (flag gaps, type traps, missing checks, etc.)
   → Phase 2: 3 parallel workers create Part A/B/C report
   → Output: distortion-report-[repo]-[area]-[date].md
```

**Part A/B/C Framework**:
- **Part A**: Business Process-driven -- maps risks to business processes
- **Part B**: Root Cause-driven -- classifies by problem patterns (P1-P6), produces remediation priority with ROI
- **Part C**: Mermaid Overview -- visualizes flow, causality, and remediation impact

**Key concepts**:
- **Distortion Patterns**: A (invalid value passes), B (stops midway), C (no check exists)
- **Problem Patterns**: P1-P6 (shared flags, enum mismatch, type traps, soft-delete gaps, implicit conversion, insufficient branching)
- **Subject-First Rule**: Always state "whose/what" when documenting flags and variables
- **Cross-Cutting Risk View**: L1 (per-repo) + L2 (cross-repo) risk management

See [ARCHITECTURE.md](ARCHITECTURE.md#distortion-analysis-framework) for detailed framework documentation.

## Review Flow

```
/review [PR number]
   → /project-guide + /review-code
   → Reviews code quality + business logic alignment
   → References knowledge/domain/ for domain knowledge validation
```

## Templates

CLysis provides templates for consistent documentation across projects:

| Template | Location | Purpose |
|----------|----------|---------|
| Domain Knowledge | `legacy-knowledge/prompts/domain-knowledge-template.md` | 8-section unified structure for organizing domain knowledge |
| Non-Functional Analysis | `legacy-knowledge/prompts/non-functional-analysis-template.md` | Non-functional requirements analysis template |
| CLAUDE.md | `docs/claude-md-template.md` | Minimal project configuration template |
| Workflow Example | `docs/full-workflow-example.md` | End-to-end workflow demonstration |

The domain knowledge template uses a structured 8-section format (Overview, Data Model, Business Rules, Process Flow, External Integrations, Constraints, Usage Context, Related Domains) to ensure consistent and complete documentation. See [ARCHITECTURE.md](ARCHITECTURE.md#template-system) for design philosophy.

## Domain Knowledge

**Domain knowledge is project-specific and NOT included in the public repository.**

Each project maintains its own `knowledge/domain/` directory with:
- Business rules and logic
- Data structures and enum definitions
- External API specifications
- System architecture and service responsibilities
- Technical constraints and known limitations

Domain knowledge is accumulated through the investigation and analysis phases and persisted to `knowledge/domain/`.

## Terminology

This project uses **Sengoku-style terminology** based on Japanese feudal hierarchy by default. This is purely a naming convention and can be fully customized to match your team culture.

| Default Term | English | Role |
|--------------|---------|------|
| Shogun | General | Team leader who coordinates agents |
| Ashigaru | Foot Soldier | Worker agents executing specific tasks |
| Karo | Chief Retainer | Task planner and decomposition specialist |
| Metsuke | Inspector | Quality assurance and code review specialist |

See `config/terminology.md` for full customization instructions.

## Customization

### Terminology

Edit `config/terminology.md` to customize role names and communication style:

```markdown
| Default (JA) | Default (EN) | Your Custom | Role Description |
|-------------|-------------|-------------|-----------------|
| Shogun | General | Tech Lead | Team leader who coordinates agents |
| Ashigaru | Foot Soldier | Engineer | Task execution specialist |
```

Supported styles:
- **Sengoku Japanese** (default): "My lord, I have received the mission."
- **Business Japanese**: "Understood. Starting the task now."
- **English Casual**: "Got it! Starting the task now."
- **English Formal**: "Understood. Initiating the assigned task."

### Project Paths

Update paths in CLAUDE.md to match your project structure.

### Technology Stack

Agent definitions reference generic frameworks (e.g., "Backend framework" → specify Laravel/Rails/Django).
Update agent definitions to reference your actual tech stack.

## Quality Validation

Run the validation script to verify plugin structure and completeness:

```bash
python3 validate_plugins.py
```

This checks:
- Plugin structure (skills, commands, examples, .claude-plugin/)
- Skill frontmatter format
- Command frontmatter format
- marketplace.json and plugin.json validity

## Acknowledgments

This project was inspired by and built upon ideas from the following projects:

- [takt](https://github.com/nrslib/takt) by nrslib - AI agent orchestration framework using YAML-defined workflows
- [pm-skills](https://github.com/phuryn/pm-skills) by phuryn - AI-powered product management skills marketplace for Claude Code
- [multi-agent-shogun](https://github.com/yohey-w/multi-agent-shogun) by yohey-w - Bushido-inspired multi-agent system with feudal hierarchy orchestration

## License

MIT

## Contributing

PRs welcome! This is a generic toolkit designed to adapt to any legacy codebase.

When contributing:
- Keep skills and agents generic (no project-specific hardcoding)
- Use placeholders like "Backend framework" or "project-specific domain knowledge"
- Document customization points in agent headers
- Add examples to `examples/` if adding new workflows

## Links

- [GitHub Repository](https://github.com/t-hasuike/CLysis)
- [Architecture Documentation](ARCHITECTURE.md)
- [Migration Guide](docs/migration-guide.md)
