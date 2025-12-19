# Microsoft Sentinel Data Lake Notebook Examples (Preview Features)

⚠️ **This is a private preview repository** containing notebooks that use Microsoft Sentinel features still in preview or not yet generally available.

## About This Repository

This repository contains advanced notebook examples that demonstrate upcoming Microsoft Sentinel data lake capabilities. These notebooks require:
- Preview feature enrollment
- Specific feature flags enabled
- Beta/preview API access

**Public Repository**: For notebooks using generally available features, see [MsSentinel.Notebooks](https://github.com/jcoliz/MsSentinel.Notebooks)

## Preview Features Used

Current notebooks in this repository use the following preview features:
- _[Add features as notebooks are created]_
- _Example: Advanced hunting ML models (Preview)_
- _Example: Custom entity enrichment APIs (Private Preview)_

## 📚 Preview Notebooks

Explore preview notebooks in the [`notebooks/`](notebooks/) directory:

_[Update this section as notebooks are added]_

## 🚀 Quick Start

### Prerequisites

1. **Preview Access**: Ensure your Sentinel workspace is enrolled in required preview programs
2. **Feature Flags**: Enable necessary feature flags in Azure Portal
3. **API Access**: Verify you have access to preview APIs

### Using Notebooks

Same workflow as main repository:

1. List available notebooks: `python scripts/setup-workspace.py --list`
2. Copy to workspace: `python scripts/setup-workspace.py --copy category/notebook-name`
3. Update configuration (e.g., `WORKSPACE_NAME`)
4. Upload and run in your Sentinel environment

[View detailed setup guide →](docs/getting-started.md)

## 🤖 Build Your Own Notebooks

Use the [**notebook template**](templates/notebook-template.ipynb) to create custom security analytics with AI assistance:

1. Copy [`templates/notebook-template.ipynb`](templates/notebook-template.ipynb) to your workspace
2. Describe your security analysis goal in natural language
3. Work with an AI assistant through three phases:
   - **Design** - Create and iterate on approach
   - **Plan** - Build implementation roadmap
   - **Implement** - Build cell-by-cell with testing

[Learn more about AI-assisted development →](templates/)

## 📖 Documentation

- [Getting Started](docs/getting-started.md) - Complete setup and usage guide
- [Migration Guide](docs/migration-guide.md) - Publishing notebooks when features release
- [Repository Structure](docs/repository-structure.md) - How this repository is organized

## 🔧 Tools & Scripts

Same scripts as main repository:
- [`setup-workspace.py`](scripts/) - Copy notebooks to workspace or create new ones from templates
- [`sanitize-notebook.py`](scripts/) - Remove outputs and credentials before publishing
- [`validate-notebooks.py`](scripts/) - Validation checks for CI/CD

[View all scripts →](scripts/)

## Publishing to Main Repository

When preview features become generally available, notebooks are migrated to the [public repository](https://github.com/jcoliz/MsSentinel.Notebooks).

See [Migration Guide](docs/migration-guide.md) for the publishing process.

## 📚 Microsoft Sentinel References

- [Microsoft Sentinel Preview Features](https://learn.microsoft.com/en-us/azure/sentinel/preview-features)
- [What is Microsoft Sentinel data lake?](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-overview)
- [Onboard to Microsoft Sentinel data lake](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-onboarding)
- [Microsoft Sentinel Provider class](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-provider-class-reference)
- [Available system tables](https://learn.microsoft.com/en-us/azure/sentinel/datalake/enable-data-connectors)
- [Available workspace tables](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables-index)

---

**Access**: This is a private repository. Contact [repository owner] for access requests.

**Get Started:** [Browse preview notebooks](notebooks/) or [create your own with AI assistance](templates/)
