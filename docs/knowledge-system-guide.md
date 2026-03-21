# Knowledge System Guide

## Overview

This guide defines the target file list for `knowledge/system/`. Since `knowledge/` itself is `.gitignore`-excluded (project-specific), this guide lives in `docs/` as a shared reference.

Use this checklist to understand what files should eventually exist in `knowledge/system/` and when to create them.

---

## Customization Policy

This is a recommended structure, not a requirement. Add or remove files freely to match your project's needs. The goal is to capture the knowledge that agents and developers actually need — no more, no less.

---

## Target File Checklist

### Core (Required)

- [ ] `01_overview/overview.md` — Project overview: purpose, target users, repository list
- [ ] `02_structure/repositories.md` — Repository roles and responsibilities
- [ ] `02_structure/tech_stack.md` — Technology stack details
- [ ] `03_behavior/data_flow.md` — Data Flow Diagram (DFD)
- [ ] `03_behavior/io_interfaces.md` — I/O interfaces for each system

### Optional

- [ ] `04_change_impact/service_responsibilities.md` — Service/UseCase responsibility map (useful when planning changes)
- [ ] `04_change_impact/impact_analysis_template.md` — Impact analysis template (useful when planning changes)
- [ ] `operations/non_functional_requirements.md` — Non-functional requirements (when relevant)

---

## File Descriptions

| File | Why it exists | Created in |
|------|--------------|------------|
| `01_overview/overview.md` | Gives agents the business context needed to interpret code correctly. Without it, agents lack the "why" behind system design. | Phase 0 |
| `02_structure/repositories.md` | Maps each repository to its role. Prevents agents from looking in the wrong place for features or APIs. | Phase 0 |
| `02_structure/tech_stack.md` | Ensures agents apply the right framework knowledge and tooling assumptions when analyzing code. | Phase 0 |
| `03_behavior/data_flow.md` | Captures how data moves across systems. Enables agents to trace side effects and understand cross-repo dependencies. | Phase 1 (fragments) → Phase 3 (complete) |
| `03_behavior/io_interfaces.md` | Documents the inputs and outputs of each system boundary. Essential for impact analysis before making changes. | Phase 1 (fragments) → Phase 3 (complete) |
| `04_change_impact/service_responsibilities.md` | Maps Services and UseCases to their business responsibilities. Needed when assessing the blast radius of a change. | Phase 3 |
| `04_change_impact/impact_analysis_template.md` | Standardizes how impact analyses are documented. Reduces variability across investigations. | Phase 3 |
| `operations/non_functional_requirements.md` | Captures performance, availability, and compliance constraints that affect design decisions. | As needed |

---

## Creation Timeline by Phase

### Phase 0 — Project Orientation
- `01_overview/overview.md` is created as the initial draft
- `02_structure/repositories.md` is created as the initial draft
- `02_structure/tech_stack.md` is created as the initial draft

These three files form the baseline context for all subsequent agent work.

### Phase 1 — Legacy Investigation
- Fragments of `03_behavior/data_flow.md` and `03_behavior/io_interfaces.md` are produced as byproducts of each investigation
- These fragments are stored in `output/` and not yet promoted to `knowledge/system/`

### Phase 3 — Knowledge Consolidation (Map Update)
- Fragments from Phase 1 are merged and promoted to `03_behavior/data_flow.md` and `03_behavior/io_interfaces.md`
- `04_change_impact/service_responsibilities.md` is created based on accumulated investigation results
- Phase 3 must be executed after every Phase 1 investigation; skipping it leaves the maps in a partial state

---

## Related

- `/legacy-analyze` skill — defines the Phase 0 → Phase 1 → Phase 3 cycle that produces these files
- `docs/full-workflow-example.md` — end-to-end example of the investigation workflow
