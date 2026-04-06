---
name: current-legacy
description: A skill for progressively understanding legacy code through iterative concrete-to-abstract cycles. Three maps (system overview, DFD, I/O interface) are "grown" rather than "built."
argument-hint: "Phase 0 | Phase 1 [change theme] | Phase 2 | Phase 3"
---

# /current-legacy -- Legacy Code Mastery Skill

> This is a generic skill from [CLysis](https://github.com/t-hasuike/CLysis).
> Terminology can be customized via `config/terminology.md`.

## Overview
A skill for progressively understanding legacy code through iterative concrete-to-abstract cycles.
Three maps (system overview, DFD, I/O interface) are "grown" rather than "built."

See config/terminology.md for term customization

## Prerequisites

**First Run**:
- Local repository clones must exist (see CLAUDE.local.md)
- Other files (overview.md, etc.) are generated in Phase 0; not required for startup

**Second Run and After**:
- Phase 0 deliverables (overview.md, diagrams) must exist
- `knowledge/README.md` must be current

### Prerequisites Checklist

| Prerequisite | Check Method | First Run | Subsequent Runs |
|-------------|-----------|-----------|-----------------|
| Local repository clones | `ls` to verify paths | Required | Required |
| `knowledge/system/01_overview/birdseye_project_overview.md` | File exists? | Not needed (Phase 0 generates) | Required |
| `knowledge/README.md` | File exists? | Not needed (use `/project-guide` for guidance) | Required |
| `knowledge/system/02_structure/` directory | Directory exists? | Not needed (Phase 0 creates) | Required |

**Note**: During first run, Phase 0 automatically creates `knowledge/system/` subdirectories with `mkdir -p` if they don't exist.

## Phase 0: Foundation Building (first time only)

### Purpose
Auto-collect "indisputable facts" readable from code, and derive the minimal set of questions to ask humans.

### Procedure

**Step 1: Auto-collection (no human input required)**
Auto-collect the following from each repository:
- README.md
- docker-compose.yml / Dockerfile
- .env.example (.env excluded -- security)
- Dependency management files (composer.json / package.json / go.mod / build.gradle, etc.)
- Root directory file structure
- routes/ (API endpoint structure)
- Console/Commands or equivalent CLI commands directory
- Jobs/ or equivalent async job directory
- app/Services/ or equivalent service layer directory structure (directory listing only, not file contents)
- config/ files (connection settings, third-party integrations)

If DB schema (schema.duckdb) is available, extract table list and foreign key relationships.
If schema.duckdb is not available:
1. Estimate table names and relationships from Eloquent Models / ORM entity classes
2. Estimate table structure from migration files
3. If neither is available, note as "DB structure unknown" in the unknowns list

### Additional Collection Items (Dynamic / Hidden Assets)

| Collection Target | Method | Output |
|------------------|--------|--------|
| **Orphan Endpoints** | Glob `public/` and root directories for executable files (.php, .asp, .cgi, .pl, etc.) | Endpoint list |
| **OS Scheduled Jobs** | Search crontab, `infra/` shell scripts, Docker cron definitions | Scheduled job list |
| **Database Logic** | Extract Triggers, Stored Procedures, Views definitions (skip if unavailable) | DB-layer logic list |
| **External Service Integrations** | Full-codebase grep for `http://`, `https://`, `curl`, `guzzle`, `axios`, `fetch` keywords | External service endpoints |

**Base Quantitative Scan** (counting only — do not read file contents):
- Route count
- Model/Entity count
- Table count (from schema or migrations)
- Total file count per major language
- Service/UseCase count

**Risk Quantitative Scan** (code metrics for risk assessment):

| Metric | Method | Purpose |
|--------|--------|---------|
| **File LOC Top 10** | `wc -l` on all files; rank by line count | Identify bloated "God Classes" and baseline investigation difficulty |
| **Incoming Coupling** | Serena `find_referencing_symbols` or grep for references | Determine maximum impact radius |
| **Dynamic Table Reference** | Regex search for patterns like `table_{year}` or string-based table names | Discover hidden table dependencies |
| **Raw SQL Queries** | grep for `DB::raw`, `query(`, direct SQL literals (patterns vary by language) | Identify complex hidden joins and business logic in SQL |

### Code Freshness & EOL Risk

| Category | Method | Purpose |
|----------|--------|---------|
| **Code Liveness** | Git Blame for last update date; flag files not updated in 1+ year as "dormant" | Prioritize investigation targets; identify dead code areas |
| **Runtime/Library EOL Risk** | Extract dependency versions from composer.json, package.json, go.mod, build.gradle; check for deprecated APIs and EOL runtimes | Early security and maintainability risk detection |

> Phase 0 quantitative scanning is limited to **counting** (how many routes, models, tables exist). **Reading** the contents or analyzing complexity belongs to Phase 1.

**Validation**: ~65-73% of project information is automatically determined from README, composer.json, package.json, etc.

**Step 2: Organize "what we know"**
Organize information identified from auto-collection using the following four categories:

**1. Technology Stack**
- Framework, language version, major dependencies per repository

**2. Repository Roles**
- What each repository does (from README)

**3. Inter-Repository Connections**
- Clues about how repositories connect (API URLs in .env.example, shared DB, etc.)

**4. Batch & Infrastructure**
- Scheduled tasks, queue workers, infrastructure components


**Step 3: Present "what we don't know" as questions**
Generate questions dynamically based on what Step 1-2 revealed and what remains unknown. The following are reference examples of common question categories:

```
Please provide the following items. The rest has been auto-collected:

1. Business domain of the service (1-2 sentences)
   -> What does the service provide and to whom?

2. Target user names and specific roles
   -> README mentions "for XX", but please describe each user's specific role

3. Domain-specific terminology meanings
   -> Meanings of proprietary terms (plan names, etc.) found during auto-collection

4. Industry/attributes per user type
   -> Specific industries that terms like "Partner" refer to

5. Importance assessment
   -> Which repository is most critical, which has highest change frequency

6. Legacy system positioning
   -> Migration status of old systems, whether still in use

7. Supplementary inter-repository integration details
   -> Confirmation of integrations that could not be auto-estimated

8. Organization/brand name context
   -> Official meanings of proper nouns appearing in README

9. Production domain mapping (optional)
   -> URLs where each service is running
```

**Step 4: Generate initial overview.md and overview diagram**
Integrate Step 2 (auto-collection results) + Step 3 (human answers) to:
- Generate initial version of overview.md
- Generate initial system overview diagram (mermaid)
- "Known" list
- "Still unknown" list (this is most important -- targets for Phase 1 investigation)

### When working with multiple repositories (5+)
1. Start with the most critical/central repository (usually the main backend API)
2. Proceed to repositories that directly depend on or are depended upon by the first
3. Complete Phase 0 for all repositories before moving to Phase 1
4. The system overview diagram should include ALL repositories, not just individually scanned ones
5. Inter-repository connections discovered in Step 2 should be cross-referenced across repositories

### Key Principles
- Steps 1-2 can execute without human input
- Step 3 questions are dynamically generated based on auto-collection results (not fixed questions)
- AI structures the state of "not knowing what to ask"

## Phase 1: Dig from the Concrete (core of iteration)

### Purpose
Select one specific change theme and trace it through the system. Map fragments emerge as a byproduct of tracing.

### Procedure
1. User specifies a change theme (e.g., "I want to add a new product category")
2. Trace impact scope with /change-impact
3. Record the following discovered during tracing:
   - Inter-repository connections (API calls, shared DB, shared Enums, etc.)
   - Hidden outputs (email, CSV, batch processing, external API integrations)
   - Hardcoded locations
   - Technical debt
4. Organize related Services with /current-spec
5. For cross-repository cases, use /current-spec (CROSS) for diff analysis
6. Output:
   - Impact analysis report (reports/)
   - Overview diagram update diff
   - DFD fragments
   - "Unknown" list update (resolved items/newly discovered items)

### Key Principles
- Do not write code using "likely names." Always verify existence with Serena
- Write fix examples only after confirming actual code structure
- For unfamiliar repositories, use /current-spec to understand the full picture before incorporating

## Phase 2: Audit to Eliminate Falsehoods

### Purpose
Verify the accuracy of Phase 1 deliverables. AI can hallucinate.

### Procedure
1. **Metsuke** (inspector) audits deliverables
2. Verification items:
   - Do all method names and class names actually exist?
   - Are all file paths correct?
   - Do code snippets match actual code?
   - Are project-specific mandatory rules properly considered?
3. Correct findings and re-audit
4. Output: Audited deliverables (with corrections applied)

## Phase 3: Return to the Abstract

### Purpose
Integrate fragments obtained in Phase 1-2 and update the three maps. Persist knowledge.

### Procedure
1. Add connections/flows discovered in impact analysis to the overview diagram
2. Add data flows to the DFD
3. Add entry/exit points of each system to the I/O interface diagram
4. Persist domain knowledge to the domain knowledge directory
   - **Ashigaru (scribe)** handles this task
   - Under `knowledge/domain/`
5. Update the "known/unknown" list
6. Output:
   - Update the 3 diagrams in the diagram storage location
   - Add new knowledge to the domain knowledge directory

### Phase 3 Mandatory Rule

**After completing Phase 1-2 investigations, Phase 3 (map update) MUST be executed.**

If investigation ends without Phase 3, findings remain trapped in the session, and subsequent investigations will re-cover the same ground. By updating maps and domain knowledge in Phase 3:
- The starting point for the next Phase 1 advances
- The "unknown" list shrinks
- Team-wide understanding accumulates

## Iteration
Repeat Phase 1-3 with different change themes. With each iteration:
- The accuracy of the three maps improves
- The "unknown" list shrinks
- From the second theme onward, "same pattern here" recognition kicks in, increasing speed

## Team Composition Templates

### Medium Scale (Standard)
| Role | Assignment | Notes |
|------|-----------|-------|
| **Ashigaru A** | Code tracing and impact analysis (investigator role) | - |
| **Ashigaru B** | Knowledge organization and diagram updates (scribe role) | - |

### Large Scale (Cross-Repository)
| Role | Assignment | Notes |
|------|-----------|-------|
| **Ashigaru A** | Repository A investigation (investigator) | - |
| **Ashigaru B** | Repository B investigation (investigator) | - |
| **Ashigaru C** | Knowledge integration and diagram updates (scribe) | - |
| **Metsuke** | Quality audit (deployed Phase 2) | Independent verification |

## Agent Pattern Mapping
| Pattern | Implementation | Phase |
|---------|---------------|-------|
| Advanced RAG | schema.duckdb + Serena | All Phases |
| ReAct | /change-impact, /current-spec | Phase 1 |
| Self-Reflection | Metsuke audit | Phase 2 |
| Multi-Agent | Shogun + Ashigaru team + Metsuke | Phase 1-3 |
| Plan-and-Execute | /change-impact + Phase decomposition | Phase 1 |
| Knowledge Graph Memory | domain knowledge directory + diagrams | Phase 3 |
| Sequential Chain | Phase 0→1→2→3 iteration | Overall |

---

## I/O Specification

### INPUT
| Type | Description | Required/Optional | Example |
|------|-------------|-------------------|---------|
| Phase | Phase 0, 1, 2, or 3 | Required | `Phase 0`, `Phase 1` |
| Change theme | Specific change theme (Phase 1 only) | Required for Phase 1 | `I want to add a new product category` |
| Investigation target | Target repositories or features | Optional | `backend`, `order processing feature` |

### OUTPUT
| Type | Format | Destination |
|------|--------|-------------|
| Phase 0 deliverables | overview.md + system overview diagram + known/unknown list | Project information directory (`knowledge/system/`) |
| Phase 1 deliverables | Impact analysis report + Service specs + DFD fragments + unknown list update | `reports/`, diagram storage location |
| Phase 2 deliverables | Audited deliverables (with corrections applied) | `reports/` (updated) |
| Phase 3 deliverables | Updated 3 maps + domain knowledge | Diagram storage location, domain knowledge directory |

### Prerequisites
- Serena MCP is running
- Phase 0: Repository access available
- Phase 1-3: Phase 0 completed

### Downstream Skills (Pipeline)
Phase 0 -> Phase 1 -> Phase 2 -> Phase 3 -> (return to Phase 1 and iterate)

### Quality Checkpoints
- [ ] Phase 0: Obtained 65-73% of information through auto-collection
- [ ] Phase 1: Confirmed actual code before reporting (not assumptions)
- [ ] Phase 2: Verified all method names and class names actually exist
- [ ] Phase 3: Persisted domain knowledge to the domain knowledge directory
