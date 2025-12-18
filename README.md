# Microsoft Sentinel Data Lake Notebook Examples

This repository contains examples of Jupyter notebooks for Microsoft Sentinel data lake that demonstrate security scenarios and analytics. My goal is to illustrate the possibilities of Sentinel Data lake for your security scenarios, and teach you how to build your own for your unique needs.

## 📚 Notebook Examples

Explore ready-to-use notebooks in the [`notebooks/`](notebooks/) directory:

### Risk Scoring
- **[User Risk Score Simple](notebooks/risk-scoring/user-risk-score-simple/)** - Training notebook for learning Sentinel analytics through basic user risk scoring
- **[User Risk Score Complete](notebooks/risk-scoring/user-risk-score-complete/)** - Production-ready comprehensive user risk scoring system

[View all notebooks →](notebooks/)

## 🤖 Build Your Own Notebooks

Use the [**notebook template**](templates/notebook-template.ipynb) to create custom security analytics with AI assistance:

1. Copy [`templates/notebook-template.ipynb`](templates/notebook-template.ipynb) to your workspace
2. Describe your security analysis goal in natural language
3. Work with an AI assistant through three phases:
   - **Design** - Create and iterate on approach
   - **Plan** - Build implementation roadmap
   - **Implement** - Build cell-by-cell with testing

[Learn more about AI-assisted development →](templates/)

## 🚀 Quick Start

**Run an example notebook:**
1. List available notebooks: `python scripts/setup-workspace.py --list`
2. Copy to workspace: `python scripts/setup-workspace.py --copy risk-scoring/user-risk-score-simple`
3. Update configuration (e.g., `WORKSPACE_NAME`)
4. Upload and run in your Sentinel environment

**Create your own notebook:**
1. Create from template: `python scripts/setup-workspace.py --create my-category/my-analysis`
2. Follow the AI-assisted workflow to design and build your analysis

[View detailed setup guide →](docs/getting-started.md)

## 📖 Documentation

- [Getting Started](docs/getting-started.md) - Complete setup and usage guide
- [Repository Structure](docs/repository-structure.md) - How this repository is organized
- [Notebook Template](templates/) - AI-assisted notebook development workflow

## 🔧 Tools & Scripts

This repository includes helpful scripts:
- [`setup-workspace.py`](scripts/) - Copy notebooks to workspace or create new ones from templates
- [`sanitize-notebook.py`](scripts/) - Remove outputs and credentials before publishing

[View all scripts →](scripts/)

## 📚 Microsoft Sentinel References

- [What is Microsoft Sentinel data lake?](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-overview)
- [Onboard to Microsoft Sentinel data lake](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-onboarding)
- [Notebook examples](https://learn.microsoft.com/en-us/azure/sentinel/datalake/notebook-examples)
- [Microsoft Sentinel Provider class](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-provider-class-reference)
- [Available system tables](https://learn.microsoft.com/en-us/azure/sentinel/datalake/enable-data-connectors)
- [Available workspace tables](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables-index)

---

**Get Started:** [Browse example notebooks](notebooks/) or [create your own with AI assistance](templates/)
