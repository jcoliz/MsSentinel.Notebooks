# Utility Scripts

This directory contains utility scripts for managing notebooks in this repository.

## Scripts

### sanitize-notebook.py
**Status: Implemented**

Sanitizes notebooks before publishing by:
- Removing all cell outputs and execution counts
- Clearing execution metadata
- Replacing actual workspace names with placeholders
- Validating required documentation files exist
- Scanning for common secret patterns

Usage:
```bash
# Sanitize a notebook
python scripts/sanitize-notebook.py workspace/threat-hunting/example-notebook/

# Sanitize and publish
python scripts/sanitize-notebook.py --publish workspace/threat-hunting/example-notebook/

# Dry run
python scripts/sanitize-notebook.py --dry-run workspace/threat-hunting/example-notebook/
```

### setup-workspace.py
**Status: Implemented**

Helps set up workspace environment by copying notebooks and creating new ones from templates.

Usage:
```bash
# List available notebooks
python scripts/setup-workspace.py --list

# Copy existing notebook to workspace
python scripts/setup-workspace.py --copy risk-scoring/user-risk-score-simple

# Create new notebook from template
python scripts/setup-workspace.py --create threat-hunting/new-notebook
```

Features:
- Lists all published notebooks with workspace status
- Copies published notebooks to workspace maintaining directory structure
- Creates new notebooks from templates with placeholder documentation
- Interactive confirmation for overwriting existing notebooks
- Generates starter documentation (README.md, DESIGN.md, IMPLEMENTATION.md)

### validate-notebooks.py
**Status: Implemented**

CI/CD validation script to ensure all published notebooks are properly sanitized.

Usage:
```bash
# Validate all notebooks in notebooks/ directory
python scripts/validate-notebooks.py

# Validate notebooks in a specific subdirectory
python scripts/validate-notebooks.py --directory notebooks/risk-scoring/

# Strict mode: treat warnings as errors
python scripts/validate-notebooks.py --strict

# Verbose output
python scripts/validate-notebooks.py --verbose
```

Features:
- Validates notebooks have no cell outputs or execution counts
- Checks that credentials use template placeholders (not real values)
- Scans for potential secrets (Bearer tokens, GUIDs, Azure URLs)
- Validates WORKSPACE_NAME uses `<YOUR_WORKSPACE_NAME>` placeholder
- Logs presence of optional documentation files in verbose mode (no warnings/errors)
- Supports strict mode where warnings become errors (useful for CI/CD)
- Returns appropriate exit codes for CI/CD integration

Exit Codes:
- 0: All notebooks passed validation
- 1: Validation errors found
- 2: Warnings found (strict mode only)

## Implementation Priority

1. **Phase 1**: [`sanitize-notebook.py`](sanitize-notebook.py) - ✅ **Implemented** - Critical for preventing accidental credential commits
2. **Phase 2**: [`setup-workspace.py`](setup-workspace.py) - ✅ **Implemented** - Streamlines workflow for contributors
3. **Phase 4**: [`validate-notebooks.py`](validate-notebooks.py) - ✅ **Implemented** - Automated validation for CI/CD

## Contributing

When implementing these scripts, ensure they:
- Handle errors gracefully with clear messages
- Provide verbose output for debugging
- Support dry-run mode where applicable
- Include comprehensive help text
