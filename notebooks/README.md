# Notebook Examples

This directory contains example Jupyter notebooks for Microsoft Sentinel data lake operations. Each notebook demonstrates specific security scenarios and operations.

## Hello-World Notebooks

### [Show Tables](hello-world/show-tables/show-tables.ipynb)

Quick connectivity verification notebook that lists available databases and tables in your Sentinel environment. Perfect for first-time setup validation and environment discovery. Uses [`MicrosoftSentinelProvider`](hello-world/show-tables/show-tables.ipynb:30) to enumerate system tables and workspace-specific tables. Ideal for new users verifying access permissions and exploring available data sources.

### [Hello CSL](hello-world/hello-csl/hello-csl.ipynb)

Demonstrates loading and querying the CommonSecurityLog (CSL) table with important column filtering techniques. Includes workaround for known Parquet schema compatibility issue with `DeviceCustomFloatingPoint1` column in Sentinel data lake. Shows proper column selection patterns to avoid data type conversion errors. Essential reading for anyone working with CommonSecurityLog data.

**Note:** Always scope CSL queries to specific columns to avoid schema issues. See Section 3 for column filtering example.

## Custom Graph Notebooks

### [PAM Complete](custom-graph/pam-complete/pam-complete.ipynb)

Comprehensive demonstration of Microsoft Sentinel Custom Graph capabilities for ISV integration scenarios using synthetic data. Showcases privileged access management (PAM) vendor data combined with Microsoft security telemetry (EntraUsers, AzureActivity, AuditLogs) to perform advanced graph analytics similar to Microsoft Security Exposure Management (MSEM). Demonstrates all 5 built-in graph algorithms (Centrality, K-Hop, Reachability, Blast Radius, Ranked Paths) plus GraphFrames extensibility with synthetic data (≤50 rows per table).

## Risk Scoring Notebooks

### [User Risk Score Simple](risk-scoring/user-risk-score-simple/README.md)

Training notebook for learning Microsoft Sentinel analytics through basic user risk scoring. Calculates 50-point risk scores based on IP diversity, sign-in frequency, and activity consistency patterns. Perfect for new Sentinel users, security analysts learning PySpark, and risk scoring pilots. Uses SigninLogs and EntraUsers tables only.

### [User Risk Score Complete](risk-scoring/user-risk-score-complete/README.md)

Production-ready comprehensive user risk scoring system for SOC teams. Calculates 100-point risk scores across 6 categories: sign-in behavior (30 pts), application access (25 pts), privileged activity (20 pts), security alerts (15 pts), geographic risk (5 pts), and temporal risk (5 pts). Uses SigninLogs, EntraUsers, AuditLogs, and SecurityAlert tables with graceful degradation for optional sources. Ideal for threat hunting, insider threat programs, and automated risk workflows.

## Organization

Further notebooks will be organized by category based on their primary use case, *i.e.*

- **threat-hunting/** - Proactive security investigations and threat hunting scenarios
- **incident-response/** - Reactive security operations and incident investigation
- **reporting/** - Analytics, dashboards, and reporting workflows
- **data-exploration/** - Data discovery, profiling, and exploration

Categories are created organically as notebooks are added. If you're contributing a new notebook, choose the most appropriate category or propose a new one if needed.

## Notebook Structure

Each notebook is contained in its own directory with the following structure:

```
category-name/
└── notebook-name/
    ├── README.md          # Overview, prerequisites, usage instructions
    ├── DESIGN.md          # Architecture, data sources, approach
    ├── IMPLEMENTATION.md  # Implementation notes, gotchas, improvements
    └── notebook.ipynb     # The Jupyter notebook (sanitized)
```

## Using These Notebooks

### Prerequisites

- Azure subscription with Microsoft Sentinel data lake configured
- Access to a Sentinel workspace
- Permissions to run notebooks in the Sentinel Spark environment

### Getting Started

1. **Copy to your workspace area**:
   ```bash
   cp -r notebooks/threat-hunting/example-notebook workspace/threat-hunting/
   ```

2. **Update configuration**: Edit the notebook and replace placeholder values:
   ```python
   WORKSPACE_NAME = "<YOUR_WORKSPACE_NAME>"  # Replace with your workspace
   ```

3. **Upload and run**: Upload the notebook to your Sentinel data lake environment and execute.

For detailed setup instructions, see the [docs/getting-started.md](../docs/getting-started.md) guide.

## Contributing

If you're developing a new notebook or updating an existing one, please follow the contribution guidelines in [CONTRIBUTING.md](../CONTRIBUTING.md).

Key points:
- All notebooks must be sanitized (no outputs, no real credentials) before committing
- Use the workspace directory for development with real data
- Include complete documentation (README, DESIGN, IMPLEMENTATION)
- Follow the established category structure
