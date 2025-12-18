# Repository Structure

This document describes the organization and purpose of directories and files in this repository.

## Overview

The repository is organized to separate working notebooks (with real credentials) from published notebooks (sanitized for public sharing), while providing clear documentation and tooling for both contributors and end users.

```
MsSentinel.Notebooks/
├── .gitignore                     # Excludes workspace and sensitive files
├── .roorules                      # Project conventions for AI assistants
├── README.md                      # Main project overview
│
├── docs/                          # User documentation
│   ├── README.md                  # Documentation index
│   ├── getting-started.md         # Quick start guide
│   ├── repository-structure.md    # This document
│   └── wip/                       # Work-in-progress planning docs
│
├── notebooks/                     # Published, sanitized notebooks
│   ├── README.md                  # Notebook catalog
│   └── <category>/                # Categories (created as needed)
│       └── <notebook-name>/       # One directory per notebook
│           ├── README.md          # Overview and usage
│           ├── DESIGN.md          # Architecture and approach
│           ├── IMPLEMENTATION.md  # Technical notes
│           └── *.ipynb            # The sanitized notebook
│
├── workspace/                     # Local working area (gitignored)
│   ├── README.md                  # Usage instructions
│   ├── .gitkeep                   # Preserves directory in repo
│   └── <category>/                # Mirrors notebooks/ structure
│       └── <notebook-name>/       # Development copies with real data
│
├── scripts/                       # Automation and utilities
│   ├── README.md                  # Script documentation
│   ├── setup-workspace.py         # Copies notebooks and creates from templates
│   ├── sanitize-notebook.py       # Removes outputs and credentials
│   └── validate-notebooks.py      # CI/CD validation checks
│
└── templates/                     # Templates for new notebooks
    ├── README.md                  # Template usage guide
    ├── notebook-template.ipynb    # Starter notebook
    └── README-template.md         # Documentation templates
```

## Directory Purposes

### [`docs/`](.)

End-user documentation including setup guides, tutorials, and architectural documentation.

**Key files:**
- [`getting-started.md`](getting-started.md) - First-time user guide
- [`repository-structure.md`](repository-structure.md) - This document

The [`wip/`](wip/) subdirectory contains planning documents and design discussions that are still being refined.

### [`notebooks/`](../notebooks/)

Published, sanitized notebooks ready for public use. All notebooks here:
- Have outputs stripped
- Use placeholder values like `<YOUR_WORKSPACE_NAME>` for configuration
- Include complete documentation (README, DESIGN, IMPLEMENTATION)
- Are organized by category

**Category organization:**
- Categories are created organically as notebooks are added
- Don't create empty category directories
- Suggested categories: `threat-hunting`, `incident-response`, `reporting`, `data-exploration`, `automation`, `risk-scoring`

### [`workspace/`](../workspace/)

**⚠️ Important**: This directory is gitignored - work here never gets committed.

Your private development area where you:
- Work with real workspace names and credentials
- Run notebooks and generate outputs
- Test changes before sanitizing and publishing

The workspace mirrors the category/notebook-name structure of [`notebooks/`](../notebooks/) to maintain organization.

### [`scripts/`](../scripts/)

Automation tools for the repository workflow.

**Key scripts:**
- [`setup-workspace.py`](../scripts/setup-workspace.py) - Copies published notebooks to workspace or creates new notebooks from templates
- [`sanitize-notebook.py`](../scripts/sanitize-notebook.py) - Removes outputs and replaces credentials with placeholders before publishing
- [`validate-notebooks.py`](../scripts/validate-notebooks.py) - Validates notebook structure and documentation (CI/CD integration)

### [`templates/`](../templates/)

Starting points for creating new notebooks, including:
- Notebook template with standard structure
- Documentation templates (README, DESIGN, IMPLEMENTATION)

## Workflow

### For End Users (Using Notebooks)

1. Clone the repository
2. Use [`setup-workspace.py`](../scripts/setup-workspace.py) to copy a notebook to [`workspace/`](../workspace/):
   ```bash
   python scripts/setup-workspace.py --copy risk-scoring/user-risk-score-simple
   ```
3. Update placeholder values with your real workspace details
4. Run and modify the notebook as needed
5. Your workspace changes stay local (gitignored)

### For Contributors (Publishing Notebooks)

1. Create a new notebook in [`workspace/`](../workspace/) using [`setup-workspace.py`](../scripts/setup-workspace.py):
   ```bash
   python scripts/setup-workspace.py --create threat-hunting/new-notebook
   ```
   Or copy an existing one to modify:
   ```bash
   python scripts/setup-workspace.py --copy risk-scoring/user-risk-score-simple
   ```
2. Develop the notebook with real credentials and test thoroughly
3. Create or update documentation files (README.md, DESIGN.md, IMPLEMENTATION.md)
4. Run [`sanitize-notebook.py`](../scripts/sanitize-notebook.py) to remove outputs and credentials:
   ```bash
   python scripts/sanitize-notebook.py --publish workspace/category/notebook-name
   ```
5. Commit and push to the repository

See [`scripts/README.md`](../scripts/README.md) for detailed workflow documentation.

## Configuration Management

**Important**: Sentinel Data Lake notebooks don't support external configuration files. All configuration must be inline in notebooks.

**Published format** (in [`notebooks/`](../notebooks/)):
```python
# Configuration - Update with your workspace name
WORKSPACE_NAME = "<YOUR_WORKSPACE_NAME>"
```

**Working format** (in [`workspace/`](../workspace/)):
```python
# Configuration - Update with your workspace name
WORKSPACE_NAME = "MyCompany-SpecialWorkspace12345"
```

The sanitization script automatically converts between these formats.

## Documentation Requirements

Each notebook requires three documentation files:

1. **README.md** - User-facing overview
   - What the notebook does
   - Prerequisites
   - How to use it
   - Expected results

2. **DESIGN.md** - Architectural documentation
   - Data sources and tables used
   - Query approach and logic
   - Design decisions
   - Limitations

3. **IMPLEMENTATION.md** - Technical details
   - Implementation notes
   - Known issues and workarounds
   - Future improvements
   - Development history

Templates for these files are available in [`templates/`](../templates/).

## Security Model

The repository structure is designed to prevent accidental commits of sensitive data:

- **Separation**: Working area ([`workspace/`](../workspace/)) is completely separate from published area ([`notebooks/`](../notebooks/))
- **Gitignore**: [`workspace/`](../workspace/) is explicitly excluded from version control
- **Sanitization**: Automated script enforces credential removal before publishing
- **Validation**: Script checks for required documentation and placeholder format

**⚠️ Never commit files directly from [`workspace/`](../workspace/)** - always sanitize first.

## Category Guidelines

Categories help organize notebooks by use case. They are created on-demand as notebooks are added.

**Suggested categories:**
- **threat-hunting** - Proactive security investigations
- **incident-response** - Reactive security operations  
- **reporting** - Analytics and dashboards
- **data-exploration** - Data discovery and profiling
- **automation** - Scheduled tasks and maintenance
- **risk-scoring** - Risk assessment and scoring

Don't create categories until you have a notebook to put in them. Categories emerge organically based on actual notebook content.

## Related Documentation

- [`getting-started.md`](getting-started.md) - Quick start guide for new users
- [`notebooks/README.md`](../notebooks/README.md) - Catalog of available notebooks
- [`scripts/README.md`](../scripts/README.md) - Script usage and workflow details
- [`templates/README.md`](../templates/README.md) - Creating new notebooks
- [`.roorules`](../.roorules) - Project conventions

---

**Questions?** Check the [Getting Started](getting-started.md) guide or review the [WIP documents](wip/) for detailed design rationale.
