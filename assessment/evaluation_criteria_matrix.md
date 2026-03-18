# Legacy System Mastery Evaluation Criteria Matrix

> **Version**: 1.0
> **Last Updated**: 2026-03-01
> **Author**: ashigaru-scribe

## Overview

This document provides specific quantitative evaluation criteria for the 9-perspective x 5-level maturity model defined in `legacy_system_maturity_model.md`. It defines 3-5 measurable indicators for each perspective, enabling objective level determination.

---

## 1. State Management Health

**Definition**: Maturity of system state management methods, change tracking, and consistency maintenance

| Level | Global Variable Count | State Management Pattern Adoption Rate | State Change Log Rate | Inconsistency Detection Mechanism |
|-------|----------------------|---------------------------------------|---------------------|----------------------------------|
| **Level 1** | 100+ | 0-10% | 0-10% | None |
| **Level 2** | 50-100 | 10-30% | 10-40% | Manual check (weekly) |
| **Level 3** | 20-50 | 30-70% | 40-80% | Semi-automatic detection (daily batch) |
| **Level 4** | 5-20 | 70-95% | 80-95% | Automatic detection (real-time), inconsistency reduction over 80% |
| **Level 5** | 0 | 95-100% | 95-100% | Automatic detection + auto-repair, inconsistency rate under 0.1% |

**Measurement methods**:
- Global variable count: Static analysis tools (SonarQube, etc.)
- Pattern adoption rate: Code review, design documents
- Log rate: `logger.*`, `log->*` implementation count / state change point count
- Inconsistency detection: Monitoring tools, alert settings

---

## 2. Testing Maturity

**Definition**: Maturity of test coverage, automation, and execution frequency (TMMi-compliant)

| Level | Code Coverage | Test Automation Rate | Test Execution Frequency | Test Maintenance Cost | Mutation Score |
|-------|--------------|---------------------|------------------------|---------------------|---------------|
| **Level 1** | 0-10% | 0-20% | Pre-release only | Over 5 hours per 1% coverage | Not measured |
| **Level 2** | 10-40% | 20-50% | Pre-release + weekly | 3-5 hours per 1% | Not measured |
| **Level 3** | 40-70% | 50-80% | Daily (CI execution) | 1-3 hours per 1% | Not measured |
| **Level 4** | 70-90% | 80-95% | Per commit | 0.5-1 hour per 1% | Not measured |
| **Level 5** | 90-100% | 95-100% | Per commit + pre-production | Under 0.5 hours per 1% | Over 80% (Mutation Testing introduced) |

**Measurement methods**:
- Code coverage: PHPUnit, Jest, etc. coverage reports
- Automation rate: Automated test count / total test case count
- Execution frequency: CI/CD configuration files, execution logs
- Maintenance cost: Effort for test modification/addition / coverage increase rate
- Mutation Score: Infection (PHP), Stryker (JS), etc. reports

---

## 3. Deployment Pipeline (CI/CD)

**Definition**: Deployment frequency, lead time, change failure rate, recovery time (DORA Metrics-compliant)

| Level | Deployment Frequency | Lead Time (commit to production) | Change Failure Rate | Recovery Time (MTTR) |
|-------|---------------------|--------------------------------|--------------------|--------------------|
| **Level 1** | Less than 6/year | Over 3 months | Over 46% | Over 24 hours |
| **Level 2** | 1-4/month | 1-3 months | 31-45% | 1-24 hours |
| **Level 3** | 1-4/week | 1 week - 1 month | 16-30% | 15 min - 1 hour |
| **Level 4** | 1-4/day | 1 day - 1 week | 5-15% | Under 15 min |
| **Level 5** | 5+/day | Under 1 day (on-demand possible) | 0-5% | Under 5 min |

**Measurement methods**:
- Deployment frequency: Deployment logs, Git tag count
- Lead time: Git commit timestamp to production deployment timestamp
- Change failure rate: Rollback count / deployment count
- MTTR: Average of (incident detection timestamp - recovery timestamp)

---

## 4. Domain Knowledge Visibility

**Definition**: Maturity of business logic/specification documentation, currency, and knowledge silo elimination

| Level | Documentation Rate | Documentation Update Frequency | Last Document Update | Expert Dependency Rate | Auto-Generation Rate |
|-------|-------------------|-------------------------------|---------------------|-----------------------|--------------------|
| **Level 1** | 0-10% | None | Over 3 years ago | 80-100% | 0% |
| **Level 2** | 10-40% | 1-2/year | 1-3 years ago | 50-80% | 0-10% |
| **Level 3** | 40-70% | 3-6/year | 6 months - 1 year ago | 20-50% | 10-40% |
| **Level 4** | 70-90% | 1-3/month | 1-6 months ago | 5-20% | 40-70% |
| **Level 5** | 90-100% | Weekly+ | Within 1 month | 0-5% | 70-100% |

**Measurement methods**:
- Documentation rate: Documented business logic count / total business logic count
- Update frequency: Document update commit count / year
- Last update: Last modified date of document files
- Expert dependency rate: Expert inquiry frequency for specification confirmation (survey)
- Auto-generation rate: Auto-generated document count / total document count (Swagger, auto-generated ER diagrams, etc.)

---

## 5. Technology Stack Consistency (Technical Debt)

**Definition**: Technical debt, framework/library version dispersion, duplicate code (SQALE-compliant)

| Level | Debt Ratio | EOL Usage Rate | Duplicate Code Rate | Technology Stack Type Count | Debt Repayment Rate |
|-------|-----------|---------------|--------------------|--------------------------|--------------------|
| **Level 1** | Over 50% | Over 30% | Over 20% | 10+ types | Not measured |
| **Level 2** | 21-50% | 10-30% | 10-20% | 6-10 types | Below accumulation rate |
| **Level 3** | 11-20% | 0-10% | 5-10% | 3-6 types | Equal to accumulation rate |
| **Level 4** | 6-10% | 0% | 2-5% | 2-3 types | 1.5x accumulation rate |
| **Level 5** | 0-5% | 0% | 0-2% | 1-2 types | 2x+ accumulation rate |

**Measurement methods**:
- Debt Ratio: SonarQube `Technical Debt Ratio = (remediation cost / development cost) x 100`
- EOL usage rate: EOL library count / total library count (Composer, npm audit, etc.)
- Duplicate code rate: SonarQube `Duplicated Lines Density`
- Technology stack type count: Total of frameworks, languages, and DB types used
- Debt repayment rate: Monthly debt reduction / monthly debt accumulation

---

## 6. Observability

**Definition**: Implementation rate of logging, metrics, tracing, and incident detection time (Observability Maturity Model-compliant)

| Level | Logging Rate | Metrics Rate | Tracing Rate | Detection Time (MTTD) | SLO Achievement Rate |
|-------|-------------|-------------|-------------|---------------------|---------------------|
| **Level 1** | 0-10% | 0-10% | 0% | Over 24 hours | Not measured |
| **Level 2** | 10-40% | 10-30% | 0-10% | 1-24 hours | Not measured |
| **Level 3** | 40-70% | 30-70% | 30-70% | 15 min - 1 hour | 80-95% |
| **Level 4** | 70-90% | 70-90% | 70-90% | 5-15 min | 95-99% |
| **Level 5** | 90-100% | 90-100% | 90-100% | Under 5 min | Over 99% |

**Measurement methods**:
- Logging rate: Log recording point count / critical processing point count
- Metrics rate: Metrics collection point count / API and batch processing count
- Tracing rate: Tracing implementation count / microservice and external integration count
- MTTD: Average of (alert timestamp - actual incident timestamp)
- SLO achievement rate: SLO-met period / total evaluation period (SLO setting prerequisite for Level 3+)

---

## 7. Security and Compliance

**Definition**: Vulnerability scan frequency, critical vulnerability count, injection countermeasures, authentication implementation (OWASP Top 10-compliant)

| Level | Scan Frequency | Critical Vulnerabilities | OWASP Top 10 Coverage | SQL Injection Prevention Rate | Auto-Fix Rate |
|-------|---------------|------------------------|----------------------|------------------------------|--------------|
| **Level 1** | None | 10+ | 0-30% | 0-30% | 0% |
| **Level 2** | 1-4/year | 5-10 | 30-50% | 30-60% | 0-20% |
| **Level 3** | 1-4/month | 1-5 | 50-80% | 60-90% | 20-50% |
| **Level 4** | Daily | 0-1 | 80-95% | 90-100% | 50-80% |
| **Level 5** | Per commit | 0 | 95-100% | 100% | 80-100% |

**Measurement methods**:
- Scan frequency: CI/CD settings, SAST/DAST tool execution logs
- Critical vulnerabilities: Snyk, Trivy, OWASP ZAP reports
- OWASP Top 10 coverage: Checklist completion rate (A01-A10 countermeasure implementation count / 10)
- SQL injection prevention rate: Placeholder usage rate (detected via static analysis)
- Auto-fix rate: Auto-patch count / detected vulnerability count

---

## 8. Dependency Health

**Definition**: Direct/indirect dependency count, average age, vulnerable dependencies, circular dependencies

| Level | Direct Dependencies | Indirect Dependencies | Dependency Average Age | Vulnerable Dependency Rate | Auto-Update Rate |
|-------|--------------------|-----------------------|-----------------------|--------------------------|-----------------|
| **Level 1** | 100+ | 500+ | Over 5 years | Over 30% | 0% |
| **Level 2** | 50-100 | 200-500 | 3-5 years | 15-30% | 0-30% |
| **Level 3** | 20-50 | 50-200 | 1-3 years | 5-15% | 30-70% |
| **Level 4** | 10-20 | 20-50 | 6 months - 1 year | 1-5% | 70-95% |
| **Level 5** | Under 10 | Under 20 | Under 6 months | 0-1% | 95-100% |

**Measurement methods**:
- Direct dependencies: Dependencies count in `composer.json`, `package.json`
- Indirect dependencies: Total package count in `composer.lock`, `package-lock.json`
- Average age: Average elapsed days since last update of each dependency
- Vulnerable dependency rate: Vulnerable dependency count / total dependency count (npm audit, composer audit)
- Auto-update rate: Dependabot auto-merge count / total update PR count

---

## 9. Data Quality and Consistency

**Definition**: NULL value rate, duplication rate, foreign key constraints, validation implementation, inconsistency detection

| Level | NULL Value Rate | Duplication Rate | FK Constraint Rate | Data Validation Rate | Auto-Fix Rate |
|-------|----------------|-----------------|-------------------|---------------------|--------------|
| **Level 1** | Over 30% | Over 10% | 0-30% | 0-30% | 0% |
| **Level 2** | 15-30% | 5-10% | 30-50% | 30-50% | 0-30% |
| **Level 3** | 5-15% | 2-5% | 50-80% | 50-80% | 30-50% |
| **Level 4** | 1-5% | 0.5-2% | 80-95% | 80-95% | 50-80% |
| **Level 5** | Under 1% | Under 0.5% | 95-100% | 95-100% | 80-100% |

**Measurement methods**:
- NULL value rate: NULL value column count / total column count (major tables)
- Duplication rate: Duplicate record count / total record count
- FK constraint rate: FK constraint column count / foreign reference column count
- Data validation rate: Validation implementation count / data input point count
- Auto-fix rate: Auto-cleansing/normalization fix count / detected inconsistency count

---

## Composite Score Calculation

### Basic Score

Evaluate each perspective at Level 1-5 and sum (max 45 points).

**Composite Score = Sum(each perspective's level)**

### Weighted Score (Optional)

Weighting possible based on project characteristics.

**Weighted Score = Sum(perspective level x weight) / Sum(weights)**

Example: EC system weight settings
- Security: 2.0
- Data quality: 1.5
- Observability: 1.5
- Others: 1.0

---

## Recommended Measurement Tools

| Perspective | Recommended Tools |
|------------|-----------------|
| State management | SonarQube, static analysis tools |
| Testing | PHPUnit, Jest, Infection (Mutation Testing) |
| CI/CD | GitHub Actions, GitLab CI, Datadog |
| Domain knowledge | Confluence, Notion, Git history analysis |
| Technical debt | SonarQube, CodeClimate, SQALE |
| Observability | Datadog, New Relic, OpenTelemetry |
| Security | Snyk, Trivy, OWASP ZAP |
| Dependencies | Dependabot, npm audit, composer audit |
| Data quality | Great Expectations, dbt tests, SQL analysis |

---

## 10. Code Distortion Detection Maturity

**Definition**: Maturity of capability to detect and manage code distortions (insufficient validation, implicit dependencies, type comparison traps, etc.)

| Level | Detection Method | Problem Pattern (P1-P6) Coverage | Subject-First Rule Adoption | Cross-Cutting Risk Management | Report Quality |
|-------|-----------------|--------------------------------|---------------------------|------------------------------|---------------|
| **Level 1** | None (incidental discovery) | 0% | 0% | None | None |
| **Level 2** | Partial detection during manual review | 1-2 patterns | 0-20% | None | Unstructured notes |
| **Level 3** | Regular distortion analysis | 3-4 patterns | 20-60% | L1 (single repo) only | Part A/B/C format |
| **Level 4** | Automated via CI/static analysis | 5-6 patterns | 60-90% | L1 + L2 (cross-cutting) | Part A/B/C + remediation ROI |
| **Level 5** | Automated + preventive checks | 6 patterns + custom | 90-100% | L1 + L2 + automated alerts | Part A/B/C + remediation tracking |

**Measurement methods**:
- Detection method: Presence and frequency of analysis processes
- Pattern coverage: Number of patterns targeted for detection out of P1-P6
- Subject-First Rule: Percentage of distortion reports that explicitly state "whose/what" as subject
- Cross-cutting risk management: L1 (per component) / L2 (cross-cutting risk view) implementation status
- Report quality: Degree of structural organization in output format

### Distortion Patterns (A/B/C) Severity Assessment Criteria

| Pattern | Severity Criteria |
|---------|-----------------|
| **A: Invalid value passes through** | High: Affects money/personal info / Medium: Affects business data / Low: Display only |
| **B: Stops midway** | High: Transaction inconsistency / Medium: Downstream batch failure / Low: Log error only |
| **C: No check exists** | High: Affects security/payments / Medium: Possible business rule violation / Low: Edge cases only |

### Problem Pattern (P1-P6) Remediation ROI Assessment Criteria

| ROI | Definition | Criteria |
|-----|-----------|---------|
| **Highest** | 1 fix resolves multiple high-severity risks | Fix size: small & resolved risks: high x 2+ |
| **High** | 1 fix resolves a high-severity risk | Fix size: small-medium & resolved risks: high x 1 |
| **Medium** | 1 fix resolves a medium-severity risk | Fix size: medium & resolved risks: medium x 1+ |
| **Low** | Large fix size or low-severity only | Fix size: large or resolved risks: low only |

---

## Reference Standards

This matrix references the following industry standards:

- **DORA Metrics** (DevOps Research and Assessment): CI/CD evaluation criteria
- **SQALE** (Software Quality Assessment based on Lifecycle Expectations): Technical debt evaluation
- **TMMi** (Test Maturity Model integration): Testing maturity evaluation
- **Observability Maturity Model**: Observability evaluation
- **OWASP Top 10**: Security evaluation
- **CMMI**: Maturity level definitions

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2026-03-13 | Added 10th perspective "Code Distortion Detection Maturity." Defined evaluation criteria for distortion patterns A/B/C and problem patterns P1-P6 |
| 1.0 | 2026-03-01 | Initial version. Defined 9-perspective x 5-level quantitative evaluation criteria matrix |
