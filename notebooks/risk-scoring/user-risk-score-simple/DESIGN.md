# User Risk Score Simple - Training Notebook Design

## Executive Summary

This simplified notebook is designed as a **training tool** for users new to Microsoft Sentinel to understand fundamental concepts:
- Reading data from Sentinel tables
- Performing basic PySpark aggregations
- Calculating simple risk scores
- Visualizing results with charts
- Writing results back to a custom table

**Simplified Approach:**
- **2 tables only**: SigninLogs + EntraUsers
- **2-4 columns per table**: Focus on essentials
- **3 risk categories (50 points total)**: Easier to understand
- **12 output columns**: Streamlined for clarity
- **No department baselines**: Removes complexity
- **Output table**: `UserRiskScoreSimple_SPRK`

---

## Prompt history

Me: "Review the user_risk_score_design.md and implementation in Risk Score.ipynb. This risk score notebook is *GREAT*. 

However, it will be hard for someone new to understand all these new concepts. I would like a **simpler** version for training.

Design a simpler alternative notebook that will help people new to Sentinel to understand these topics. Leading from Sentinel, making simple calcuilations, showing a graph, saving a notebook. Let's keep it easier to start!

I'm thinking it should

* Use 2 tables only, for simplicity
* Use only 2-4 columns max from each table
* Don't need department baselines
* We'd call it "UserRiskScoreSimple" and write to a table of that name."

Roo: "Based on my review of the existing risk score notebook, I can see it's comprehensive but complex (4 tables, 27 output columns, 6 risk categories). Let me design a simpler training-focused alternative. For the simplified training notebook, which 2 tables would you prefer to use? I'm thinking about these options for teaching Sentinel basics: ..."

Me: "Proceed with SigninLogs + EntraUsers as the best balance for training"

Roo: "I've created a comprehensive design plan for a simplified User Risk Score training notebook at plans/user_risk_score_simple_design.md."

Me: "Please implement this! Refer to the Risk Score.ipynb where needed for appropriate patterns, because that notebook has been proven to work well."

Roo: "I'll implement the simplified notebook now, using proven patterns from the existing Risk Score.ipynb."

---

## Table of Contents

1. [Learning Objectives](#learning-objectives)
2. [Data Sources](#data-sources)
3. [Simplified Risk Scoring](#simplified-risk-scoring)
4. [Output Schema](#output-schema)
5. [Notebook Structure](#notebook-structure)
6. [Key Differences from Full Version](#key-differences-from-full-version)

---

## Learning Objectives

By completing this notebook, users will learn:

✅ **Sentinel Basics**
- How to connect to Sentinel workspace
- How to read data from Sentinel tables
- Understanding basic table schemas (SigninLogs, EntraUsers)

✅ **PySpark Fundamentals**
- Filtering data with `.filter()`
- Aggregating with `.groupBy()` and `.agg()`
- Counting unique values with `countDistinct()`
- Joining two DataFrames
- Creating calculated columns with `.withColumn()`

✅ **Risk Scoring Concepts**
- Simple threshold-based scoring
- Combining multiple risk factors
- Classifying users into risk levels

✅ **Visualization**
- Creating bar charts with matplotlib
- Displaying risk distribution

✅ **Data Persistence**
- Writing results to custom Sentinel tables
- Understanding table naming conventions (_SPRK suffix)

---

## Data Sources

### Table 1: SigninLogs (3 columns)

**Purpose:** User authentication patterns

**Columns Used:**
- `UserId` - Unique user identifier (for joining)
- `UserPrincipalName` - User email (for display)
- `IPAddress` - Source IP address (for diversity analysis)

**Filters:**
- Last 14 days only
- Member users only (exclude guests)
- Non-null UserId

**Why These Columns?**
- `IPAddress` is easy to understand and visualize (people signing in from different locations)
- Single behavioral metric keeps analysis simple
- Real security signal (unusual IP diversity = potential compromise)

### Table 2: EntraUsers (4 columns)

**Purpose:** User profile and organizational context

**Columns Used:**
- `id` - Unique identifier (joins with SigninLogs.UserId)
- `displayName` - User's full name (for reporting)
- `mail` - Email address (backup identifier)
- `department` - Organizational unit (for context)

**Filters:**
- Non-null and non-empty id
- Drop duplicates by id

**Why These Columns?**
- Provides human-readable context (names, departments)
- Shows how to enrich security data with identity information
- Department is useful for analysis without being complex

---

## Simplified Risk Scoring

### Total Possible Score: 50 points

**Risk Levels:**
- **Low**: 0-15 points (most users)
- **Medium**: 16-30 points (unusual activity)
- **High**: 31-50 points (investigate immediately)

### Category 1: IP Diversity Score (0-20 points)

**Metric:** Unique IP address count per user (last 14 days)

| Unique IPs | Score | Interpretation |
|------------|-------|----------------|
| 1 | 0 | Normal - single location |
| 2-3 | 5 | Normal - home + office or travel |
| 4-6 | 12 | Elevated - multiple locations |
| 7+ | 20 | High - suspicious diversity |

**Rationale:**
- Most users sign in from 1-3 IPs (home, office, maybe coffee shop)
- 7+ unique IPs in 2 weeks suggests credential sharing or compromise
- Easy for new users to understand and visualize

**PySpark Implementation:**
```python
.withColumn("ip_diversity_score",
    when(col("unique_ip_count") == 1, 0)
    .when(col("unique_ip_count") <= 3, 5)
    .when(col("unique_ip_count") <= 6, 12)
    .otherwise(20)
)
```

### Category 2: Sign-in Frequency Score (0-20 points)

**Metric:** Total sign-in count per user (last 14 days)

| Total Sign-ins | Score | Interpretation |
|----------------|-------|----------------|
| 1-50 | 0 | Low activity - normal |
| 51-150 | 5 | Moderate activity - normal |
| 151-300 | 12 | High activity - monitor |
| 301+ | 20 | Very high activity - unusual |

**Rationale:**
- Typical users: 3-10 sign-ins per day = 42-140 per 14 days
- 300+ sign-ins = 21+ per day suggests automation or abnormal behavior
- Simple threshold approach (no baselines needed)
- Easy to explain to non-technical users

**PySpark Implementation:**
```python
.withColumn("frequency_score",
    when(col("total_signins") <= 50, 0)
    .when(col("total_signins") <= 150, 5)
    .when(col("total_signins") <= 300, 12)
    .otherwise(20)
)
```

### Category 3: Consistency Score (0-10 points)

**Metric:** Sign-in consistency (activity spread)

**Calculation:**
- Average sign-ins per day = total_signins / 14
- If user has activity across multiple days = more consistent
- Single-day bursts = suspicious

| Pattern | Score | Interpretation |
|---------|-------|----------------|
| Consistent daily activity | 0 | Normal usage pattern |
| Occasional bursts | 5 | Moderate concern |
| Single-day spike | 10 | Suspicious pattern |

**Simplified Approach:**
We'll use the ratio of unique IPs to total sign-ins as a proxy:
- High ratio (many IPs, few sign-ins each) = 0 (normal travel)
- Low ratio (few IPs, many sign-ins) = more suspicious if combined with high frequency

**PySpark Implementation:**
```python
.withColumn("consistency_score",
    when(col("total_signins") >= 200, 
        when(col("unique_ip_count") <= 2, 10).otherwise(5)
    ).otherwise(0)
)
```

**Rationale:**
- 200+ sign-ins from only 1-2 IPs = possible automated access
- Keeps scoring simple while adding useful signal
- Demonstrates conditional logic in PySpark

### Total Risk Score Calculation

```python
.withColumn("total_risk_score",
    col("ip_diversity_score") + 
    col("frequency_score") + 
    col("consistency_score")
)

.withColumn("risk_level",
    when(col("total_risk_score") <= 15, "Low")
    .when(col("total_risk_score") <= 30, "Medium")
    .otherwise("High")
)
```

---

## Output Schema

### Table: `UserRiskScoreSimple_SPRK`

**12 columns total** (compared to 27 in full version)

| Field | Type | Category | Description |
|-------|------|----------|-------------|
| **Identity (4 columns)** |
| UserId | string | Identity | Unique user identifier |
| UserPrincipalName | string | Identity | User email/UPN |
| UserDisplayName | string | Identity | User's display name |
| department | string | Identity | User's department |
| **Risk Scores (4 columns)** |
| total_risk_score | int | Score | Overall risk (0-50) |
| risk_level | string | Score | Low/Medium/High |
| ip_diversity_score | int | Score | IP diversity subscore (0-20) |
| frequency_score | int | Score | Frequency subscore (0-20) |
| **Metrics (2 columns)** |
| unique_ip_count | int | Metric | Number of unique IPs |
| total_signins | int | Metric | Total sign-in events |
| **Metadata (2 columns)** |
| calculation_date | timestamp | Meta | When calculated |
| TimeGenerated | timestamp | Meta | Record creation time |

---

## Notebook Structure

### Section 1: Setup & Configuration (1 cell)
**Learning Goal:** Understand workspace connection

```python
# Import libraries
from sentinel_lake.providers import MicrosoftSentinelProvider
from pyspark.sql.functions import col, count, countDistinct, when, lit, current_timestamp

# Configuration
WORKSPACE_NAME = "YourWorkspaceName"
ANALYSIS_DAYS = 14

# Initialize provider
sentinel_provider = MicrosoftSentinelProvider(spark)
```

**What Users Learn:**
- Required imports for Sentinel + PySpark
- Configuration parameters
- Provider initialization pattern

---

### Section 2: Load SigninLogs (1 cell)
**Learning Goal:** Read and filter Sentinel data

```python
print("📊 Loading SigninLogs...")

signin_df = (
    sentinel_provider.read_table('SigninLogs', WORKSPACE_NAME)
    .filter(
        (col("UserType") == "Member") & 
        (col("UserId").isNotNull()) &
        (col("TimeGenerated") >= expr(f"current_timestamp() - INTERVAL {ANALYSIS_DAYS} DAYS"))
    )
    .select("UserId", "UserPrincipalName", "IPAddress")
    .persist()
)

print(f"✅ Loaded {signin_df.count()} sign-in events")
signin_df.show(5)
```

**What Users Learn:**
- `.read_table()` method
- Chaining filters with `.filter()`
- `.select()` to choose columns
- `.persist()` for caching
- `.count()` and `.show()` for inspection

---

### Section 3: Load EntraUsers (1 cell)
**Learning Goal:** Load profile data

```python
print("📊 Loading EntraUsers...")

users_df = (
    sentinel_provider.read_table('EntraUsers')
    .filter((col("id").isNotNull()) & (col("id") != ""))
    .select("id", "displayName", "mail", "department")
    .dropDuplicates(["id"])
    .persist()
)

print(f"✅ Loaded {users_df.count()} user profiles")
users_df.show(5)
```

**What Users Learn:**
- Multiple filter conditions
- `.dropDuplicates()` for data quality
- Working with identity data

---

### Section 4: Calculate Sign-in Metrics (1 cell)
**Learning Goal:** Aggregation basics

```python
print("🔍 Calculating sign-in metrics...")

signin_metrics = (
    signin_df
    .groupBy("UserId", "UserPrincipalName")
    .agg(
        countDistinct("IPAddress").alias("unique_ip_count"),
        count("*").alias("total_signins")
    )
)

print(f"✅ Calculated metrics for {signin_metrics.count()} users")
signin_metrics.orderBy(col("total_signins").desc()).show(10)
```

**What Users Learn:**
- `.groupBy()` for aggregation
- `.agg()` with multiple metrics
- `countDistinct()` vs `count()`
- `.alias()` for column naming
- `.orderBy()` for sorting

---

### Section 5: Join with User Profiles (1 cell)
**Learning Goal:** Joining DataFrames

```python
print("🔗 Enriching with user profiles...")

combined_df = (
    signin_metrics
    .join(users_df, signin_metrics.UserId == users_df.id, "left")
    .select(
        signin_metrics["UserId"],
        signin_metrics["UserPrincipalName"],
        users_df["displayName"].alias("UserDisplayName"),
        users_df["department"],
        col("unique_ip_count"),
        col("total_signins")
    )
)

print(f"✅ Enriched {combined_df.count()} user records")
combined_df.show(5)
```

**What Users Learn:**
- LEFT JOIN syntax
- Qualifying columns from specific DataFrames
- `.alias()` for renaming
- Why enrichment matters

---

### Section 6: Calculate Risk Scores (1 cell)
**Learning Goal:** Conditional logic and scoring

```python
print("🎯 Calculating risk scores...")

risk_scores = (
    combined_df
    # IP Diversity Score (0-20)
    .withColumn("ip_diversity_score",
        when(col("unique_ip_count") == 1, 0)
        .when(col("unique_ip_count") <= 3, 5)
        .when(col("unique_ip_count") <= 6, 12)
        .otherwise(20)
    )
    # Frequency Score (0-20)
    .withColumn("frequency_score",
        when(col("total_signins") <= 50, 0)
        .when(col("total_signins") <= 150, 5)
        .when(col("total_signins") <= 300, 12)
        .otherwise(20)
    )
    # Consistency Score (0-10)
    .withColumn("consistency_score",
        when(col("total_signins") >= 200, 
            when(col("unique_ip_count") <= 2, 10).otherwise(5)
        ).otherwise(0)
    )
    # Total Risk Score
    .withColumn("total_risk_score",
        col("ip_diversity_score") + col("frequency_score") + col("consistency_score")
    )
    # Risk Level
    .withColumn("risk_level",
        when(col("total_risk_score") <= 15, "Low")
        .when(col("total_risk_score") <= 30, "Medium")
        .otherwise("High")
    )
)

print("✅ Risk scores calculated")
risk_scores.select(
    "UserPrincipalName", "unique_ip_count", "total_signins",
    "ip_diversity_score", "frequency_score", "total_risk_score", "risk_level"
).orderBy(col("total_risk_score").desc()).show(10)
```

**What Users Learn:**
- `.withColumn()` for creating columns
- `when().otherwise()` for conditional logic
- Nested conditions
- Building composite scores
- Classification logic

---

### Section 7: Visualize Risk Distribution (1 cell)
**Learning Goal:** Creating visualizations

```python
print("📊 Creating risk distribution chart...")

import matplotlib.pyplot as plt

# Calculate distribution
risk_dist = risk_scores.groupBy("risk_level").count().orderBy("risk_level").toPandas()
total_users = risk_scores.count()

# Create bar chart
plt.figure(figsize=(10, 6))
colors = {"Low": "#2ecc71", "Medium": "#f39c12", "High": "#e74c3c"}
bars = plt.bar(
    risk_dist["risk_level"], 
    risk_dist["count"],
    color=[colors[level] for level in risk_dist["risk_level"]],
    edgecolor="black",
    linewidth=1.2
)

# Add labels
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2., height,
        f"{int(height)}\n({int(height)/total_users*100:.1f}%)",
        ha="center", va="bottom", fontsize=12, fontweight="bold"
    )

plt.xlabel("Risk Level", fontsize=14, fontweight="bold")
plt.ylabel("Number of Users", fontsize=14, fontweight="bold")
plt.title(f"User Risk Distribution (Total: {total_users} users)", 
          fontsize=16, fontweight="bold")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()

print("✅ Chart created")
```

**What Users Learn:**
- Converting Spark DataFrame to Pandas for plotting
- Creating bar charts with matplotlib
- Color coding for visual clarity
- Adding data labels
- Professional chart formatting

---

### Section 8: Prepare Final Output (1 cell)
**Learning Goal:** Output preparation and metadata

```python
print("📝 Preparing final output...")

output_df = (
    risk_scores
    .withColumn("calculation_date", current_timestamp())
    .withColumn("TimeGenerated", current_timestamp())
    .select(
        # Identity
        "UserId", "UserPrincipalName", "UserDisplayName", "department",
        # Risk Scores
        "total_risk_score", "risk_level", 
        "ip_diversity_score", "frequency_score",
        # Metrics
        "unique_ip_count", "total_signins",
        # Metadata
        "calculation_date", "TimeGenerated"
    )
    .orderBy(col("total_risk_score").desc())
)

print(f"✅ Output prepared: {output_df.count()} users, {len(output_df.columns)} columns")
output_df.show(10, truncate=False)
```

**What Users Learn:**
- Adding timestamp metadata
- Column ordering for readability
- Final `.select()` for output schema
- `.orderBy()` for prioritization

---

### Section 9: Write to Custom Table (1 cell)
**Learning Goal:** Persisting results

```python
print("💾 Writing to custom table...")

CUSTOM_TABLE_NAME = "UserRiskScoreSimple_SPRK"

try:
    sentinel_provider.save_as_table(
        output_df,
        CUSTOM_TABLE_NAME,
        write_options={"mode": "overwrite", "mergeSchema": "true"}
    )
    
    print(f"✅ Successfully wrote {output_df.count()} records to {CUSTOM_TABLE_NAME}")
    print(f"\n🔍 Query in KQL:")
    print(f"   {CUSTOM_TABLE_NAME}")
    print(f"   | where risk_level == 'High'")
    print(f"   | order by total_risk_score desc")
    
except Exception as e:
    print(f"❌ Could not write to table: {e}")
    print(f"⚠️  Note: Writing requires Microsoft Sentinel Contributor permissions")
    print(f"\n💡 Your results are still in 'output_df' for analysis")
```

**What Users Learn:**
- `.save_as_table()` method
- Write modes (overwrite)
- Error handling with try/except
- Permission requirements
- Sample KQL queries for the output

---

### Section 10: Summary & Next Steps (1 cell - markdown)
**Learning Goal:** Recap and progression path

```markdown
## 🎉 Congratulations!

You've successfully:
- ✅ Loaded data from 2 Sentinel tables
- ✅ Performed aggregations and joins
- ✅ Calculated risk scores with conditional logic
- ✅ Created visualizations
- ✅ Saved results to a custom table

### What You Learned

**Sentinel Skills:**
- Connecting to workspace
- Reading from SigninLogs and EntraUsers
- Understanding table schemas

**PySpark Skills:**
- Filtering: `.filter()`, `.select()`
- Aggregating: `.groupBy()`, `.agg()`, `countDistinct()`
- Joining: LEFT JOIN with qualified columns
- Transforming: `.withColumn()`, `when().otherwise()`

**Security Analytics:**
- IP diversity as a risk signal
- Threshold-based scoring
- Risk level classification

### Next Steps

**To Enhance This Notebook:**
1. Add off-hours analysis (temporal patterns)
2. Include application diversity (unique apps accessed)
3. Add device diversity (unique user agents)

**Progress to Full Version:**
- Explore the full `Risk Score.ipynb` notebook
- Adds AuditLogs (admin operations) and SecurityAlert
- Department baselines for context-aware scoring
- 6 risk categories, 27 output columns

**Apply in Production:**
- Schedule this notebook to run daily/weekly
- Create workbooks to visualize trends
- Build analytics rules based on risk scores
- Join with other tables for correlation
```

---

## Key Differences from Full Version

| Aspect | Simple Version | Full Version |
|--------|---------------|--------------|
| **Tables** | 2 (SigninLogs, EntraUsers) | 4 (+ AuditLogs, SecurityAlert) |
| **Columns per Table** | 2-4 | 5-8 |
| **Risk Categories** | 3 (IP, Frequency, Consistency) | 6 (+ Admin, Alerts, Geographic, Temporal) |
| **Total Points** | 50 | 100 |
| **Output Columns** | 12 | 27 |
| **Baselines** | None | Department-aware baselines |
| **Complexity** | Beginner | Advanced |
| **Cells** | 10 | 12+ |
| **Runtime** | ~2-3 min | ~5-15 min |
| **Target Audience** | New to Sentinel | Production use |

---

## Advantages for Training

✅ **Easier to Understand**
- Only 2 tables to learn
- Simple metrics (IPs and counts)
- Clear scoring thresholds

✅ **Faster Execution**
- Less data to process
- Fewer joins
- Quick iteration for learning

✅ **Focused Learning**
- Each cell teaches one concept
- Progressive complexity
- Clear input/output at each step

✅ **Still Valuable**
- Real security signals
- Production-ready output table
- Foundation for enhancement

✅ **Encourages Exploration**
- Easy to modify thresholds
- Simple to add new metrics
- Clear path to full version

---

## Expected Results

**Typical Risk Distribution (example):**
- **Low Risk**: 75-85% of users (normal activity)
- **Medium Risk**: 12-20% of users (monitor)
- **High Risk**: 3-8% of users (investigate)

**High-Risk User Profile Examples:**
- User signing in from 10+ different IPs in 2 weeks
- User with 500+ sign-ins from only 2 IPs (automation?)
- User with unusual burst pattern (300+ sign-ins in one day)

**Use Cases:**
- Training new security analysts on Sentinel
- Understanding PySpark DataFrame operations
- Learning risk scoring fundamentals
- Building confidence before tackling complex notebooks

---

## Migration Path

Once comfortable with this simple version, users can:

1. **Add Temporal Analysis** (Section 3.5)
   - Calculate off-hours sign-ins
   - Add `temporal_risk_score` (0-10 points)

2. **Add Application Diversity** (Section 4.5)
   - Use `AppId` from SigninLogs
   - Add `app_diversity_score` (0-10 points)

3. **Add SecurityAlert** (Sections 5-6)
   - Load active alerts
   - Join on `CompromisedEntity`
   - Add `alert_risk_score` (0-20 points)

4. **Add AuditLogs** (Sections 7-8)
   - Load admin operations
   - Parse JSON `InitiatedBy` field
   - Add `admin_risk_score` (0-20 points)

5. **Add Department Baselines** (Section 9)
   - Calculate per-department averages
   - Use in frequency scoring
   - More context-aware risk assessment

Each addition builds on the foundation without breaking existing code.

---

## Success Criteria

Users completing this notebook should be able to:

✅ Connect to a Sentinel workspace  
✅ Read data from multiple tables  
✅ Filter and select relevant columns  
✅ Perform basic aggregations  
✅ Join two DataFrames  
✅ Create calculated columns with conditions  
✅ Visualize results with matplotlib  
✅ Write output to custom tables  
✅ Understand basic risk scoring concepts  
✅ Read and modify PySpark code confidently

---

## Conclusion

This simplified notebook provides a **gentle introduction** to Sentinel security analytics while still delivering **real value** through actionable risk scores. It serves as both a **training tool** and a **foundation** that can be incrementally enhanced into the full-featured risk scoring system.

The focus on **2 tables, simple metrics, and clear progression** makes it ideal for:
- New Sentinel users learning the platform
- Security analysts learning PySpark
- Teams wanting to pilot risk scoring before full deployment
- Training workshops and documentation

By mastering this simple version, users build the confidence and skills needed to tackle more complex security analytics in Sentinel.