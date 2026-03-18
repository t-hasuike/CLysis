# CLysis

> AI-powered framework for understanding, analyzing, and modernizing legacy systems.

Systematic support for investigation, analysis, and modernization of legacy systems using AI agent teams.
14 domain-specific skills and 6 workflow commands across 4 plugins.

## Repository Structure

```
CLysis/
├── .claude-plugin/            # Marketplace manifest
├── agents/                    # Agent definitions (karo, metsuke, ashigaru-*)
├── assessment/                # Quality evaluation criteria & maturity model
├── config/                    # Terminology customization
├── docs/                      # Templates, workflow examples, migration guide
├── legacy-analysis/           # Plugin: impact-analysis, legacy-analyze, distortion-analysis
│   ├── .claude-plugin/
│   ├── commands/
│   ├── examples/
│   └── skills/
├── legacy-execution/          # Plugin: code-review, create-pr, propose-changes
│   ├── .claude-plugin/
│   ├── commands/
│   ├── examples/
│   └── skills/
├── legacy-investigation/      # Plugin: investigate, project-guide, service-spec
│   ├── .claude-plugin/
│   ├── commands/
│   ├── examples/
│   └── skills/
├── legacy-knowledge/          # Plugin: build-knowledge, archive-output, templates
│   ├── .claude-plugin/
│   ├── examples/
│   ├── prompts/
│   └── skills/
├── ARCHITECTURE.md
├── LICENSE
├── README.md
└── validate_plugins.py
```

## Plugins

| Plugin | Skills | Commands | Description |
|--------|--------|----------|-------------|
| [legacy-investigation](./legacy-investigation/) | 3 | 3 | Investigation & understanding (project-guide, investigate, service-spec) |
| [legacy-analysis](./legacy-analysis/) | 3 | 1 | Analysis & planning (impact-analysis, legacy-analyze, distortion-analysis) |
| [legacy-execution](./legacy-execution/) | 3 | 2 | Execution & review (propose-changes, create-pr, code-review) |
| [legacy-knowledge](./legacy-knowledge/) | 5 | 0 | Knowledge accumulation (build-knowledge, archive-output, templates, prd-generate, doc-update) |

## Prerequisites

- **Claude Code** — Required
- **Serena MCP** — Recommended. Enables semantic code search for `/investigate`, `/service-spec`. Skills work without it but with reduced accuracy.
- **GitHub MCP** — Optional. Required for `/create-pr` and `/code-review`.

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
claude plugin install legacy-investigation@CLysis legacy-analysis@CLysis legacy-execution@CLysis legacy-knowledge@CLysis

# Verify installation
claude plugin list
```

#### Local Installation

If running locally or adding to an existing marketplace:

```bash
# Add this repository to the marketplace
claude plugin marketplace add CLysis /path/to/CLysis

# Then install plugins as above
claude plugin install legacy-investigation@CLysis legacy-analysis@CLysis legacy-execution@CLysis legacy-knowledge@CLysis

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
| **legacy-investigation** | project-guide, investigate, service-spec | Code exploration, service specification, documentation reference |
| **legacy-analysis** | impact-analysis, legacy-analyze, distortion-analysis | Impact analysis, system overview, code quality patterns |
| **legacy-execution** | propose-changes, create-pr, code-review | Change proposals, PR creation, automated code review |
| **legacy-knowledge** | build-knowledge, archive-output, templates, prd-generate, doc-update | Knowledge extraction, domain documentation, team templates, PRD generation, document updates |

### Skill Chain Patterns

Common workflows for analyzing and modernizing legacy systems:

#### Impact Analysis Chain

Investigate the full impact of proposed changes:

```bash
/project-guide [your task]
  → /investigate [target service or area]
  → /service-spec [high-impact services]
  → /impact-analysis [change description]
```

**Use case**: Before implementing a change, understand its ripple effects across the codebase.

#### Bug Investigation Chain

Locate and understand the root cause of defects:

```bash
/project-guide [bug description]
  → /investigate [suspected area]
  → /service-spec [related services]
  → /distortion-analysis [repository] [area]
```

**Use case**: Systematically identify code quality patterns and risk areas.

#### System Understanding Chain

Build comprehensive domain knowledge:

```bash
/project-guide [feature or module]
  → /investigate [target service]
  → /service-spec [service documentation]
  → /build-knowledge [output path]
```

**Use case**: Document and archive understanding of critical legacy components.

### First Steps

1. Use the skills in your Claude Code session:

```bash
/project-guide my-legacy-feature
/investigate AccountService
/impact-analysis [describe your planned change]
```

2. Build domain knowledge from your investigations:

```bash
/build-knowledge output/investigation-results.md
```

3. Use the execution skills to propose and review changes:

```bash
/propose-changes [change description]
/create-pr [task description]
/code-review [PR number]
```

## Plugin Dependencies and Recommended Setup

### Dependency Matrix

Some commands reference skills from other plugins. Ensure required plugins are installed:

| Command | Required Plugins | Purpose |
|---------|-----------------|---------|
| `/investigate-flow` | legacy-investigation + legacy-analysis | Full investigation pipeline with impact analysis |
| `/bug-hunt` | legacy-investigation + legacy-analysis | Bug root cause analysis |
| `/deep-dive` | legacy-analysis (+ others for context) | System-wide analysis |
| `/implement` | legacy-execution + legacy-investigation | End-to-end change implementation |
| `/review` | legacy-execution + legacy-investigation | PR review with context |

### Recommended Setup

**For all users**: Install all 4 plugins to unlock full functionality and workflow chains:

```bash
claude plugin install legacy-investigation@CLysis legacy-analysis@CLysis legacy-execution@CLysis legacy-knowledge@CLysis
```

**By team role**:

| Team Role | Required Plugins | Install Command |
|-----------|-----------------|-----------------|
| **Investigators** (understand legacy code) | legacy-investigation + legacy-analysis | `legacy-investigation@CLysis legacy-analysis@CLysis` |
| **Implementers** (make changes) | legacy-execution + legacy-investigation | `legacy-execution@CLysis legacy-investigation@CLysis` |
| **Reviewers** (validate changes) | legacy-execution + legacy-analysis | `legacy-execution@CLysis legacy-analysis@CLysis` |
| **Knowledge Architects** (document systems) | legacy-knowledge + legacy-investigation | `legacy-knowledge@CLysis legacy-investigation@CLysis` |
| **Full Teams** | All 4 plugins | `legacy-investigation@CLysis legacy-analysis@CLysis legacy-execution@CLysis legacy-knowledge@CLysis` |

## Workflow Commands

| Command | Plugin | Description |
|---------|--------|-------------|
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
| `/investigate` | legacy-investigation | Code investigation with semantic search (Serena MCP) |
| `/service-spec` | legacy-investigation | Service/UseCase specification documentation |
| `/impact-analysis` | legacy-analysis | Impact analysis with ADR-format reports |
| `/legacy-analyze` | legacy-analysis | Legacy codebase understanding workflow (Phase 0->1->2->3) |
| `/distortion-analysis` | legacy-analysis | Detect code distortion patterns and organize in Part A/B/C framework |
| `/propose-changes` | legacy-execution | Generate code diffs with context |
| `/create-pr` | legacy-execution | Create PR with ADR summary and checklist |
| `/code-review` | legacy-execution | PR review with code quality and domain knowledge validation |
| `/build-knowledge` | legacy-knowledge | Extract and persist domain knowledge from investigation results |
| `/archive-output` | legacy-knowledge | Archive investigation outputs for knowledge reuse |
| `/templates` | legacy-knowledge | General team operation templates (for leaders) |
| `/prd-generate` | legacy-knowledge | Reverse-engineer PRD from existing codebase (Phase 1-3 workflow) |
| `/doc-update` | legacy-knowledge | Update knowledge documents for target audience (developer, PM, onboarding) |

## Initial Setup

After installing the plugins, set up your project structure:

### 1. Create directory structure

```bash
# Private directories (not tracked by git)
mkdir -p input/{domain,project,local_dev,staging,prompts}
mkdir -p output

# Preserve directory structure in git
touch input/domain/.gitkeep
touch input/project/.gitkeep
touch input/local_dev/.gitkeep
touch input/staging/.gitkeep
touch input/prompts/.gitkeep
touch output/.gitkeep
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
- **Domain Knowledge**: Map your `input/domain/` files

### 4. Start accumulating knowledge

```
/project-guide [your first task]
/investigate [target service or module]
/build-knowledge [investigation output path]
```

Each investigation builds your domain knowledge in `input/domain/`.

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
    │  • Reports generated to output/                    │
    │  • Domain knowledge persisted to input/domain/     │
    └────────────────────────────────────────────────────┘
```

## Investigation Flow

Commands provide pre-configured pipelines for common workflows:

```
/investigate-flow [target]
   → /project-guide + /investigate + /service-spec + /impact-analysis
   → All-in-one investigation pipeline
   ↓
/build-knowledge [output path]
   → Persists domain knowledge to input/domain/
```

## Distortion Analysis Flow

Detect code-level risks ("distortions") and organize them systematically:

```
/distortion-analysis [repository] [area]
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
   → /project-guide + /code-review
   → Reviews code quality + business logic alignment
   → References input/domain/ for domain knowledge validation
```

## Domain Knowledge

**Domain knowledge is project-specific and NOT included in the public repository.**

Each project maintains its own `input/domain/` directory with:
- Business rules and logic
- Data structures and enum definitions
- External API specifications
- System architecture and service responsibilities
- Technical constraints and known limitations

The `/build-knowledge` skill bridges the gap by extracting domain knowledge from investigation results and persisting it to `input/domain/`.

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
