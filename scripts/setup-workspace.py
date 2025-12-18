#!/usr/bin/env python3
"""
Workspace Setup Script

Helps set up workspace environment by:
- Copying published notebooks to workspace for local development
- Creating new notebooks from templates with proper structure

Usage:
    python scripts/setup-workspace.py --copy risk-scoring/user-risk-score-simple
    python scripts/setup-workspace.py --create threat-hunting/new-notebook
    python scripts/setup-workspace.py --list
"""

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Optional


class WorkspaceSetup:
    """Handles workspace setup operations."""
    
    def __init__(self, verbose: bool = False, force: bool = False):
        """
        Initialize the workspace setup handler.
        
        Args:
            verbose: If True, print detailed output
            force: If True, skip confirmation prompts
        """
        self.verbose = verbose
        self.force = force
        self.workspace_dir = Path('workspace')
        self.notebooks_dir = Path('notebooks')
        self.templates_dir = Path('templates')
        
    def log(self, message: str, level: str = 'info'):
        """Log a message based on verbosity settings."""
        if level == 'error':
            print(f"[ERROR] {message}", file=sys.stderr)
        elif level == 'warning':
            print(f"[WARNING] {message}")
        elif level == 'success':
            print(f"[SUCCESS] {message}")
        elif self.verbose or level == 'info':
            print(f"[INFO] {message}")
    
    def validate_paths(self) -> bool:
        """
        Validate that required directories exist.
        
        Returns:
            True if valid, False otherwise
        """
        if not self.workspace_dir.exists():
            self.log(f"Workspace directory not found: {self.workspace_dir}", 'error')
            return False
        
        if not self.notebooks_dir.exists():
            self.log(f"Notebooks directory not found: {self.notebooks_dir}", 'error')
            return False
        
        if not self.templates_dir.exists():
            self.log(f"Templates directory not found: {self.templates_dir}", 'error')
            return False
        
        return True
    
    def list_available_notebooks(self):
        """List all published notebooks available to copy."""
        print("\n" + "="*60)
        print("AVAILABLE PUBLISHED NOTEBOOKS")
        print("="*60 + "\n")
        
        # Find all notebook directories (contain .ipynb files)
        notebook_paths = []
        
        for category_dir in sorted(self.notebooks_dir.iterdir()):
            if category_dir.is_dir() and category_dir.name != '.git':
                for notebook_dir in sorted(category_dir.iterdir()):
                    if notebook_dir.is_dir():
                        # Check if it contains a notebook
                        if list(notebook_dir.glob('*.ipynb')):
                            relative_path = notebook_dir.relative_to(self.notebooks_dir)
                            notebook_paths.append(relative_path)
        
        if not notebook_paths:
            print("No published notebooks found.\n")
            return
        
        for path in notebook_paths:
            # Check if already in workspace
            workspace_path = self.workspace_dir / path
            status = "[in workspace]" if workspace_path.exists() else ""
            print(f"  {path}  {status}")
        
        print(f"\nTotal: {len(notebook_paths)} notebook(s)")
        print("\nUsage:")
        print("  python scripts/setup-workspace.py --copy <category>/<notebook-name>")
        print("="*60 + "\n")
    
    def copy_notebook_to_workspace(self, notebook_path: str) -> bool:
        """
        Copy a published notebook to workspace for development.
        
        Args:
            notebook_path: Relative path like "category/notebook-name"
            
        Returns:
            True if successful, False otherwise
        """
        # Validate source exists
        source_dir = self.notebooks_dir / notebook_path
        if not source_dir.exists():
            self.log(f"Source notebook not found: {source_dir}", 'error')
            self.log("Run with --list to see available notebooks", 'info')
            return False
        
        if not source_dir.is_dir():
            self.log(f"Source is not a directory: {source_dir}", 'error')
            return False
        
        # Check if it contains a notebook
        notebook_files = list(source_dir.glob('*.ipynb'))
        if not notebook_files:
            self.log(f"No notebook file found in: {source_dir}", 'error')
            return False
        
        # Determine target location (mirrors structure)
        target_dir = self.workspace_dir / notebook_path
        
        # Check if already exists
        if target_dir.exists():
            self.log(f"Target already exists: {target_dir}", 'warning')
            if not self.force:
                response = input("Overwrite? [y/N]: ").strip().lower()
                if response not in ('y', 'yes'):
                    self.log("Operation cancelled", 'info')
                    return False
            else:
                self.log("Force mode: overwriting existing directory", 'info')
            self.log("Removing existing directory...", 'info')
            shutil.rmtree(target_dir)
        
        try:
            # Create target directory
            target_dir.mkdir(parents=True, exist_ok=True)
            self.log(f"Created directory: {target_dir}")
            
            # Copy all files from source
            files_copied = []
            for item in source_dir.iterdir():
                if item.is_file():
                    target_file = target_dir / item.name
                    shutil.copy2(item, target_file)
                    files_copied.append(item.name)
                    self.log(f"Copied: {item.name}")
            
            self.log(f"\nSuccessfully copied {len(files_copied)} file(s) to workspace", 'success')
            self.log(f"Location: {target_dir}", 'success')
            self.log("\nNext steps:", 'info')
            self.log("1. Open the notebook in your workspace directory", 'info')
            self.log("2. Update configuration placeholders with your values", 'info')
            self.log("3. Run and modify the notebook as needed", 'info')
            self.log("4. Use sanitize-notebook.py before publishing changes", 'info')
            
            return True
            
        except Exception as e:
            self.log(f"Error copying notebook: {e}", 'error')
            return False
    
    def create_new_notebook(self, notebook_path: str) -> bool:
        """
        Create a new notebook from templates.
        
        Args:
            notebook_path: Relative path like "category/notebook-name"
            
        Returns:
            True if successful, False otherwise
        """
        # Validate path format
        path_parts = Path(notebook_path).parts
        if len(path_parts) != 2:
            self.log("Notebook path must be in format: category/notebook-name", 'error')
            return False
        
        category, notebook_name = path_parts
        
        # Determine target location
        target_dir = self.workspace_dir / notebook_path
        
        # Check if already exists
        if target_dir.exists():
            self.log(f"Target already exists: {target_dir}", 'error')
            self.log("Choose a different name or remove the existing directory", 'info')
            return False
        
        try:
            # Create target directory
            target_dir.mkdir(parents=True, exist_ok=True)
            self.log(f"Created directory: {target_dir}")
            
            # Copy notebook template
            template_notebook = self.templates_dir / 'notebook-template.ipynb'
            if template_notebook.exists():
                target_notebook = target_dir / f"{notebook_name}.ipynb"
                
                # Read template and update title
                with open(template_notebook, 'r', encoding='utf-8') as f:
                    notebook_data = json.load(f)
                
                # Update first cell title if it exists
                if notebook_data.get('cells') and len(notebook_data['cells']) > 0:
                    first_cell = notebook_data['cells'][0]
                    if first_cell.get('cell_type') == 'markdown':
                        # Replace template title with notebook name
                        source = first_cell.get('source', [])
                        if isinstance(source, list) and len(source) > 0:
                            # Update title (first line is typically "# Template Title")
                            title = notebook_name.replace('-', ' ').replace('_', ' ').title()
                            source[0] = f"# {title}\n"
                            first_cell['source'] = source
                
                # Write updated notebook
                with open(target_notebook, 'w', encoding='utf-8') as f:
                    json.dump(notebook_data, f, indent=1, ensure_ascii=False)
                    f.write('\n')
                
                self.log(f"Created notebook: {target_notebook.name}")
            else:
                self.log("Warning: notebook template not found, skipping", 'warning')
            
            # Create placeholder documentation files
            docs = {
                'README.md': f"""# {notebook_name.replace('-', ' ').replace('_', ' ').title()}

## Overview

[Brief description of what this notebook does]

## Prerequisites

- Microsoft Sentinel workspace with data lake enabled
- Appropriate permissions to query Sentinel tables
- Required data sources:
  - [List data sources needed]

## Usage

1. Open the notebook in your Spark environment
2. Update the configuration section with your workspace details
3. Run all cells sequentially
4. Review the results

## Expected Results

[Describe what outputs/visualizations to expect]

## Related Notebooks

- [Link to related notebooks if any]

## References

- [Link to relevant documentation]
""",
                'DESIGN.md': f"""# Design Document: {notebook_name.replace('-', ' ').replace('_', ' ').title()}

## Purpose

[What problem does this notebook solve?]

## Data Sources

### Tables Used

1. **TableName**
   - Fields: field1, field2, field3
   - Time range: [typical range]
   - Purpose: [why this table]

## Analysis Approach

### Step 1: [First Step]

[Description of what happens in this step]

### Step 2: [Second Step]

[Description of what happens in this step]

## Output Schema

| Column | Type | Description |
|--------|------|-------------|
| column1 | string | [description] |
| column2 | int | [description] |

## Assumptions

- [List any assumptions made]

## Limitations

- [List any known limitations]
""",
                'IMPLEMENTATION.md': f"""# Implementation Notes: {notebook_name.replace('-', ' ').replace('_', ' ').title()}

## Technical Details

### Libraries Used

- pyspark.sql
- [Other libraries]

### Performance Considerations

- [Notes about query performance]
- [Data volume considerations]

## Known Issues

- [List any known issues or workarounds]

## Testing

### Test Cases

1. [Test case description]
   - Expected: [expected result]
   - Actual: [actual result]

## Future Improvements

- [ ] [Improvement idea 1]
- [ ] [Improvement idea 2]

## Change Log

### Version 1.0
- Initial implementation
"""
            }
            
            for filename, content in docs.items():
                doc_file = target_dir / filename
                doc_file.write_text(content, encoding='utf-8')
                self.log(f"Created: {filename}")
            
            self.log(f"\nSuccessfully created new notebook structure", 'success')
            self.log(f"Location: {target_dir}", 'success')
            self.log("\nNext steps:", 'info')
            self.log("1. Fill out the documentation files (README.md, DESIGN.md, IMPLEMENTATION.md)", 'info')
            self.log("2. Open the notebook and implement your analysis", 'info')
            self.log("3. Test thoroughly with real data", 'info')
            self.log("4. Use sanitize-notebook.py --publish before sharing", 'info')
            
            return True
            
        except Exception as e:
            self.log(f"Error creating notebook: {e}", 'error')
            # Clean up partial creation
            if target_dir.exists():
                shutil.rmtree(target_dir)
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Setup workspace for notebook development',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List available published notebooks
  python scripts/setup-workspace.py --list
  
  # Copy a published notebook to workspace
  python scripts/setup-workspace.py --copy risk-scoring/user-risk-score-simple
  
  # Create a new notebook from template
  python scripts/setup-workspace.py --create threat-hunting/suspicious-logins
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument(
        '--list',
        action='store_true',
        help='List all available published notebooks'
    )
    
    group.add_argument(
        '--copy',
        type=str,
        metavar='PATH',
        help='Copy published notebook to workspace (e.g., category/notebook-name)'
    )
    
    group.add_argument(
        '--create',
        type=str,
        metavar='PATH',
        help='Create new notebook from template (e.g., category/notebook-name)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '-f', '--force',
        action='store_true',
        help='Force overwrite without confirmation'
    )
    
    args = parser.parse_args()
    
    # Create setup handler
    setup = WorkspaceSetup(verbose=args.verbose, force=args.force)
    
    # Validate paths
    if not setup.validate_paths():
        return 1
    
    # Execute requested operation
    if args.list:
        setup.list_available_notebooks()
        return 0
    
    elif args.copy:
        print(f"\n{'='*60}")
        print(f"COPYING NOTEBOOK TO WORKSPACE")
        print(f"{'='*60}")
        print(f"Source: notebooks/{args.copy}")
        print(f"Target: workspace/{args.copy}")
        print(f"{'='*60}\n")
        
        success = setup.copy_notebook_to_workspace(args.copy)
        
        if not success:
            print("\n[ERROR] Failed to copy notebook to workspace.", file=sys.stderr)
            return 1
        
        print("\n[SUCCESS] Notebook copied to workspace successfully!")
        return 0
    
    elif args.create:
        print(f"\n{'='*60}")
        print(f"CREATING NEW NOTEBOOK")
        print(f"{'='*60}")
        print(f"Location: workspace/{args.create}")
        print(f"{'='*60}\n")
        
        success = setup.create_new_notebook(args.create)
        
        if not success:
            print("\n[ERROR] Failed to create new notebook.", file=sys.stderr)
            return 1
        
        print("\n[SUCCESS] New notebook created successfully!")
        return 0
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
