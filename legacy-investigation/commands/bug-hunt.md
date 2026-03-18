---
description: Support bug root cause identification and fix strategy formulation. Execute project-guide -> investigate -> service-spec skill chain.
argument-hint: "<bug symptoms / error description>"
---

# /bug-hunt -- Bug Investigation Flow

## Overview

A workflow for systematically executing from cause identification to fix strategy formulation for bug fix tasks.

## Workflow

### Step 1: Get Reference Guide

Apply **project-guide** skill:

- Identify the document reference order needed for bug fixing

$ARGUMENTS

> **Checkpoint**: "Reference guide prepared. Ready to proceed to the next phase (cause investigation)?"

### Step 2: Cause Investigation

Apply **investigate** skill:

- Trace the code flow from the error content/symptoms
- Identify the cause location with file path:line number
- Record discovered risks

> **Checkpoint**: "Narrowed down the likely cause. Ready to proceed to the next phase (specification verification)?"

### Step 3: Verify Relevant Service Specification

Apply **service-spec** skill:

- Organize the specification of the cause location's Service and verify correct behavior
- Provide judgment material for the fix strategy

### Step 4: Suggest Next Actions

- "If you'd like to proceed with the fix, use `/implement`"
- "If the impact scope is wide, proceed with impact analysis using `/investigate-flow`"
