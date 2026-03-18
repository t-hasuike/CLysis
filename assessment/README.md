# Legacy System Mastery Assessment Criteria - README

> **Version**: 1.2
> **Last Updated**: 2026-03-13
> **Author**: ashigaru-scribe

## Overview

This directory provides **generic assessment criteria for quantitatively evaluating legacy system mastery**. It measures maturity across 10 perspectives at 5 levels, supporting system visualization, improvement prioritization, and progress tracking.

**Important**: These are generic assessment criteria, not specialized for any particular system (e.g., internal business systems). Customize according to project characteristics when applying.

---

## File Structure

| File | Content | Purpose |
|------|---------|---------|
| **legacy_system_maturity_model.md** | 9-perspective x 5-level maturity model definition | Overall assessment model, importance of each perspective, level overview |
| **evaluation_criteria_matrix.md** | Quantitative evaluation criteria matrix | Specific numerical criteria and judgment methods for each perspective x level |
| **legacy_document_quality.md** | Investigation document quality assessment criteria | Evaluating actionability of leader team output documents |
| **README.md** (this file) | Usage and application procedures | How to conduct assessments, target audience, references |

---

## Two Types of Assessment Criteria

This directory contains **2 types of assessment criteria** with different evaluation targets and usage timing:

| Assessment Criteria | Evaluation Target | Usage Timing | Users |
|--------------------|-------------------|-------------|-------|
| **legacy_system_maturity_model.md** + **evaluation_criteria_matrix.md** | **Legacy system maturity** | System improvement planning, improvement progress tracking | Management, development team |
| **legacy_document_quality.md** | **Investigation document quality** | Document completion, pre-implementation review | Leader, user (human) |

### System Maturity Assessment (legacy_system_maturity_model.md)

**Evaluation target**: The legacy system itself (test coverage, technical debt, security, etc.)

**Purpose**: Measure overall system health and determine improvement priorities

**Usage examples**:
- "This system's test maturity is Level 2, technical debt is Level 1. Prioritize debt repayment first"
- "Quarterly evaluation shows composite score improved from 19 to 24 points. Confirming continuous improvement results"

### Document Quality Assessment (legacy_document_quality.md)

**Evaluation target**: Investigation documents output by the leader team

**Purpose**: Determine whether documents meet the quality needed to "proceed to the next step (implementation/planning)"

**Usage examples**:
- "Investigation document is Level 4. Impact scope, Phase breakdown, and risks are documented. Ready to start implementation"
- "Level 2 (basic completion) but blocker B004 (risk organization) prevents implementation start. Additional investigation needed"

### Decision Flow for Which to Use

```
Question: What do you want to evaluate?
  |
  |- Want to plan system improvements
  |   |-> Use legacy_system_maturity_model.md + evaluation_criteria_matrix.md
  |
  |- Want to review if investigation documents are ready for implementation
      |-> Use legacy_document_quality.md
```

---

## Assessment Model Overview

### 10 Evaluation Perspectives

| Perspective | Reference Framework | Importance |
|------------|-------------------|-----------|
| 1. State Management Health | - | Maintainability, change impact predictability |
| 2. Testing Maturity | TMMi | Quality assurance, refactoring safety |
| 3. CI/CD Pipeline | DORA Metrics | Business agility, deployment risk reduction |
| 4. Domain Knowledge Visibility | - | Eliminating knowledge silos, design quality improvement |
| 5. Technology Stack Consistency | SQALE | Maintenance cost reduction, security risk reduction |
| 6. Observability | Observability MM | Faster incident response, system understanding |
| 7. Security | OWASP Top 10 | Vulnerability risk reduction, compliance |
| 8. Dependency Health | - | Maintenance cost reduction, vulnerability risk reduction |
| 9. Data Quality | - | Business logic reliability, consistency assurance |
| 10. Code Distortion Detection Maturity | Distortion Analysis Framework | Distortion detection and management capability maturity |

### 5-Level Maturity Scale

| Level | Name | Description | Characteristics |
|-------|------|-------------|----------------|
| **Level 1** | Initial (Ad hoc) | Lacking documentation and automation | Ad-hoc, individual-dependent |
| **Level 2** | Managed | Basic processes and measurement introduced | Partial improvement started |
| **Level 3** | Defined | Standardized, systematic processes | Organizational management |
| **Level 4** | Quantitatively Managed | Metrics-driven management | Data-based improvement |
| **Level 5** | Optimizing | Continuous improvement through automation | Autonomous improvement |

### Composite Maturity Classification

Determine composite maturity by total score (max 50 points):

| Score Range | Composite Maturity | Status |
|------------|-------------------|--------|
| 0-10 points | **Critical** | Immediate improvement needed |
| 11-20 points | **Low** | Broad improvement needed |
| 21-30 points | **Moderate** | Partial improvement needed |
| 31-40 points | **High** | Maintain continuous improvement |
| 41-50 points | **Very High** | Optimization stage |

---

## How to Conduct Assessments

### Step 1: Data Collection

Collect quantitative indicators for each perspective as described in `evaluation_criteria_matrix.md`.

**Collection methods**:
- **Automatic collection**: Tool reports from SonarQube, npm audit, Datadog, etc.
- **Manual collection**: Code review, document investigation, interviews
- **Calculation**: Git history analysis, DB analysis queries

**Collection timing**: Start 1-2 weeks before assessment

### Step 2: Level Determination

For each perspective, compare collected data against criteria in `evaluation_criteria_matrix.md` to determine Level 1-5.

**Determination rules**:
- If multiple indicators exist, adopt the **lowest level** (conservative assessment)
- For boundary values, review and discuss with stakeholders
- Record determination rationale (ensure traceability)

### Step 3: Review

Review assessment results with stakeholders (development team, managers, stakeholders).

**Review points**:
- Is the determination appropriate? (data reliability, criteria interpretation)
- Need for project-specific corrections?
- Need for weighting?

### Step 4: Improvement Planning

Develop improvement measures for low-level perspectives and determine priorities.

**Prioritization perspectives**:
- Business impact (revenue, customer satisfaction impact)
- Feasibility (effort, resources, technical difficulty)
- Ripple effect (positive impact on other perspectives)
- Weighting (importance based on project characteristics)

**Improvement measure examples**:
- Level 1->2: Basic tool introduction, process definition
- Level 2->3: Standardization, automation expansion
- Level 3->4: Metrics-driven management system construction
- Level 4->5: Advanced automation and autonomy

### Step 5: Trend Analysis

Compare with past assessment results to visualize improvement effectiveness.

**Analysis methods**:
- **Time series graph**: Composite score and per-perspective score trends
- **Radar chart**: Comparison with previous assessment
- **Improvement velocity**: Time required for level-up

---

## Target Audience

### Development Team
- **Usage**: Detailed technical improvement planning and execution
- **Resources**: Quantitative criteria and measurement tools in `evaluation_criteria_matrix.md`

### Management
- **Usage**: Improvement priority decisions, resource allocation
- **Resources**: Composite assessment and radar chart in `legacy_system_maturity_model.md`

### Stakeholders
- **Usage**: Improvement progress tracking, investment decisions
- **Resources**: Composite score, time series graphs

---

## Project-Specific Customization

These assessment criteria are generic; customization is recommended based on project characteristics.

### Customization Examples

**For EC systems**:
- Security weight: 2.0 (personal information, payment data protection)
- Data quality weight: 1.5 (inventory, order consistency)
- Observability weight: 1.5 (preventing sales opportunity loss)

**For internal business systems**:
- Domain knowledge visibility weight: 2.0 (importance of eliminating knowledge silos)
- CI/CD weight: 0.8 (lower importance of deployment frequency)

**For SaaS products**:
- CI/CD weight: 2.0 (agility as business advantage)
- Testing maturity weight: 1.8 (quality as brand value)

### Threshold Adjustment

Adjust threshold values for each level based on current project state.

**Example**: For already high-maturity projects, raise Level 3 criteria
- Test coverage Level 3: 40-70% -> 60-80%

---

## Recommended Assessment Frequency

| Frequency | Purpose | Application Timing |
|-----------|---------|-------------------|
| **Quarterly** | Regular trend tracking | Continuous improvement phase |
| **Per milestone** | Improvement measure effectiveness measurement | Refactoring completion |
| **Project start** | Baseline setting | Legacy system mastery initiation |

---

## How to Use Assessment Results

### Executive Report
- **Content**: Composite score, radar chart, improvement trends
- **Frequency**: Quarterly
- **Purpose**: Investment decisions, resource allocation basis

### Technical Team Report
- **Content**: Detailed scores per perspective, determination rationale, improvement measure proposals
- **Frequency**: Per assessment
- **Purpose**: Specific technical improvement planning and execution

### Stakeholder Dashboard
- **Content**: Composite score time series, key perspective progress
- **Frequency**: Real-time updates (tool integration)
- **Purpose**: Transparency, improvement progress visibility

---

## Reference Frameworks

These assessment criteria reference the following industry standard frameworks:

| Framework | Applied Perspective | Description |
|-----------|-------------------|-------------|
| **CMMI** (Capability Maturity Model Integration) | Overall structure | Basic structure of 5-level maturity model |
| **DORA Metrics** | CI/CD | DevOps Research and Assessment deployment evaluation criteria |
| **SQALE** | Technical debt | Software Quality Assessment based on Lifecycle Expectations |
| **TMMi** | Testing | Test Maturity Model integration |
| **Observability Maturity Model** | Observability | Log, metrics, tracing maturity assessment |
| **OWASP Top 10** | Security | Top 10 web application security risks |

---

## Notes

### Regarding Generality
These assessment criteria are a generic framework, not specialized for any particular system (e.g., internal business systems). Consider the following when applying:

- Weighting based on project characteristics
- Threshold adjustments (according to current state)
- Adding/removing perspectives (based on business requirements)

### Data Reliability
Data accuracy is critical as a prerequisite for quantitative assessment. Be aware of:

- Tool configuration errors/bugs causing measurement errors
- Subjectivity in manually collected data
- Consistency of data collection timing

### Continuous Improvement
Assessments should be operated as a continuous improvement cycle, not a "one-time" event:

1. Conduct assessment
2. Develop improvement measures
3. Execute measures
4. Re-assess (measure effectiveness)
5. Review criteria (as needed)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2 | 2026-03-13 | Added 10th perspective "Code Distortion Detection Maturity." Updated composite score max to 50 points |
| 1.1 | 2026-03-02 | Added legacy_document_quality.md. Explained usage of 2 types of assessment criteria |
| 1.0 | 2026-03-01 | Initial version. Defined directory overview and assessment procedures |
