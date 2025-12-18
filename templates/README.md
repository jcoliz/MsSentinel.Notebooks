# Notebook Templates

This directory contains templates for creating new notebooks with consistent structure and documentation.

## Templates

### README-template.md
Template for notebook README files (user-facing overview).

### DESIGN-template.md
Template for design documentation (architecture and approach).

### IMPLEMENTATION-template.md
Template for implementation documentation (technical details).

### notebook-template.ipynb
Template for the Jupyter notebook itself with standard structure.

## Usage

These templates are used by the `setup-workspace.py` script when creating new notebooks:

```bash
python scripts/setup-workspace.py --create threat-hunting/new-notebook
```

This will create a new notebook directory in the workspace with all template files copied and ready for customization.

## Customizing Templates

When creating a new notebook:

1. **README.md**: Update with notebook-specific overview, prerequisites, and usage
2. **DESIGN.md**: Document the architecture, data sources, and analytical approach
3. **IMPLEMENTATION.md**: Add implementation notes, known issues, and improvement ideas
4. **notebook.ipynb**: Implement your notebook logic with clear markdown explanations

## Template Structure

Each template includes:
- Placeholder sections to guide content creation
- Examples of what to include
- Consistent formatting and structure
- Links to related documentation

Templates will be implemented in Phase 1 of the migration plan.
