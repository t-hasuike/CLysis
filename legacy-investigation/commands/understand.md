---
description: Support legacy code specification understanding. Execute the project-guide -> investigate -> service-spec skill chain.
argument-hint: "<feature or process name to understand>"
---

# /understand -- Code Comprehension Flow

## Overview

A workflow for systematically executing specification understanding and code reading of legacy code.

## Workflow

### Step 1: Get Reference Guide

Apply **project-guide** skill:

- Identify the document reference order needed for investigation and analysis

$ARGUMENTS

> **Checkpoint**: "Reference guide prepared. Ready to proceed to the next phase (code investigation)?"

### Step 2: Code Investigation

Apply **investigate** skill:

- Explore the code flow and dependency relationships of the target feature
- Identify key classes, methods, and tables

> **Checkpoint**: "Investigation results ready. Ready to proceed to the next phase (specification organization)?"

### Step 3: Systematic Specification Organization

Apply **service-spec** skill:

- Systematically document the specification of discovered key Services
- Organize method lists, dependencies, and business rules

### Step 4: Suggest Next Actions

- "To accumulate as domain knowledge, use `/build-knowledge`"
- "If planning changes, proceed with impact analysis using `/investigate-flow`"
