# User Risk Score Complete - Production Notebook

A comprehensive user risk scoring system for Microsoft Sentinel that analyzes behavior across 4 data sources to calculate a 100-point risk score.

## Purpose

Production-ready risk scoring for security operations teams to prioritize investigations, identify insider threats, detect compromised accounts, and monitor privileged users.

**Perfect for:** SOC teams, security monitoring, threat hunting, insider threat programs, and automated risk workflows.

> **📖 For detailed design rationale, scoring algorithms, and architecture, see [`DESIGN.md`](DESIGN.md)**

## What This Notebook Does

Calculates a **100-point user risk score** across 6 categories:

- **Sign-in Behavior (30 pts)** - IP diversity, device diversity, frequency anomalies
- **Application Access (25 pts)** - Unique apps and resources accessed
- **Privileged Activity (20 pts)** - Admin operations and high-risk actions
- **Security Alerts (15 pts)** - Active alerts and severity weighting
- **Geographic Risk (5 pts)** - Location-based indicators
- **Temporal Risk (5 pts)** - Off-hours activity patterns

**Risk Levels:** Low (0-30) | Medium (31-60) | High (61-100)

**Data Sources:** SigninLogs, EntraUsers, AuditLogs (optional), SecurityAlert (optional)

**Graceful Degradation:** Works with 2-4 tables depending on availability

## Prerequisites

- Microsoft Sentinel workspace access
- Synapse Analytics notebook environment
- Read permissions on SigninLogs and EntraUsers (required)
- Read permissions on AuditLogs and SecurityAlert (optional but recommended)

## Quick Start

1. Open the notebook in Synapse Analytics
2. Update configuration:
   ```python
   WORKSPACE_NAME = "<YOUR_WORKSPACE_NAME>"
   ANALYSIS_DAYS = 14
   ```
3. Run all cells (⏵ Run All)
4. Results saved to **`UserRiskScores_SPRK`** custom table

## Example Queries

```kql
// High-risk users requiring investigation
UserRiskScores_SPRK
| where risk_level == "High"
| order by total_risk_score desc
| project UserPrincipalName, total_risk_score, signin_behavior_score, 
          security_alert_score, active_alert_count, has_active_alerts

// Users with active security alerts
UserRiskScores_SPRK
| where has_active_alerts == true
| order by alert_severity_score desc

// Privileged users with elevated risk
UserRiskScores_SPRK
| where privileged_activity_score > 10
| where total_risk_score > 40
| project UserPrincipalName, jobTitle, privileged_activity_score, 
          total_admin_operations, high_risk_operations
```

## Key Features

- **Multi-dimensional scoring** - Combines authentication, privileges, alerts, and context
- **Department-aware baselines** - Context-sensitive frequency analysis
- **Weighted severity** - Security alerts get proportional impact based on severity
- **Production-ready** - Error handling, metadata tracking, configurable parameters
- **Graceful degradation** - Works even if optional tables unavailable

## Files

- [`User Risk Score Complete.ipynb`](User%20Risk%20Score%20Complete.ipynb) - The notebook
- [`DESIGN.md`](DESIGN.md) - Complete design, methodology, scoring algorithms, and use cases
