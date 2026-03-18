# Legacy System Mastery Maturity Model

> **Version**: 1.1
> **Last Updated**: 2026-03-13
> **Author**: ashigaru-scribe

## Overview

This document is a maturity model for quantitatively evaluating the mastery of generic legacy systems. It evaluates 10 perspectives at 5 levels, supporting system visualization, improvement prioritization, and progress tracking.

## Assessment Model Description

Based on the CMMI (Capability Maturity Model Integration) 5-level model, it defines 10 perspectives addressing legacy system-specific challenges.

**Maturity Level Definitions**:
- Level 1: Initial (Ad hoc) - Lacking documentation and automation
- Level 2: Managed - Basic processes and measurement introduced
- Level 3: Defined - Standardized, systematic processes
- Level 4: Quantitatively Managed - Metrics-driven management
- Level 5: Optimizing - Continuous improvement through automation

## Evaluation Perspectives

### 1. State Management Health

**Definition**: Maturity of system state management methods, change tracking, and consistency maintenance

**Importance**:
- Global variables and scattered state changes reduce maintainability
- Applying appropriate state management patterns increases change impact predictability
- Log recording and inconsistency detection accelerate incident response

**Level Overview**:
- Level 1: Heavy use of global variables, scattered state changes, no logging
- Level 2: Partial improvements, basic log recording
- Level 3: State management pattern adoption begins, structured logging
- Level 4: High pattern adoption rate, automated inconsistency detection and reduction
- Level 5: Zero global variables, complete traceability, automatic repair

### 2. Testing Maturity

**Definition**: Maturity of test coverage, automation, and execution frequency (TMMi-compliant)

**Importance**:
- Tests are the safety net for refactoring and feature additions
- Automation enables continuous quality assurance
- Insufficient coverage risks latent bugs and regressions

**Level Overview**:
- Level 1: Coverage under 10%, manual testing focus
- Level 2: Partial automation, pre-release testing
- Level 3: Coverage 40-70%, daily execution
- Level 4: Coverage 70-90%, per-commit execution
- Level 5: Coverage 90%+, Mutation Testing introduced

### 3. Deployment Pipeline (CI/CD)

**Definition**: Deployment frequency, lead time, change failure rate, recovery time (DORA Metrics-compliant)

**Importance**:
- Deployment frequency is an indicator of business agility
- Shortened lead time improves responsiveness to market changes
- Change failure rate and recovery time are quality and reliability indicators

**Level Overview**:
- Level 1: Less than 6 deployments/year, lead time over 3 months, failure rate over 46%
- Level 2: Monthly deployment, lead time 1-3 months
- Level 3: Weekly deployment, lead time 1 week to 1 month
- Level 4: Daily deployment, lead time 1 day to 1 week
- Level 5: Multiple daily deployments, lead time under 1 day

### 4. Domain Knowledge Visibility

**Definition**: Maturity of business logic/specification documentation, currency, and knowledge silo elimination

**Importance**:
- Visualizing tacit knowledge eliminates individual dependency
- Making domain models explicit improves design quality
- Automatic document updating prevents obsolescence

**Level Overview**:
- Level 1: Under 10% documented, 100% expert dependency
- Level 2: Partial documentation, last updated 1-3 years ago
- Level 3: 40-70% documented, annual updates
- Level 4: 70-90% documented, semi-automatic updates
- Level 5: 90%+ documented, automatic updates, knowledge silos eliminated

### 5. Technology Stack Consistency (Technical Debt)

**Definition**: Technical debt, framework/library version dispersion, duplicate code (SQALE-compliant)

**Importance**:
- Technology stack dispersion increases learning and maintenance costs
- EOL (End of Life) libraries pose security risks
- Technical debt visualization and repayment planning accelerate improvement

**Level Overview**:
- Level 1: Debt Ratio over 50%, EOL usage rate over 30%
- Level 2: Debt Ratio 21-50%, EOL usage rate 10-30%
- Level 3: Debt Ratio 11-20%, EOL usage rate 0-10%
- Level 4: Debt Ratio 6-10%, EOL 0%, repayment rate exceeds accumulation rate
- Level 5: Debt Ratio under 5%, automatic refactoring

### 6. Observability

**Definition**: Implementation rate of logging, metrics, tracing and incident detection time (Observability Maturity Model-compliant)

**Importance**:
- Lack of observability prolongs incident response and makes root cause identification difficult
- Structured logging and distributed tracing support understanding of complex systems
- SLO (Service Level Objective) setting clarifies quality targets

**Level Overview**:
- Level 1: Under 10% logging, detection over 24 hours
- Level 2: 10-40% logging, detection 1-24 hours
- Level 3: 40-70% logging, metrics and tracing 30-70%, detection 15 min to 1 hour
- Level 4: 70-90% logging, detection under 15 min, SLO achievement rate over 95%
- Level 5: 90%+ logging, detection under 5 min, SLO achievement rate over 99%

### 7. Security and Compliance

**Definition**: Vulnerability scan frequency, critical vulnerability count, injection prevention, authentication implementation

**Importance**:
- Security vulnerabilities are business continuity risks
- Regular scanning and auto-patching enable early detection and response
- OWASP Top 10 countermeasures such as SQL injection prevention are essential

**Level Overview**:
- Level 1: No scanning, over 10 critical vulnerabilities
- Level 2: 1-4 annual scans, 5-10 critical vulnerabilities
- Level 3: Monthly scanning, 1-5 critical vulnerabilities
- Level 4: Daily scanning, 0-1 critical vulnerabilities
- Level 5: Per-commit scanning, 0 critical vulnerabilities, auto-fix rate over 80%

### 8. Dependency Health

**Definition**: Direct/indirect dependency count, average age, vulnerable dependencies, circular dependencies

**Importance**:
- Dependency bloat increases maintenance cost and security risk
- Old dependencies risk vulnerabilities and compatibility issues
- Circular dependencies indicate reduced design quality

**Level Overview**:
- Level 1: Over 100 direct dependencies, over 500 indirect, average age over 5 years
- Level 2: 50-100 direct, 200-500 indirect
- Level 3: 20-50 direct, 50-200 indirect, average age 1-3 years
- Level 4: 10-20 direct, auto-update rate 70-95%
- Level 5: Under 10 direct, auto-update rate over 95%, dependency reduction rate over 10%/year

### 9. Data Quality and Consistency

**Definition**: NULL value rate, duplication rate, foreign key constraints, validation implementation, inconsistency detection

**Importance**:
- Data quality degradation undermines business logic reliability
- Foreign key constraints and validation logic guarantee data consistency
- Automatic detection and correction maintain quality

**Level Overview**:
- Level 1: NULL rate over 30%, duplication over 10%, FK constraints under 30%
- Level 2: NULL rate 15-30%, FK constraints 30-50%
- Level 3: NULL rate 5-15%, FK constraints 50-80%, quality score 50-80%
- Level 4: NULL rate 1-5%, FK constraints 80-95%, auto-fix 50-80%
- Level 5: NULL rate under 1%, FK constraints over 95%, auto-fix over 80%

### 10. Code Distortion Detection Maturity

**Definition**: Capability to detect and manage distortions in code (insufficient validation, implicit dependencies, type comparison traps, etc.)

**Importance**:
- Legacy code distortions are breeding grounds for latent business risks
- Systematic detection (distortion patterns A/B/C) enables early problem discovery
- Cross-cutting risk views (L1/L2) identify problems invisible at the single-repository level
- Subject-First Rule eliminates ambiguous descriptions, preventing recognition gaps between teams

**Level Overview**:
- Level 1: No distortion detection, problems discovered incidentally
- Level 2: Partial detection during manual review, P1-P2 patterns only
- Level 3: Regular distortion analysis, P1-P4 patterns, Part A/B/C format reports
- Level 4: Automated detection via CI/static analysis, all P1-P6 patterns, L1+L2 cross-cutting management
- Level 5: Automated detection + preventive checks, custom patterns added, automated alerts

## Composite Assessment Method

### Scoring

Evaluate each perspective at Level 1-5, with total score (max 50 points) determining composite maturity.

**Composite maturity classification**:
- 0-10 points: **Critical** - Immediate improvement needed
- 11-20 points: **Low** - Broad improvement needed
- 21-30 points: **Moderate** - Partial improvement needed
- 31-40 points: **High** - Maintain continuous improvement
- 41-50 points: **Very High** - Optimization stage

### Weighted Assessment (Optional)

Weights (0.5-2.0) can be assigned to each perspective based on project characteristics.

**Example**: For EC systems
- Security: Weight 2.0
- Data quality: Weight 1.5
- Observability: Weight 1.5
- Others: Weight 1.0

Weighted composite score = Sum(perspective score x weight) / Sum(weights)

### Assessment Visualization

Radar chart visualization of 10 perspectives is recommended. Useful for identifying weaknesses and prioritizing improvements.

## Reference Frameworks

This assessment model references the following industry standard frameworks:

- **CMMI (Capability Maturity Model Integration)**: Basic maturity level structure
- **DORA Metrics**: Deployment perspective assessment criteria
- **SQALE/SonarQube**: Technical debt quantitative assessment
- **TMMi (Test Maturity Model integration)**: Testing maturity assessment
- **Observability Maturity Model**: Observability assessment criteria
- **OWASP Top 10**: Security perspective assessment items

## How to Conduct Assessments

### Recommended Frequency

- **Quarterly**: Regular trend tracking
- **Per milestone**: Improvement measure effectiveness measurement
- **Project start**: Baseline setting

### Assessment Process

1. **Data collection**: Measure quantitative indicators for each perspective (see `evaluation_criteria_matrix.md` for details)
2. **Level determination**: Determine level based on quantitative/qualitative criteria
3. **Review**: Review assessment results with stakeholders
4. **Improvement planning**: Prioritize and develop measures for low-level perspectives
5. **Trend analysis**: Compare with past assessments, visualize improvement effectiveness

### Using Assessment Results

- **Executive reporting**: Composite score, radar chart
- **Technical team**: Detailed analysis per perspective, improvement measure development
- **Stakeholders**: Quantitative tracking of improvement progress

## Related Documents

- **Detailed assessment criteria**: [evaluation_criteria_matrix.md](./evaluation_criteria_matrix.md) - 10 perspectives x 5 levels quantitative criteria
- **Usage**: [README.md](./README.md) - How to use assessment criteria and application examples

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2026-03-13 | Added 10th perspective "Code Distortion Detection Maturity." Updated composite score max to 50 points |
| 1.0 | 2026-03-01 | Initial version. Defined 9 perspectives x 5 levels generic assessment model |
