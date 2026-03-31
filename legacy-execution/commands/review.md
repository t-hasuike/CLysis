---
description: Review Pull Request code quality and business logic alignment. Execute the project-guide -> review-code skill chain.
argument-hint: "<PR number> <repository name>"
---

# /review -- PR Review Flow

## Overview

A workflow for reviewing PR code quality and business logic alignment.

## Workflow

### Step 1: Prepare Context

Apply **project-guide** skill:

- Identify domain knowledge and project information needed for PR review
- Pre-read related domain knowledge from knowledge/domain/

$ARGUMENTS

> **Checkpoint**: "Review preparation complete. Ready to proceed with the review?"

### Step 2: Code Review

Apply **review-code** skill:

- Evaluate code quality (readability, maintainability, security)
- Verify business logic alignment
- Make judgment: Approve / Request Changes / Comment

### Step 3: Suggest Next Actions

- "If changes are needed, use `/implement` to create a change proposal"
