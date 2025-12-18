# User Risk Score Simple - Training Notebook

A simplified training notebook for learning Microsoft Sentinel analytics fundamentals through basic user risk scoring.

## Purpose

Educational tool for users new to Microsoft Sentinel. Teaches core concepts through calculating user risk scores based on sign-in behavior.

**Perfect for:** New Sentinel users, security analysts learning PySpark, training workshops, and risk scoring pilots.

> **📖 For detailed design rationale, scoring algorithms, and architecture, see [`DESIGN.md`](DESIGN.md)**

## What This Notebook Does

Calculates a **50-point user risk score** based on:
- **IP Diversity** (0-20 points): Number of different IP addresses
- **Sign-in Frequency** (0-20 points): Number of sign-ins in 14 days
- **Consistency Pattern** (0-10 points): Activity distribution

**Risk Levels:** Low (0-15) | Medium (16-30) | High (31-50)

**Data Sources:** SigninLogs and EntraUsers tables only

## Prerequisites

- Microsoft Sentinel workspace access
- Synapse Analytics notebook environment
- Read permissions on SigninLogs and EntraUsers tables

## Quick Start

1. Open the notebook in Synapse Analytics
2. Update configuration:
   ```python
   WORKSPACE_NAME = "<YOUR_WORKSPACE_NAME>"
   ANALYSIS_DAYS = 14
   ```
3. Run all cells (⏵ Run All)
4. Results saved to **`UserRiskScoreSimple_SPRK`** custom table

## Example Query

```kql
// View high-risk users
UserRiskScoreSimple_SPRK
| where risk_level == "High"
| order by total_risk_score desc
| take 10
```

## What You'll Learn

- Connect to Sentinel and read data
- PySpark operations: filter, groupBy, join, aggregate
- Risk scoring methodology and threshold-based classification
- Write results to custom tables and create visualizations

## Next Steps

- Modify scoring thresholds in Section 6
- Add custom metrics (application diversity, temporal patterns)
- Progress to the complete Risk Score notebook
- Schedule automated execution

## Files

- [`User Risk Score Simple.ipynb`](User%20Risk%20Score%20Simple.ipynb) - The notebook
- [`DESIGN.md`](DESIGN.md) - Detailed design, architecture, and scoring algorithms
