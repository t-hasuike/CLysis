---
description: Systematically execute impact investigation for legacy systems. Sequentially execute the project-guide -> investigate -> service-spec -> impact-analysis skill chain.
argument-hint: "<description of the change>"
---

# /investigate-flow -- Impact Investigation Flow

## Overview

A workflow for systematically investigating the impact scope when adding new features or changing specifications.
Sequentially execute 4 skills and output the final ADR-format impact analysis report.

## Workflow

### Step 1: Get Reference Guide

Apply **project-guide** skill:

- Analyze the task overview and identify the order of documents to reference
- Present the optimal reference order from knowledge/system/ and knowledge/domain/

$ARGUMENTS

> **Checkpoint**: "Reference guide prepared. Ready to proceed to the next phase (investigation)?"

### Step 2: Codebase Investigation

Apply **investigate** skill:

- Pre-read documents identified in Step 1
- Explore target classes/features using Serena's symbolic search
- Create investigation report with file path:line numbers

> **Checkpoint**: "Investigation results ready. Ready to proceed to the next phase (specification organization)?"

### Step 3: Service Specification Organization

Apply **service-spec** skill:

- Organize specifications of high-impact Services discovered in Step 2 in detail
- Document method lists, dependencies, and business rules
- If spanning multiple Services, also apply **service-spec (CROSS)** skill

> **Checkpoint**: "Specification organization complete. Ready to proceed to the next phase (impact analysis)?"

### Step 4: Impact Analysis

Apply **impact-analysis** skill:

- Create an ADR-format impact analysis report based on Step 2-3 results
- Includes risk assessment and phased implementation plan

### Step 5: Suggest Next Actions

- "If you'd like to proceed with the fix, use `/implement`"
- "If deeper investigation is needed, use `/deep-dive`"
- "To accumulate as domain knowledge, use `/build-knowledge`"
