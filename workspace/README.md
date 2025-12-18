# Workspace Directory

This directory is your **private working area** for developing and testing notebooks with real credentials and data. Everything in this directory (except this README) is excluded from version control via `.gitignore`.

## Purpose

The workspace directory allows you to:
- Work with real workspace names and credentials
- Generate and view notebook outputs
- Test notebooks before publishing
- Create job definitions for scheduling
- Keep sensitive data separate from published content

## Structure

The workspace mirrors the 2-level category structure of the `notebooks/` directory:

```
workspace/
├── README.md (this file)
├── threat-hunting/
│   └── notebook-name/
│       ├── README.md
│       ├── DESIGN.md
│       ├── IMPLEMENTATION.md
│       ├── notebook.ipynb
│       └── job-definition.json  # Optional
└── incident-response/
    └── notebook-name/
        └── ...
```

## Usage

### For End Users (Running Notebooks)

1. **Copy a notebook from the published notebooks**:
   ```bash
   # Create category directory if needed
   mkdir -p workspace/threat-hunting
   
   # Copy the notebook
   cp -r notebooks/threat-hunting/example-notebook workspace/threat-hunting/
   ```

2. **Edit the configuration**: Replace placeholder values with your actual workspace details:
   ```python
   WORKSPACE_NAME = "MyActualWorkspace-12345"  # Replace <YOUR_WORKSPACE_NAME>
   ```

3. **Work freely**: Run cells, generate outputs, iterate on the analysis.

### For Contributors (Developing Notebooks)

1. **Create or copy a notebook**:
   ```bash
   # For new notebook, use the setup script:
   python scripts/setup-workspace.py --create threat-hunting/new-notebook
   
   # For updating existing, copy from notebooks/:
   python scripts/setup-workspace.py --copy threat-hunting/existing-notebook
   ```

2. **Develop with real data**: Edit the notebook in your workspace with actual credentials and run it to verify functionality.

3. **Document your work**: Fill out README.md, DESIGN.md, and IMPLEMENTATION.md files.

4. **Sanitize before committing**:
   ```bash
   # This removes outputs and replaces real values with placeholders
   python scripts/sanitize-notebook.py workspace/threat-hunting/new-notebook/
   
   # Or sanitize and publish in one step
   python scripts/sanitize-notebook.py --publish workspace/threat-hunting/new-notebook/
   ```

5. **Review and commit**: Check the sanitized files in `notebooks/` and commit.

## Job Definitions

If you create job definitions for scheduling notebooks, keep them in the workspace directory alongside the notebook:

```
workspace/threat-hunting/example-notebook/
├── notebook.ipynb
└── job-definition.json  # Contains workspace-specific scheduling config
```

Job definitions should **not** be published to the repository as they contain environment-specific details.

## Important Notes

⚠️ **Never commit workspace files to version control** - The `.gitignore` protects you, but be careful with manual git commands.

⚠️ **Always sanitize before publishing** - Use the sanitization script to ensure no sensitive data leaks.

✅ **Feel free to experiment** - This is your sandbox. Break things, try things, learn things!

## Questions?

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed contribution guidelines or [docs/getting-started.md](../docs/getting-started.md) for setup help.
