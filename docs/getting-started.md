# Getting Started with Microsoft Sentinel Data Lake Notebooks

This guide will help you get started with Microsoft Sentinel data lake notebooks, whether you want to run existing examples or create your own custom analytics.

## Prerequisites

Before you begin, ensure you have:

### Azure Environment
- **Azure subscription** with billing access
- **Microsoft Sentinel workspace** configured for data lake
- **Data lake onboarding** completed ([onboarding guide](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-onboarding))

### Permissions
- **Read access** to run notebooks and query data
- **Microsoft Sentinel Contributor** role (to write results to custom tables)
- **Storage Blob Data Contributor** role (alternative for writing custom tables)

### Knowledge (Recommended)
- Basic Python programming
- Familiarity with PySpark or SQL
- Understanding of Microsoft Sentinel concepts (tables, logs, alerts)

## Understanding the Repository Structure

```
MsSentinel.Notebooks/
├── notebooks/          # Published, sanitized notebook examples
│   └── risk-scoring/
├── workspace/          # Your private development area (gitignored)
├── templates/          # Templates for creating new notebooks
│   └── notebook-template.ipynb
├── scripts/            # Utility scripts (sanitize, setup, validate)
└── docs/              # Documentation (you are here!)
```

**Key Concepts:**
- **notebooks/** - Sanitized examples ready to use (no credentials, no outputs)
- **workspace/** - Where you work with real data and credentials (never committed to git)
- **templates/** - Starting points for creating new notebooks

## Path 1: Run an Example Notebook

Follow these steps to run an existing notebook from the examples:

### Step 1: Choose a Notebook

Browse the [`notebooks/`](../notebooks/) directory and select a notebook that fits your needs.

Example: [`notebooks/risk-scoring/user-risk-score-simple/`](../notebooks/risk-scoring/user-risk-score-simple/)

Read the notebook's README.md to understand:
- What it does
- Data sources required
- Prerequisites and permissions
- Expected outputs

### Step 2: Copy to Workspace

Copy the notebook to your workspace directory (which is gitignored) using the setup script:

```bash
# Use the setup script (recommended)
python scripts/setup-workspace.py --copy risk-scoring/user-risk-score-simple
```

**Alternative (manual copy):**
```bash
# Unix/Mac
cp -r notebooks/risk-scoring/user-risk-score-simple workspace/risk-scoring/

# Windows PowerShell
Copy-Item -Recurse notebooks/risk-scoring/user-risk-score-simple workspace/risk-scoring/
```

**Tip:** Run `python scripts/setup-workspace.py --list` to see all available notebooks.

### Step 3: Configure the Notebook

Open the notebook in your workspace and update configuration placeholders:

```python
# Replace this placeholder
WORKSPACE_NAME = "<YOUR_WORKSPACE_NAME>"

# With your actual workspace name
WORKSPACE_NAME = "my-sentinel-workspace"
```

Common configuration items:
- Workspace name
- Time windows (analysis days)
- Thresholds and scoring parameters
- Custom table names

### Step 4: Upload to Sentinel

1. Navigate to your **Microsoft Sentinel workspace** in Azure Portal
2. Go to **Notebooks** section
3. Click **Upload notebook**
4. Select your configured notebook from `workspace/`
5. Choose an appropriate **compute** (Small, Medium, or Large pool)

### Step 5: Run the Notebook

1. Open the uploaded notebook in Sentinel
2. Select the compute pool size
3. Wait for compute to start (may take 2-5 minutes)
4. Run cells one at a time or use **Run All**
5. Review outputs and results

**Tip:** Run cells individually first to understand the flow and catch any configuration issues early.

## Path 2: Create Your Own Notebook with AI Assistance

Use the notebook template to build custom security analytics:

### Step 1: Create from Template

Create a new notebook structure from the template using the setup script:

```bash
# Use the setup script (recommended) - creates full structure
python scripts/setup-workspace.py --create my-category/my-analysis
```

This creates:
- `workspace/my-category/my-analysis/my-analysis.ipynb` (from template)
- `workspace/my-category/my-analysis/README.md` (placeholder)
- `workspace/my-category/my-analysis/DESIGN.md` (placeholder)
- `workspace/my-category/my-analysis/IMPLEMENTATION.md` (placeholder)

**Alternative (manual):**
```bash
# Unix/Mac
mkdir -p workspace/my-analysis
cp templates/notebook-template.ipynb workspace/my-analysis/notebook.ipynb

# Windows PowerShell
New-Item -ItemType Directory -Path workspace/my-analysis -Force
Copy-Item templates/notebook-template.ipynb workspace/my-analysis/notebook.ipynb
```

### Step 2: Describe Your Analysis Goal

Open the template and fill in the task description section with details:

- **Goal**: What security analysis do you want to perform?
- **Data Sources**: Which Sentinel tables (SigninLogs, AuditLogs, SecurityAlert, etc.)?
- **Analysis**: What metrics or calculations are needed?
- **Output**: What results do you want (charts, tables, alerts)?
- **Use Case**: Who will use this and how?

**Example:**
> "Analyze failed sign-in attempts from the SigninLogs table over the last 30 days. Calculate the number of failed attempts per user, identify patterns by time of day and location, and flag users with more than 10 failed attempts from different IP addresses. Visualize the results with charts and save high-risk users to a custom table."

### Step 3: Three-Phase Development with AI

Work with an AI assistant through these phases:

#### Phase 1: Design (15-30 minutes)
Ask your AI: *"Based on my description above and using the Microsoft Sentinel documentation links provided, create a detailed design document for this notebook."*

Review and iterate on:
- Data sources and table schemas
- Analysis methodology
- Expected output format
- Edge cases and limitations

Save the final design as `workspace/my-analysis/DESIGN.md`

#### Phase 2: Implementation Plan (15-30 minutes)
Ask your AI: *"Create a step-by-step implementation plan for this notebook with cell-by-cell instructions."*

Review and iterate on:
- Logical flow and structure
- Required libraries and PySpark operations
- Error handling strategies
- Testing approach

Save the final plan as `workspace/my-analysis/IMPLEMENTATION.md`

#### Phase 3: Implementation (1-3 hours)
Ask your AI: *"Create cell 1 according to the implementation plan."*

For each cell:
1. Have AI generate the code
2. Run and test the cell
3. If errors occur, share them with AI and iterate
4. Move to next cell only when current cell works
5. Repeat until complete

**Key Principle:** Test each cell before moving forward. Never skip ahead with broken code.

### Step 4: Test and Validate

Once complete:
- Run the entire notebook end-to-end
- Verify all outputs are correct
- Check data quality at each stage
- Validate final results match expectations
- Test with different date ranges or parameters

### Step 5: Document and Share

If your notebook might be useful to others:
1. Ensure DESIGN.md and IMPLEMENTATION.md are complete
2. Create a README.md describing usage
3. Sanitize the notebook (see Publishing section below)
4. Consider contributing back to the repository

## Understanding Sentinel Data Lake Tables

Common tables you'll work with:

### Identity & Authentication
- **SigninLogs** - User authentication events (logins, IP addresses, locations)
- **EntraUsers** - User profile information (display names, departments, emails)
- **AuditLogs** - Administrative actions and configuration changes

### Security
- **SecurityAlert** - Security alerts from various sources
- **SecurityIncident** - Incidents grouping related alerts
- **ThreatIntelligenceIndicator** - Threat intelligence indicators

### Network & Infrastructure
- **AzureActivity** - Azure resource management activities
- **AzureNetworkAnalytics** - Network flow data

[Full table reference →](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables-index)

## Working with the Microsoft Sentinel Provider

All notebooks use the `MicrosoftSentinelProvider` class to interact with data:

### Basic Usage

```python
from sentinel_lake.providers import MicrosoftSentinelProvider

# Initialize provider
sentinel_provider = MicrosoftSentinelProvider(spark)

# Read from a table
df = sentinel_provider.read_table('SigninLogs', 'my-workspace-name')

# Write to a custom table
sentinel_provider.save_as_table(
    output_df,
    'MyCustomTable_SPRK',
    write_options={'mode': 'overwrite'}
)
```

### Common Patterns

**Filter by date range:**
```python
from pyspark.sql.functions import col, expr

df = (
    sentinel_provider.read_table('SigninLogs', workspace_name)
    .filter(col("TimeGenerated") >= expr("current_timestamp() - INTERVAL 30 DAYS"))
)
```

**Select specific columns:**
```python
df = df.select("UserId", "UserPrincipalName", "IPAddress", "TimeGenerated")
```

**Aggregate data:**
```python
from pyspark.sql.functions import count, countDistinct

summary = (
    df.groupBy("UserId")
    .agg(
        count("*").alias("total_events"),
        countDistinct("IPAddress").alias("unique_ips")
    )
)
```

[Full provider reference →](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-provider-class-reference)

## Publishing Your Notebook

Before sharing or committing a notebook to the repository:

### 1. Sanitize and Publish

Use the sanitization script to remove outputs, replace credentials, and publish to the [`notebooks/`](../notebooks/) directory:

```bash
# Sanitize and publish to notebooks/ directory
python scripts/sanitize-notebook.py --publish workspace/my-category/my-analysis/
```

This will:
- Remove all cell outputs and execution counts
- Replace credentials with placeholders (e.g., `<YOUR_WORKSPACE_NAME>`)
- Validate required documentation files exist
- Copy sanitized files to `notebooks/my-category/my-analysis/`

**Note:** Your workspace original remains unchanged with outputs intact.

### 2. Verify Documentation

Ensure you have all required files:
- `README.md` - User-facing overview
- `DESIGN.md` - Architecture and approach
- `IMPLEMENTATION.md` - Technical details and gotchas
- `notebook.ipynb` - The sanitized notebook

### 3. Review Before Committing

- No real workspace names or credentials
- No cell outputs visible
- Documentation is complete and accurate
- Code runs successfully with placeholder values

## Troubleshooting

### "Permission denied when writing to custom table"

**Solution:** You need Microsoft Sentinel Contributor or Storage Blob Data Contributor role. Contact your Azure admin or use the notebook's fallback to export CSV:

```python
output_df.toPandas().to_csv('results.csv', index=False)
```

### "Table not found"

**Causes:**
- Table name misspelled
- Data connector not enabled for that table
- Workspace name incorrect

**Solution:** Verify the table exists in your workspace:
```python
# List available tables
spark.sql("SHOW TABLES").show()
```

### "Compute pool not starting"

**Causes:**
- Insufficient quota
- Temporary Azure service issue

**Solution:** 
- Try a smaller compute pool
- Wait a few minutes and retry
- Check Azure service health status

### "Out of memory errors"

**Solutions:**
- Use smaller date ranges
- Filter data earlier in the pipeline
- Use `.select()` to reduce columns
- Choose a larger compute pool
- Add `.persist()` strategically to cache intermediate results

## Next Steps

Now that you're set up:

1. **Explore Examples**: Try running the [User Risk Score Simple](../notebooks/risk-scoring/user-risk-score-simple/) notebook
2. **Read Documentation**: Review the DESIGN.md files to understand architectural patterns
3. **Build Your Own**: Use the [notebook template](../templates/notebook-template.ipynb) to create custom analytics
4. **Join the Community**: Share feedback and contribute improvements

## Additional Resources

- [Microsoft Sentinel Data Lake Overview](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-overview)
- [Notebook Examples (Microsoft Docs)](https://learn.microsoft.com/en-us/azure/sentinel/datalake/notebook-examples)
- [PySpark SQL Functions Reference](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html)
- [Repository Structure Guide](README.md)

---

**Questions or Issues?** Check the troubleshooting section above or review the example notebooks for working patterns.
