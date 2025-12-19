# Preview Repository Setup Guide

This document describes how to set up and maintain a separate private repository for notebooks that use unreleased Microsoft Sentinel features.

## Overview

**Main Repository** ([`MsSentinel.Notebooks`](https://github.com/jcoliz/MsSentinel.Notebooks))
- Public repository
- Contains notebooks using generally available features
- Production-ready examples

**Preview Repository** (e.g., `MsSentinel.Notebooks.Preview`)
- Private repository
- Contains notebooks using preview/unreleased features
- Controlled access for limited audience
- Notebooks migrate to main repo when features are released

## Why Separate Repository?

**Security & Access Control**
- Private repo with specific collaborators prevents accidental exposure
- No risk of preview features leaking to public
- GitHub's native access control (vs. complex branch protection)

**Workflow Consistency**
- Identical directory structure
- Same scripts and tools work without modification
- Familiar development experience

**Clean Migration Path**
- Independent notebook lifecycle management
- Features release on different timelines
- Simple process: sanitize → copy → PR to main repo

**No Complexity**
- Avoid branch protection rules
- No merge conflict risks
- Clear separation of concerns

## Initial Setup

### 1. Create Private Repository

```bash
# On GitHub, create new repository
Name: MsSentinel.Notebooks.Preview
Visibility: Private
Initialize: Empty (no README, no .gitignore)
```

### 2. Clone and Set Up Structure

```bash
# Clone the new preview repository
git clone https://github.com/YOUR-ORG/MsSentinel.Notebooks.Preview.git
cd MsSentinel.Notebooks.Preview

# Copy core files from main repository
cp ../MsSentinel.Notebooks/.gitignore .
cp -r ../MsSentinel.Notebooks/.roo .
cp -r ../MsSentinel.Notebooks/scripts .
cp -r ../MsSentinel.Notebooks/templates .

# Create directory structure
mkdir -p notebooks docs workspace
touch workspace/.gitkeep

# Create preview-specific README (see next section)
# Create docs/migration-guide.md (see next section)
```

### 3. Add Collaborators

In GitHub repository settings:
1. Go to Settings → Collaborators and teams
2. Add specific users who need access to preview notebooks
3. Grant appropriate permissions (usually "Write" or "Maintain")

### 4. Initial Commit

```bash
git add .
git commit -m "chore: initialize preview repository structure"
git push origin main
```

## Repository Structure

The preview repository mirrors the main repository structure:

```
MsSentinel.Notebooks.Preview/
├── .gitignore                     # Identical to main repo
├── .roo/                          # Identical conventions
│   └── rules/
├── README.md                      # Preview-specific (see template below)
├── docs/
│   ├── README.md                  # Documentation index
│   ├── getting-started.md         # Same as main repo
│   ├── repository-structure.md    # Same as main repo
│   └── migration-guide.md         # Preview-specific migration guide
├── notebooks/                     # Sanitized preview notebooks
│   ├── README.md                  # Catalog of preview notebooks
│   └── <category>/
│       └── <notebook-name>/
│           ├── README.md          # Includes preview feature notes
│           ├── DESIGN.md
│           ├── IMPLEMENTATION.md
│           └── *.ipynb
├── workspace/                     # Local working area (gitignored)
│   ├── README.md
│   ├── .gitkeep
│   └── <category>/
├── scripts/                       # Identical to main repo
│   ├── README.md
│   ├── setup-workspace.py
│   ├── sanitize-notebook.py
│   └── validate-notebooks.py
└── templates/                     # Identical to main repo
    ├── README.md
    ├── notebook-template.ipynb
    └── README-template.md
```

## Preview Repository README Template

Create this as the main `README.md` in the preview repository:

```markdown
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
- [List specific preview features as notebooks are added]
- [Example: Advanced hunting ML models (Preview)]
- [Example: Custom entity enrichment APIs (Private Preview)]

## Using Preview Notebooks

### Prerequisites

1. **Preview Access**: Ensure your Sentinel workspace is enrolled in required preview programs
2. **Feature Flags**: Enable necessary feature flags in Azure Portal
3. **API Access**: Verify you have access to preview APIs

### Getting Started

Same workflow as main repository:

1. List available notebooks: `python scripts/setup-workspace.py --list`
2. Copy to workspace: `python scripts/setup-workspace.py --copy category/notebook-name`
3. Update configuration and run in your Sentinel environment

See [Getting Started Guide](docs/getting-started.md) for detailed instructions.

## 📚 Preview Notebooks

Explore preview notebooks in the [`notebooks/`](notebooks/) directory:

[Update this section as notebooks are added]

## Publishing to Main Repository

When preview features become generally available, notebooks are migrated to the public repository.

See [Migration Guide](docs/migration-guide.md) for the publishing process.

## Documentation

- [Getting Started](docs/getting-started.md) - Setup and usage
- [Migration Guide](docs/migration-guide.md) - Publishing notebooks when features release
- [Repository Structure](docs/repository-structure.md) - How this repository is organized

## 🔧 Tools & Scripts

Same scripts as main repository:
- [`setup-workspace.py`](scripts/) - Copy notebooks or create from templates
- [`sanitize-notebook.py`](scripts/) - Remove outputs and credentials
- [`validate-notebooks.py`](scripts/) - Validation checks

## Microsoft Sentinel References

- [Microsoft Sentinel Preview Features](https://learn.microsoft.com/en-us/azure/sentinel/preview-features)
- [Sentinel Data Lake Overview](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-overview)
- [Public Notebook Examples](https://github.com/jcoliz/MsSentinel.Notebooks)

---

**Access**: This is a private repository. Contact [maintainer] for access requests.
```

## Migration Guide Template

Create `docs/migration-guide.md`:

```markdown
# Migration Guide: Publishing Preview Notebooks

This guide describes the process for migrating notebooks from the preview repository to the public [MsSentinel.Notebooks](https://github.com/jcoliz/MsSentinel.Notebooks) repository when preview features become generally available.

## When to Migrate

Migrate a notebook when:
- ✅ The Microsoft Sentinel feature is **Generally Available (GA)**
- ✅ Feature no longer requires preview enrollment or feature flags
- ✅ Documentation references GA feature versions
- ✅ Notebook has been tested in production environment

## Migration Checklist

### 1. Verify Feature Availability

- [ ] Confirm feature is officially GA (check Microsoft docs)
- [ ] Verify feature works without preview enrollment
- [ ] Check that all APIs used are GA versions
- [ ] Review release notes for breaking changes

### 2. Prepare Notebook for Publication

```bash
cd workspace/category/notebook-name/

# Test notebook in clean environment without preview features
# Ensure all cells run successfully with GA features only
```

- [ ] Test notebook with GA features (no preview flags)
- [ ] Update any preview API endpoints to GA versions
- [ ] Remove preview-specific warnings from documentation
- [ ] Update README to remove preview status notes

### 3. Update Documentation

- [ ] Update README.md - Remove preview warnings
- [ ] Update DESIGN.md - Reference GA feature documentation
- [ ] Update IMPLEMENTATION.md - Note any changes from preview
- [ ] Verify all links point to GA documentation

### 4. Sanitize Notebook

```bash
cd ../../..  # Return to repository root
python scripts/sanitize-notebook.py workspace/category/notebook-name/*.ipynb
```

- [ ] Run sanitize script successfully
- [ ] Verify outputs removed
- [ ] Verify credentials replaced with placeholders
- [ ] Review sanitized notebook in notebooks/ directory

### 5. Validate Documentation

```bash
python scripts/validate-notebooks.py notebooks/category/notebook-name/
```

- [ ] All required documentation files present
- [ ] No validation errors
- [ ] Placeholder format correct

### 6. Copy to Public Repository

```bash
# In public repository (MsSentinel.Notebooks)
cd ../MsSentinel.Notebooks

# Copy sanitized notebook and documentation
mkdir -p notebooks/category/notebook-name
cp ../MsSentinel.Notebooks.Preview/notebooks/category/notebook-name/* \
   notebooks/category/notebook-name/

# Update notebooks catalog
# Edit notebooks/README.md to add entry
```

- [ ] Files copied to public repo
- [ ] Category exists or created appropriately
- [ ] Catalog (notebooks/README.md) updated

### 7. Create Pull Request

```bash
git checkout -b add-notebook-category-name
git add notebooks/category/notebook-name/
git add notebooks/README.md
git commit -m "feat: add [Notebook Name] notebook

Migrate [Notebook Name] from preview repository now that [Feature Name] 
is generally available.

Demonstrates [brief description].
"
git push origin add-notebook-category-name
```

- [ ] Branch created with descriptive name
- [ ] Commit message follows conventional commits format
- [ ] PR created with clear description
- [ ] PR links to feature GA announcement

### 8. Update Preview Repository

After PR is merged to public repository:

```bash
# In preview repository
cd ../MsSentinel.Notebooks.Preview

# Update preview README
# Edit README.md to mark notebook as published

# Optionally archive or remove from preview repo
git mv notebooks/category/notebook-name notebooks/category/notebook-name-ARCHIVED
git commit -m "docs: mark [Notebook Name] as published to main repo"
git push
```

- [ ] Preview README updated
- [ ] Notebook marked as published/archived
- [ ] Team notified of publication

## Migration Example

### Before Migration (Preview Repo)

```python
# In notebook cell
# ⚠️ This notebook uses preview features
# Requires: Azure Sentinel ML Models (Preview)
from azure.sentinel.ml.preview import ThreatDetectionModel  # Preview API
```

```markdown
# In README.md
## Prerequisites
- Microsoft Sentinel workspace with ML Models preview enabled
- Preview enrollment for advanced threat detection
```

### After Migration (Public Repo)

```python
# In notebook cell  
# Uses generally available features
from azure.sentinel.ml import ThreatDetectionModel  # GA API
```

```markdown
# In README.md
## Prerequisites
- Microsoft Sentinel workspace
- Advanced threat detection enabled
```

## Maintaining Links Between Repositories

**In Public Repository README:**
```markdown
## Preview Notebooks

Some notebooks use features still in preview. These are maintained in a
private repository and will be published here when the features are released.

Contact [maintainer] for access to preview notebooks.
```

**In Preview Repository README:**
```markdown
## Published Notebooks

The following notebooks have been published to the [public repository](https://github.com/jcoliz/MsSentinel.Notebooks):
- [Notebook Name] - Published [Date] - [Link to public version]
```

## Troubleshooting

**Preview APIs Changed During GA**
- Update code to use GA API signatures
- Test thoroughly in clean environment
- Document breaking changes in IMPLEMENTATION.md

**Documentation References Preview URLs**
- Update all Microsoft Learn links to GA documentation
- Remove preview-specific configuration steps
- Verify all linked resources are publicly accessible

**Notebook Category Doesn't Exist in Public Repo**
- Create category organically (don't create empty categories)
- Ensure category name follows naming conventions
- Update notebooks/README.md with new category

## Questions?

Contact repository maintainer or open an issue in the preview repository.
```

## Main Repository Documentation Update

Add this section to the main repository's `README.md`:

```markdown
## Preview Notebooks

Some notebooks demonstrate features still in Microsoft Sentinel preview. These are maintained in a private repository and will be published here when the features are generally available.

**For preview access**: Contact [@jcoliz](https://github.com/jcoliz) if you're enrolled in Sentinel preview programs and need access to preview notebooks.

**Feature requests**: If you'd like to see examples for specific preview features, please [open an issue](https://github.com/jcoliz/MsSentinel.Notebooks/issues).
```

## Best Practices

### For Preview Repository Maintainers

1. **Document Preview Requirements**: Clearly state which preview features and enrollments are needed
2. **Keep Scripts Synchronized**: Periodically sync scripts from main repo to ensure consistency
3. **Test Migration Process**: Validate the migration workflow regularly
4. **Track Feature Status**: Monitor Microsoft's release notes for GA announcements
5. **Maintain Access List**: Keep collaborator list current as team members change

### For Notebook Authors

1. **Mark Preview Status Clearly**: Add warnings in notebook cells and documentation
2. **Use Version Comments**: Note which preview API versions are used
3. **Document Breaking Changes**: Track differences from preview to GA
4. **Test Regularly**: Verify notebooks still work as preview features evolve
5. **Plan for Migration**: Write notebooks with eventual publication in mind

## Timeline Expectations

- **Preview Duration**: Features typically remain in preview for 3-12 months
- **Migration Effort**: 1-3 hours per notebook depending on complexity
- **Testing**: Allow extra time for GA feature validation

## Related Documentation

- [Main Repository Structure](https://github.com/jcoliz/MsSentinel.Notebooks/blob/main/docs/repository-structure.md)
- [Getting Started Guide](getting-started.md)
- [Script Documentation](../scripts/README.md)

---

*This guide will be updated as the migration process evolves through practice.*
