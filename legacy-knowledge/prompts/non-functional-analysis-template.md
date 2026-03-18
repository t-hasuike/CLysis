# Non-Functional Requirements Investigation Procedure

## Overview
This procedure is for automatically extracting non-functional requirements (As-Is) from GitHub source code for rebuild projects.

## Prerequisites
- Serena is running
- Target repositories exist at: `<REPOSITORY_ROOT_PATH>`
  - **<REPO_NAME_1>**: <description>
  - **<REPO_NAME_2>**: <description>
  - **<REPO_NAME_3>**: <description>
- Access to GitHub (via MCP tools)

**Note**: Investigate all repositories. If narrowing to specific repositories, state this explicitly.

---

## Execution Steps

### Step 1: Static Code Analysis with Serena

Investigate the following non-functional items with Serena.

#### 1.1. Availability

**Investigation Items**:
| Item | Investigation Target | Investigation Method |
|------|---------------------|---------------------|
| External integration retry | <External integration service name> | Search for retry logic under `Services/<integration>/` |
| Timeout settings | HTTP communication, DB connections | Check `config/` and HTTP client settings |
| Error handling | Exception handling patterns | Pattern search for `try-catch` block usage |

**Serena execution example**:
```
search_for_pattern("retry|timeout", relative_path="app/Services/<integration>")
find_symbol("<HTTP client name>", include_body=true)
```

#### 1.2. Performance

**Investigation Items**:
| Item | Investigation Target | Investigation Method |
|------|---------------------|---------------------|
| DB indexes | Queries including soft-delete | Search for delete flag conditions in <ORM/query builder> |
| Cache strategy | Cache usage locations | Search for cache API usage |
| Query optimization | N+1 problem presence | Check Eager loading usage |

**Serena execution example**:
```
search_for_pattern("<delete flag condition pattern>", relative_path="app")
search_for_pattern("<cache API>", relative_path="app")
```

#### 1.3. Security

**Investigation Items**:
| Item | Investigation Target | Investigation Method |
|------|---------------------|---------------------|
| Authentication method | Middleware, auth settings | `config/auth.*` and `app/<Middleware Path>` |
| Authorization control | Access control implementation | Check `app/<Authorization Path>` |
| Input validation | Validation implementation | Check `app/<Validation Path>` |
| SQL Injection prevention | Query builder usage | Search for raw SQL query usage |

**Serena execution example**:
```
find_symbol("<Auth Middleware name>", relative_path="app/<Middleware Path>")
search_for_pattern("<raw SQL execution pattern>", relative_path="app")
```

#### 1.4. Operability

**Investigation Items**:
| Item | Investigation Target | Investigation Method |
|------|---------------------|---------------------|
| Log output | Log level usage | Search for log API usage |
| Batch schedule | Scheduler settings | Check scheduler configuration files |
| Monitoring and alerts | External monitoring tool integration | Check monitoring tool settings |

**Serena execution example**:
```
search_for_pattern("<log API pattern>", relative_path="app")
find_symbol("schedule", relative_path="<scheduler config path>", include_body=true)
```

---

### Step 2: Manual Cloud Environment Verification (Reference)

**Note**: This step cannot be executed by Claude. Reference commands for manual execution.

#### 2.1. Database
```bash
# Example: AWS RDS
aws rds describe-db-instances --region <REGION> \
  --query 'DBInstances[*].[DBInstanceIdentifier,DBInstanceClass,MultiAZ,StorageType]'
```

#### 2.2. Compute Resources
```bash
# Example: Serverless functions
<CLI command to list functions> --region <REGION>

# Example: Container services
<CLI command to list clusters> --region <REGION>
```

#### 2.3. Storage
```bash
# Example: Object storage
<CLI command to get storage policy> --bucket <BUCKET_NAME>

# Lifecycle rules
<CLI command to get lifecycle config> --bucket <BUCKET_NAME>
```

#### 2.4. Cache
```bash
# Example: Managed cache service
<CLI command to describe cache clusters> --region <REGION>
```

---

### Step 3: Background Processing Feature List Extraction

**Purpose**: Identify batch processing and time-triggered processing that is not visible from the UI, and list them in a developer-friendly format.

#### 3.1. Types of Processing to Investigate

The following background processing types are investigation targets:

##### A. Time-Triggered (UI invisible)

| Processing Type | Description | Investigation Location |
|----------------|-------------|----------------------|
| **Scheduled batch** | Processing executed periodically by scheduler | Each repository's `<scheduler config path>` |
| **CLI commands** | Commands executed manually or from scheduler | Each repository's `<command implementation path>` |
| **Async jobs** | Jobs executed asynchronously | Each repository's `<job implementation path>` |
| **Event listeners** | Processing executed on specific event firing | Each repository's `<listener implementation path>` |

**Target repositories**: <REPO_NAME_1>, <REPO_NAME_2>, <REPO_NAME_3>, ...

##### B. On-Demand Execution (User/External Trigger)

Investigate features triggered by user actions or external system requests that have **complex backend processing**.

**Execution path types**:

| Execution Path | Description | URL Example | Feature ID Range |
|---------------|-------------|------------|-----------------|
| **<Path A>** | <Description A> | <URL_PATTERN_A> | 101-149 |
| **<Path B>** | <Description B> | <URL_PATTERN_B> | 151-199 |
| **<Path C>** | <Description C> | <URL_PATTERN_C> | 201-299 |

**Processing types**:

| Processing Type | Description | Investigation Location | Investigation Focus |
|----------------|-------------|----------------------|-------------------|
| **File generation/conversion** | PDF generation, CSV output, image conversion, etc. | Controller -> Service -> External library | Storage, temp files, conversion library |
| **Data export** | Large volume CSV/Excel output | Controller -> UseCase -> Repository | Memory limits, streaming output, compression |
| **Bulk operations** | Bulk update/delete of multiple records | Controller -> Service -> Transaction | Lock control, rollback, progress management |
| **External storage operations** | File operations on cloud storage | Service -> SDK | Bucket name, permissions, region, encryption |
| **External system integration** | Data transmission/API calls to external systems | Service -> HTTP Client | API spec, auth method, retry control |
| **Data import** | Data intake from CSV/Excel | Controller -> UseCase -> Validation | Validation rules, error handling, rollback |
| **Error handling/recovery** | Recovery processing on error, compensation transactions | Service -> Exception Handler -> Recovery | Rollback strategy, retry control, error notification |
| **Multi-external dependency processing** | Processing dependent on multiple external systems | Service -> Multiple external APIs | Dependencies, fallback, timeout |
| **Data consistency check/repair** | Data inconsistency detection/repair processing | Controller -> Validation Service -> Repair | Consistency rules, repair logic, execution permissions |
| **Performance-critical processing** | Response time-critical processing, SLA targets | Controller -> Cache -> Optimized Query | Cache strategy, query optimization, monitoring |

**Target repositories**: <REPO_NAME_1>, <REPO_NAME_2>, <REPO_NAME_3>, ...

**Investigation notes**:
- Button labels alone often don't reveal processing content -- verify the implementation
- Example: "<Button A>" -> Actually <specific processing content A>
- Example: "<Button B>" -> <specific processing content B>
- Document backend processing specifically (not "<abstract name>" but "<specific processing flow>")
- **Number feature IDs by execution path** and add "Execution Path" column to CSV
- **Investigate all repositories** (explicitly state if narrowing to specific repositories)

#### 3.2. Feature Naming Convention

Feature names should be described at a **granularity that developers can recognize and develop against**.

**Good examples**:
- <External System A> - <Processing Content A>
- <External System B> - <Processing Content B>
- <Feature C> - <Processing Content C>

**Bad examples** (too granular):
- Execute <ClassName>
- Run <ConfigFileName>

**Bad examples** (too broad):
- <Major Category> processing
- Batch processing

#### 3.3. Investigation Method

##### A. Time-Triggered Investigation

```
# Scheduled batch investigation
find_symbol("schedule", relative_path="<scheduler config path>", include_body=true)

# CLI command investigation
search_for_pattern("<command definition pattern>", relative_path="<command implementation path>")

# Async job investigation
search_for_pattern("<job definition pattern>", relative_path="<job implementation path>")
```

##### B. User-Triggered Investigation

**Investigation procedure**:

1. **Identify Controller methods**
   ```
   # File generation/download
   search_for_pattern("<file generation pattern>", relative_path="<Controller Path>")

   # Storage operations
   search_for_pattern("<storage operation pattern>", relative_path="<Service Path>")

   # Bulk operations
   search_for_pattern("<bulk operation pattern>", relative_path="<Controller Path>")

   # Error handling/recovery
   search_for_pattern("<error handling pattern>", relative_path="<Service Path>")

   # Multi-external dependency processing
   search_for_pattern("<external API call pattern>", relative_path="<Service Path>")

   # Data consistency check/repair
   search_for_pattern("<consistency check pattern>", relative_path="<Controller Path>")

   # Performance-critical
   search_for_pattern("<cache usage pattern>", relative_path="<Controller Path>")
   search_for_pattern("<query optimization pattern>", relative_path="<Repository Path>")
   ```

2. **Verify UseCase/Service implementation**
   - Identify UseCase/Service classes called from Controllers
   - Trace actual processing flow (DB operations -> external API calls -> file storage, etc.)
   - Check for external system integration

3. **Detail the processing content**
   - Not just "<abstract process name>" but at this granularity:
     - Library usage (<library name>, etc.)
     - Upload to storage (bucket name, path)
     - Save metadata to DB (table, column)
     - URL generation method (signed URL, public URL, etc.)

4. **Record implementation file paths**
   - Controller: `<Controller implementation path example>`
   - UseCase: `<UseCase implementation path example>`
   - Service: `<Service implementation path example>`

**Investigation example**:

```markdown
Feature name: <Feature Name>
Trigger: <Trigger content>
Processing flow:
1. <Step 1>
2. <Step 2> (<Details>)
3. <Step 3> (<Details>)
4. <Step 4> (<Details>)
5. <Step 5> (<Details>)
6. <Step 6>
```

#### 3.4. CSV Output Format

Output in the following CSV format. Designed for final expansion in a spreadsheet.

**CSV column definitions**:

| Column Name | Description | Example (Time-triggered) | Example (On-demand) |
|------------|-------------|--------------------------|---------------------|
| Feature ID | Sequential number by execution path | 1, 2, 3... | 101 (<Path A>), 151 (<Path B>), 201 (<Path C>) |
| Execution Path | Execution path type (on-demand only) | (blank) | <Path A> / <Path B> / <Path C> |
| Feature Name | Human-recognizable feature name | <External System A> - <Processing A> | <Feature B> - <Processing B> |
| Feature Category | Processing type | Scheduled batch / CLI command / Async job / Event listener | File generation/conversion / Data export / Bulk operation / External storage operation |
| Description | Detailed feature description | <Detail A> | <Detail B> |
| Execution Trigger | When it executes | cron expression: `<cron>` / daily / hourly / on event | <Screen name> "<Button>" button click / External system API call |
| Execution Frequency | Human-readable frequency | Daily at <time> / Hourly at <minute> / Monthly on <day> at <time> / Real-time | On user action / External system trigger |
| Trigger Screen/URL | Which screen/URL triggers it (on-demand only) | (blank) | <Screen name> / <URL example> |
| HTTP Method | Request method (on-demand only) | (blank) | POST / GET / PUT / DELETE |
| Implementation File Path | Implementation file (including repo name) | <REPO_NAME>/<file path> | <REPO_NAME>/<file path> |
| Related Command/Class | Command or class name | <Command name> / <Class name> | <ClassName>::<MethodName> / <UseCase name> |
| Processing Flow | Specific processing flow (important for on-demand) | (brief) | 1. <Step 1> 2. <Step 2> 3. <Step 3> ... |
| External System Integration | External system integration target | <External System A> / <External System B> / <Cloud Service> | <Cloud Service> / <Library> |
| Notes | Supplementary information | Production environment only / <Specific period> only | Memory limit <value> / Expiration <period> / External system API call |

**CSV output examples**:

##### A. Time-Triggered
```csv
Feature ID,Feature Name,Feature Category,Description,Execution Trigger,Execution Frequency,Trigger Screen/URL,HTTP Method,Implementation File Path,Related Command/Class,Processing Flow,External System Integration,Notes
1,<External System A> - <Processing A>,Scheduled batch,<Detail>,hourlyAt(55),Every hour at :55,,,<REPO_NAME>/<file path>,<Command>,<Flow overview>,<External System A>,
2,<Feature B> - <Processing B>,Scheduled batch,<Detail>,dailyAt('02:30'),Daily at 02:30,,,<REPO_NAME>/<file path>,<Command>,<Flow overview>,,
```

##### B. On-Demand Execution (User/External Trigger)
```csv
Feature ID,Execution Path,Feature Name,Feature Category,Description,Execution Trigger,Execution Frequency,Trigger Screen/URL,HTTP Method,Implementation File Path,Related Command/Class,Processing Flow,External System Integration,Notes
101,<Path A>,<Feature A>,File generation/conversion,<Detail>,<Screen> "<Button>" button,On user action,<URL>,POST,<REPO_NAME>/<file path>,<ClassName>::<MethodName> / <UseCase>,<Detailed flow>,<Library>,
153,<Path B>,<Feature B>,File generation/conversion,<Detail>,<Screen> "<Button>" button,On user action,<URL>,POST,<REPO_NAME>/<file path>,<ClassName>::<MethodName>,<Detailed flow>,<Cloud Service> / <Library>,<Restriction>
201,<Path C>,<Feature C>,Data import,<Detail>,Request from <external system>,External system trigger,<URL>,POST,<REPO_NAME>/<file path>,<UseCase>,<Detailed flow>,<External System>,External system integration - <Status> on error
```

#### 3.5. Execution Procedure

##### A. Time-Triggered Investigation Procedure

**Target repositories**: <REPO_NAME_1>, <REPO_NAME_2>, <REPO_NAME_3>, ...

1. Read `<scheduler config path>` in each repository
2. Extract from each schedule definition:
   - Command or job being executed
   - Execution trigger (cron expression, daily, hourly, etc.)
   - timezone setting
   - when conditions (specific months only, etc.)
3. Identify command classes and determine feature names from processing content
4. Check for external system integration (under `<integration path>`, etc.)
5. Output in CSV format (Feature ID: starting from 1)
6. **Important**: Clearly state features per repository and include repository name in implementation file paths

##### B. User-Triggered Investigation Procedure

**Target repositories**: <REPO_NAME_1>, <REPO_NAME_2>, <REPO_NAME_3>, ...

1. **Search Controllers in each repository to identify heavy processing**
   - Search for file generation/download processing
   - Search for storage operations
   - Search for bulk operations

2. **Identify URLs and HTTP methods from route definitions**
   - Check `<route definition file path>` in each repository
   - Verify Controller -> method mapping

3. **Trace processing flow**
   - Controller -> UseCase/Service -> Repository -> External system
   - Record specifically what each step does
   - Focus particularly on:
     - File generation (<format>, <format>, <format>)
     - Storage operations (bucket name, path, permissions)
     - DB operations (transactions, locks)
     - External API calls

4. **Record screen information**
   - Which screen triggers it (screen name, URL)
   - Which repository implements it
   - Button labels (e.g., "<Button A>", "<Button B>")

5. **Output in CSV format (Feature ID: starting from 101)**
   - Feature IDs start from 101 to distinguish from time-triggered
   - Always include Trigger Screen/URL, HTTP Method, Processing Flow

---

### Step 4: Non-Functional Requirements Investigation Results Output

Output investigation results in the following table format.

#### 4.1. Availability

| Item | Current Implementation/Setting (As-Is) | Evidence (File:Line) | Notes |
|------|---------------------------------------|---------------------|-------|
| Continuity | <Retry implementation> | <file path>:<line> | <Library/Framework> |
| Timeout | HTTP <sec>s, DB <sec>s | <file path>:<line> | |
| Failure detection | <Monitoring tool> integration, <threshold> | <file path>:<line> | |

#### 4.2. Performance

| Item | Current Implementation/Setting (As-Is) | Evidence (File:Line) | Notes |
|------|---------------------------------------|---------------------|-------|
| DB indexes | <Status> | <file path>:<line> | <Issues> |
| Cache strategy | <Cached content> for <duration> | <file path>:<line> | <Cache system> |
| Query optimization | <Optimization technique> used | <file path>:<line> | <Specific technique> |

#### 4.3. Security

| Item | Current Implementation/Setting (As-Is) | Evidence (File:Line) | Notes |
|------|---------------------------------------|---------------------|-------|
| Authentication | <Auth method> | <file path>:<line> | <Purpose> |
| Authorization | <Authorization status> | <file path>:<line> | |
| Input validation | <Validation coverage> | <file path> | <Exceptions> |
| SQL Injection prevention | <count> raw SQL usage locations | <file path>:<line> | <API used> |

#### 4.4. Operability

| Item | Current Implementation/Setting (As-Is) | Evidence (File:Line) | Notes |
|------|---------------------------------------|---------------------|-------|
| Log levels | <Log level usage status> | Generally implemented | <Statistics> |
| Batch schedule | <count> types of batches at <frequency> | <file path>:<line> | <Batch content> |
| Monitoring/alerts | <Monitoring Tool A> + <Monitoring Tool B> | <file path>:<line> | <Notification target> |

---

## Investigation Notes

### 1. Accurate File Path Recording
- Record including line numbers (e.g., `<file path>:<line>`)
- Mark "needs verification" for settings files not under version control

### 2. Dynamic Configuration Values
- Mark values set by environment variables as "environment-dependent"
- Consider potential differences between production and development environments

### 3. Cloud Environment Information Handling
- Mark "pending verification" for cloud info requiring manual verification
- State when unable to verify due to insufficient permissions

### 4. Priority Determination
- High: Directly impacts security and availability
- Medium: Impacts performance and operability
- Low: Improvement recommended but limited impact

---

## Execution Example

```markdown
### Availability Investigation Execution

1. <External Integration A> retry logic investigation
   - Serena: search_for_pattern("retry", relative_path="<integration path>")
   - Result: Confirmed <library> usage at <file path>:<line>
   - As-Is: <count> retries at <interval> second intervals

2. Timeout settings investigation
   - Serena: find_symbol("timeout", relative_path="config")
   - Result: DB connection timeout <sec>s at <file path>:<line>
   - As-Is: HTTP <sec>s, DB <sec>s
```

---

**Last Updated**: YYYY-MM-DD
