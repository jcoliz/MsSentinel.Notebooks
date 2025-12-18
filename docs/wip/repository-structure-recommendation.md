# Repository Structure Recommendation

## Executive Summary

This document recommends a repository structure for the Microsoft Sentinel Data Lake Notebooks project that addresses the key challenges of:
1. Separating working notebooks from published notebooks
2. Managing configuration placeholders for public sharing
3. Organizing multiple notebooks with full documentation
4. Providing a clear path for contributors and end users

## Recommended Structure

```
MsSentinel.Notebooks/
├── .gitignore                     # Exclude working notebooks and outputs
├── README.md                      # Main project README
├── LICENSE                        # Project license
├── CONTRIBUTING.md                # Contribution guidelines
│
├── docs/                          # End-user documentation
│   ├── README.md
│   ├── getting-started.md
│   ├── setup-guide.md
│   └── wip/                       # Work in progress documentation
│
├── notebooks/                     # Published notebook examples
│   └── README.md                  # Index and category guidelines
│
│   # Categories will be created as needed when notebooks are added:
│   # ├── threat-hunting/
│   # │   └── <notebook-name>/
│   # │       ├── README.md
│   # │       ├── DESIGN.md
│   # │       ├── IMPLEMENTATION.md
│   # │       └── notebook.ipynb
│   #
│   # ├── incident-response/
│   # ├── reporting/
│   # ├── data-exploration/
│   # └── automation/
│
├── workspace/                     # Local working area (gitignored)
│   ├── README.md                  # Instructions for workspace usage
│   └── .gitkeep                   # Keep directory in repo
│
│   # Workspace mirrors the 2-level hierarchy of notebooks/:
│   # ├── threat-hunting/
│   # │   └── compromised-accounts/
│   # │       ├── README.md
│   # │       ├── DESIGN.md
│   # │       ├── IMPLEMENTATION.md
│   # │       ├── notebook.ipynb
│   # │       └── job-definition.json  # Optional: workspace-specific scheduling
│   # └── incident-response/
│   #     └── initial-triage/
│   #         └── ...
│
├── scripts/                       # Utility scripts
│   ├── sanitize-notebook.py       # Remove outputs and restore placeholders
│   ├── setup-workspace.py         # Copy notebooks to workspace
│   └── validate-notebooks.py      # CI/CD validation
│
└── templates/                     # Templates for new notebooks
    ├── README-template.md
    ├── DESIGN-template.md
    ├── IMPLEMENTATION-template.md
    └── notebook-template.ipynb
```

## Key Design Decisions

### 1. Workspace Directory for Active Development

**Solution**: Create a [`workspace/`](../../workspace/) directory that is excluded from version control via [`.gitignore`](../../.gitignore).

**Structure**: The workspace mirrors the full 2-level hierarchy (category/notebook-name/) of the published notebooks structure.

```
workspace/
├── README.md
├── threat-hunting/
│   └── compromised-accounts/
│       ├── README.md
│       ├── DESIGN.md
│       ├── IMPLEMENTATION.md
│       ├── notebook.ipynb
│       └── job-definition.json      # Optional: workspace-specific scheduling
└── incident-response/
    └── initial-triage/
        └── ...
```

**Workflow**:
- Contributors copy notebooks from [`notebooks/`](../../notebooks/) to [`workspace/`](../../workspace/) maintaining full path
- Work with real workspace names and credentials in [`workspace/`](../../workspace/)
- Run notebooks freely with outputs in [`workspace/`](../../workspace/)
- Optionally create job definitions for scheduling (stays in workspace, not published)
- Use sanitize script before copying back to [`notebooks/`](../../notebooks/)

**Job Definitions**:
- Job definitions are workspace-specific and contain environment details
- Should remain in workspace directory alongside the notebook
- Not published to the repository (gitignored with workspace)

**Benefits**:
- Clear separation between working and published notebooks
- No risk of accidentally committing sensitive data
- Preserves category context during development
- Simplifies sanitization script (maintains relative paths)
- Prevents name collisions across categories
- Simple mental model: workspace = private, notebooks = public

### 2. Category-Based Notebook Organization

**Solution**: Organize notebooks by use case category under [`notebooks/`](../../notebooks/).

**Policy**: Categories are created organically as notebooks are added. Don't create empty category directories in advance.

**Rationale**:
- With 10+ notebooks planned, flat structure becomes unwieldy
- Categories help users find relevant examples quickly
- Follows patterns from other successful notebook repositories
- Creating categories on-demand keeps structure clean and prevents empty directories

**Suggested Categories** (create as needed):
- `threat-hunting/` - Proactive security investigations
- `incident-response/` - Reactive security operations
- `reporting/` - Analytics and dashboards
- `data-exploration/` - Data discovery and profiling
- `automation/` - Scheduled tasks and maintenance

### 3. Consistent Documentation Structure

**Solution**: Each notebook gets its own directory with standardized documentation files.

**Files per notebook** (all required):
- `README.md` - Overview, prerequisites, usage instructions
- `DESIGN.md` - Architecture, data sources, approach
- `IMPLEMENTATION.md` - Implementation notes, gotchas, future improvements
- `notebook.ipynb` - The sanitized notebook

**Rationale**:
- Each file serves a distinct purpose and can become quite long
- Separation keeps documentation maintainable and focused
- README is user-facing, DESIGN is architectural, IMPLEMENTATION is technical
- Self-contained units that can be copied/referenced independently

**Benefits**:
- Easy to navigate and understand each example
- Documentation can grow without becoming unwieldy
- Clear separation of concerns for different audiences

### 4. Sanitization Script Approach

**Solution**: Use a Python script to sanitize notebooks before publishing.

**Script responsibilities**:
1. Strip all cell outputs and execution metadata
2. Replace actual workspace names with placeholders
3. Validate notebook structure
4. Optionally copy to [`notebooks/`](../../notebooks/) directory

**Benefits**:
- Automated and repeatable process
- Reduces human error
- Can be integrated into pre-commit hooks or CI/CD

## Detailed Workflow Examples

### For End Users Cloning the Repository

```bash
# 1. Clone the repository
git clone https://github.com/yourorg/MsSentinel.Notebooks.git
cd MsSentinel.Notebooks

# 2. Copy a notebook to workspace (preserving category structure)
cp -r notebooks/threat-hunting/compromised-accounts workspace/threat-hunting/

# 3. Edit workspace configuration
# Update WORKSPACE_NAME = "<YOUR_WORKSPACE_NAME>" with your actual workspace

# 4. Work with the notebook
# Open workspace/threat-hunting/compromised-accounts/notebook.ipynb
# Run cells, generate outputs, iterate
```

### For Contributors Developing New Notebooks

```bash
# 1. Create new notebook from template
python scripts/setup-workspace.py --create threat-hunting/new-notebook

# 2. Develop in workspace
# Work in workspace/new-notebook/ with real credentials

# 3. Document your work
# Fill out DESIGN.md, IMPLEMENTATION.md, README.md

# 4. Sanitize before committing
python scripts/sanitize-notebook.py workspace/new-notebook/

# 5. Review and commit
git add notebooks/threat-hunting/new-notebook/
git commit -m "Add new notebook for threat hunting"
```

### For Contributors Updating Existing Notebooks

```bash
# 1. Copy published notebook to workspace (maintains category structure)
python scripts/setup-workspace.py --copy threat-hunting/compromised-accounts

# 2. Make changes in workspace
# Edit workspace/threat-hunting/compromised-accounts/notebook.ipynb

# 3. Sanitize before publishing
python scripts/sanitize-notebook.py workspace/threat-hunting/compromised-accounts/

# 4. Commit changes
git add notebooks/threat-hunting/compromised-accounts/
git commit -m "Update compromised accounts notebook"
```

## Configuration Placeholder Strategy

### Template Variables (Recommended Approach)

Use consistent placeholder syntax that's easy to find and replace:

```python
# Configuration - Update with your environment details
WORKSPACE_NAME = "<YOUR_WORKSPACE_NAME>"
TENANT_ID = "<YOUR_TENANT_ID>"
SUBSCRIPTION_ID = "<YOUR_SUBSCRIPTION_ID>"
```

**Why inline configuration is required**:
- Sentinel Data Lake notebooks execute remotely in Azure Spark environment
- Config files don't get uploaded with the notebook
- All configuration must be embedded directly in the notebook cells

**Sanitization script behavior**:
- Searches for actual values using regex patterns
- Replaces with template placeholders
- Validates all placeholders are present before allowing publish

## .gitignore Configuration

```gitignore
# Workspace directory - contains working notebooks with sensitive data
workspace/*
!workspace/README.md
!workspace/.gitkeep

# Jupyter Notebook artifacts
.ipynb_checkpoints/
**/.ipynb_checkpoints/

# Python artifacts
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual environments
venv/
env/
ENV/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.bak
*~
```

## Sanitization Script Requirements

The [`sanitize-notebook.py`](../../scripts/sanitize-notebook.py) script should:

1. **Clear outputs**: Remove all cell outputs and execution counts
2. **Clear metadata**: Remove execution timing and kernel metadata
3. **Replace placeholders**: Convert actual values to template format
4. **Validate structure**: Ensure required documentation files exist
5. **Check for secrets**: Scan for common secret patterns
6. **Generate report**: Show what was changed
7. **Create backup**: Save original before sanitizing

Example usage:
```bash
# Sanitize a single notebook
python scripts/sanitize-notebook.py workspace/threat-hunting/compromised-accounts/

# Sanitize and copy to notebooks directory
python scripts/sanitize-notebook.py --publish workspace/threat-hunting/compromised-accounts/

# Dry run to see what would change
python scripts/sanitize-notebook.py --dry-run workspace/threat-hunting/compromised-accounts/
```

## Migration Path

### Phase 1: Foundation & Safety
1. Create base directory structure (notebooks/, workspace/, scripts/, templates/)
2. Implement [`.gitignore`](../../.gitignore) - **Critical for preventing accidental commits**
3. Develop basic sanitization script - **Priority: Must be available before creating any notebooks**
4. Add [`workspace/README.md`](../../workspace/README.md) with usage instructions
5. Create [`notebooks/README.md`](../../notebooks/README.md) documenting category policy
6. Create templates for notebook documentation

### Phase 2: First Content
1. Create setup script for workspace management
2. Develop first notebook in workspace with full documentation
3. Test sanitization workflow thoroughly
4. Publish first notebook (creates first category directory)
5. Update main README with example

### Phase 3: Content Expansion
1. Add more notebooks using established workflow
2. Create new categories as needed
3. Document lessons learned in CONTRIBUTING.md

### Phase 4: Automation & Polish
1. Add CI/CD validation (verify all notebooks are sanitized)
2. Finalize CONTRIBUTING.md guide
3. Enhance sanitization script with secret detection
4. Add pre-commit hooks to prevent accidental commits
5. Add automated testing for notebooks

## Alternative Approaches Considered

### Alternative 1: Git Branches

**Approach**: Use a `working` branch for development, `main` for published content.

**Rejected because**:
- Complex merge conflicts with notebook JSON
- Doesn't prevent accidental commits of sensitive data
- Harder to maintain with multiple contributors

### Alternative 2: Separate Repositories

**Approach**: Private repo for development, public repo for published notebooks.

**Rejected because**:
- Increased complexity for contributors
- Synchronization challenges
- Doesn't align with single public repo goal

### Alternative 3: Notebook Subdirectories

**Approach**: Put working notebooks in `notebooks/*/working/` subdirectories.

**Rejected because**:
- Risk of accidentally committing working notebooks
- Clutters published structure
- Harder to gitignore selectively

## Recommended Documentation Updates

Create these additional documents:

1. **CONTRIBUTING.md**: Guide for contributors covering:
   - How to set up workspace
   - How to use sanitization scripts
   - Documentation requirements
   - PR guidelines

2. **docs/getting-started.md**: End-user guide covering:
   - Prerequisites (Azure account, Sentinel setup)
   - How to clone and configure
   - How to run first notebook
   - Troubleshooting

3. **docs/setup-guide.md**: Detailed setup covering:
   - Azure Sentinel data lake setup
   - Spark environment configuration
   - Authentication methods
   - Common issues

4. **notebooks/README.md**: Notebook catalog with:
   - Table of all notebooks with descriptions
   - Category explanations
   - Difficulty levels
   - Prerequisites per notebook

## Next Steps

Once approved, implementation would include:

1. Create directory structure and [`.gitignore`](../../.gitignore)
2. Develop sanitization script
3. Create documentation templates
4. Write CONTRIBUTING.md and setup guides
5. Migrate any existing content
6. Test complete workflow with sample notebook

This structure balances the needs of public sharing, contributor workflows, and end-user simplicity while scaling to 10+ fully documented notebooks.
