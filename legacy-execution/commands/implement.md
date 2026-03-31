---
description: Based on impact analysis results, propose changes and create PR. Execute the create-pr --plan -> (human review) -> create-pr --exec skill chain.
argument-hint: "<impact analysis report path>"
---

# /implement -- Change Proposal and Implementation Flow

## Overview

A workflow for proposing specific code changes based on impact analysis results and creating PR after approval.
Includes **2 human confirmation points**.

## Workflow

### Step 1: Create Change Proposal

Apply **create-pr** skill with `--plan` flag:

- Read the impact analysis report and present Phase-specific changes in diff format
- Includes change reason, impact scope, and test strategy

$ARGUMENTS

> **[Human Confirmation Point 1]**: "Change proposal is ready. Please review the content. PR creation will proceed upon approval."

### Step 2: Create PR

Apply **create-pr** skill with `--exec` flag:

- Read the approved change proposal
- Automatically execute branch creation -> code modification -> commit -> push -> PR creation

> **[Human Confirmation Point 2]**: "PR has been created. Final review and merge is at your discretion."

### Step 3: Suggest Next Actions

- "For PR review, use `/review`"
