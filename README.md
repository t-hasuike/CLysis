# decouple-legacy

> AI-powered framework for understanding, analyzing, and modernizing legacy systems.

レガシーシステムの調査・分析・修正を AI エージェントチームで体系的に支援するフレームワーク。
10のドメイン特化スキルと6つのワークフローコマンドを、4つのプラグインで提供する。

## Repository Structure

```
decouple-legacy-skills/
├── .claude-plugin/            # Marketplace manifest
├── agents/                    # Agent definitions (karo, metsuke, ashigaru-*)
├── assessment/                # Quality evaluation criteria & maturity model
├── config/                    # Terminology customization
├── docs/                      # Templates, workflow examples, migration guide
├── legacy-analysis/           # Plugin: impact-analysis, legacy-analyze
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
├── legacy-knowledge/          # Plugin: build-knowledge, templates
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
| [legacy-investigation](./legacy-investigation/) | 3 | 3 | 調査・理解（project-guide, investigate, service-spec） |
| [legacy-analysis](./legacy-analysis/) | 2 | 1 | 分析・計画（impact-analysis, legacy-analyze） |
| [legacy-execution](./legacy-execution/) | 3 | 2 | 実行・レビュー（propose-changes, create-pr, code-review） |
| [legacy-knowledge](./legacy-knowledge/) | 2 | 0 | 知識蓄積（build-knowledge） |

## Quick Start

### Claude Code CLI (Recommended)

1. Add this repository to the marketplace:

```bash
claude plugin marketplace add decouple-legacy /path/to/decouple-legacy
```

2. Install the plugin you need:

```bash
# Investigation & understanding
claude plugin install legacy-investigation@decouple-legacy

# Analysis & planning
claude plugin install legacy-analysis@decouple-legacy

# Execution & review
claude plugin install legacy-execution@decouple-legacy

# Knowledge management
claude plugin install legacy-knowledge@decouple-legacy
```

3. Use the skills and commands in your Claude Code session:

```
/investigate-flow [target feature]
/impact-analysis [change description]
```

### Manual Installation

Copy individual skills to your project:

```bash
# Copy skills from a specific plugin
cp -r decouple-legacy/legacy-investigation/skills/* .claude/skills/

# Or copy commands
cp -r decouple-legacy/legacy-investigation/commands/* .claude/commands/
```

## Plugin Dependencies

Some commands reference skills from other plugins. To use these commands, install the required plugins:

| Command | Required Plugins |
|---------|-----------------|
| `/investigate-flow` | legacy-investigation + legacy-analysis |
| `/review` | legacy-investigation + legacy-execution |

**Recommended**: Install all 4 plugins for full functionality:

```bash
claude plugin install legacy-investigation@decouple-legacy
claude plugin install legacy-analysis@decouple-legacy
claude plugin install legacy-execution@decouple-legacy
claude plugin install legacy-knowledge@decouple-legacy
```

## Workflow Commands

| Command | Plugin | Description |
|---------|--------|-------------|
| `/investigate-flow` | legacy-investigation | 影響調査フロー（4スキルチェーン） |
| `/bug-hunt` | legacy-investigation | バグ調査フロー |
| `/understand` | legacy-investigation | コード理解フロー |
| `/deep-dive` | legacy-analysis | システム全体の深掘り分析 |
| `/implement` | legacy-execution | 修正提案→PR作成（2段階人間確認） |
| `/review` | legacy-execution | PRレビューフロー |

## Skills Overview

| Skill | Plugin | Description |
|-------|--------|-------------|
| `/project-guide` | legacy-investigation | Context-aware documentation reference guide |
| `/investigate` | legacy-investigation | Code investigation with semantic search (Serena MCP) |
| `/service-spec` | legacy-investigation | Service/UseCase specification documentation |
| `/impact-analysis` | legacy-analysis | Impact analysis with ADR-format reports |
| `/legacy-analyze` | legacy-analysis | Legacy codebase understanding workflow (Phase 0→1→2→3) |
| `/propose-changes` | legacy-execution | Generate code diffs with context |
| `/create-pr` | legacy-execution | Create PR with ADR summary and checklist |
| `/code-review` | legacy-execution | PR review with code quality and domain knowledge validation |
| `/build-knowledge` | legacy-knowledge | Extract and persist domain knowledge from investigation results |
| `/templates` | legacy-knowledge | General team operation templates (for leaders) |

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
cp decouple-legacy/.gitignore.template .gitignore
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
| 将軍 (Shogun) | General | Team leader who coordinates agents |
| 足軽 (Ashigaru) | Foot Soldier | Worker agents executing specific tasks |
| 家老 (Karo) | Chief Retainer | Task planner and decomposition specialist |
| 目付 (Metsuke) | Inspector | Quality assurance and code review specialist |

See `config/terminology.md` for full customization instructions.

## Customization

### Terminology

Edit `config/terminology.md` to customize role names and communication style:

```markdown
| Default (JA) | Default (EN) | Your Custom | Role Description |
|-------------|-------------|-------------|-----------------|
| 将軍 (Shogun) | General | Tech Lead | Team leader who coordinates agents |
| 足軽 (Ashigaru) | Foot Soldier | Engineer | Task execution specialist |
```

Supported styles:
- **Sengoku Japanese** (default): 「上様、任務を承りました」
- **Business Japanese**: 「承知しました。タスクを開始します」
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

- [GitHub Repository](https://github.com/t-hasuike/decouple-legacy-skills)
- [Architecture Documentation](ARCHITECTURE.md)
- [Migration Guide](docs/migration-guide.md)
