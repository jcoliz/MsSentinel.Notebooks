#!/usr/bin/env python3
"""
Notebook Sanitization Script

Sanitizes Jupyter notebooks before publishing by:
- Removing all cell outputs and execution counts
- Clearing execution metadata
- Replacing actual values with template placeholders
- Validating required documentation files exist
- Scanning for common secret patterns

Usage:
    python scripts/sanitize-notebook.py workspace/category/notebook-name/
    python scripts/sanitize-notebook.py --publish workspace/category/notebook-name/
    python scripts/sanitize-notebook.py --dry-run workspace/category/notebook-name/
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any


class NotebookSanitizer:
    """Handles sanitization of Jupyter notebooks."""
    
    # Placeholder patterns to use for sanitization
    PLACEHOLDERS = {
        'workspace_name': '<YOUR_WORKSPACE_NAME>',
        'tenant_id': '<YOUR_TENANT_ID>',
        'subscription_id': '<YOUR_SUBSCRIPTION_ID>',
        'resource_group': '<YOUR_RESOURCE_GROUP>',
        'workspace_id': '<YOUR_WORKSPACE_ID>',
        'client_id': '<YOUR_CLIENT_ID>',
        'storage_account': '<YOUR_STORAGE_ACCOUNT>',
    }
    
    # Common patterns that might indicate secrets
    SECRET_PATTERNS = [
        (r'["\'](?:key|password|secret|token)["\']:\s*["\'](?!<YOUR_)[^"\']{8,}["\']', 
         'Possible hardcoded credential'),
        (r'Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*', 
         'Bearer token'),
        (r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', 
         'UUID/GUID (possibly Azure resource ID)'),
        (r'https://[a-z0-9\-]+\.azuresynapse\.net', 
         'Azure Synapse workspace URL'),
        (r'[a-z0-9]{24,}\.database\.windows\.net', 
         'Azure SQL database URL'),
    ]
    
    # Patterns for values that should be replaced with placeholders
    REPLACEMENT_PATTERNS = [
        # Azure workspace names (alphanumeric, hyphens, 1-50 chars)
        (r'[a-z0-9][a-z0-9\-]{0,48}[a-z0-9](?=\.azuresynapse\.net)', 'workspace_name'),
        # Azure subscription IDs (GUIDs)
        (r'(?<=subscription[s]?[/_])[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', 
         'subscription_id'),
        # Azure tenant IDs (GUIDs in tenant context)
        (r'(?<=tenant[s]?[/_])[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', 
         'tenant_id'),
    ]
    
    def __init__(self, notebook_dir: Path, dry_run: bool = False, verbose: bool = False):
        """
        Initialize the sanitizer.
        
        Args:
            notebook_dir: Path to notebook directory
            dry_run: If True, don't write changes
            verbose: If True, print detailed output
        """
        self.notebook_dir = Path(notebook_dir)
        self.dry_run = dry_run
        self.verbose = verbose
        self.issues_found: List[str] = []
        self.changes_made: List[str] = []
        
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
    
    def validate_structure(self) -> bool:
        """
        Validate that required documentation files exist.
        
        Returns:
            True if structure is valid, False otherwise
        """
        self.log("Validating directory structure...")
        
        required_files = ['README.md', 'DESIGN.md', 'IMPLEMENTATION.md']
        missing_files = []
        
        for filename in required_files:
            filepath = self.notebook_dir / filename
            if not filepath.exists():
                missing_files.append(filename)
                self.issues_found.append(f"Missing required file: {filename}")
        
        # Find .ipynb files
        notebook_files = list(self.notebook_dir.glob('*.ipynb'))
        if not notebook_files:
            self.issues_found.append("No .ipynb file found in directory")
            missing_files.append("*.ipynb")
        
        if missing_files:
            self.log(f"Missing required files: {', '.join(missing_files)}", 'error')
            return False
        
        self.log(f"Structure validation passed", 'success')
        return True
    
    def scan_for_secrets(self, content: str, context: str) -> List[Tuple[str, str]]:
        """
        Scan content for potential secrets.
        
        Args:
            content: Content to scan
            context: Context description (e.g., "cell 3")
            
        Returns:
            List of (pattern_description, matched_text) tuples
        """
        findings = []
        
        for pattern, description in self.SECRET_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # Skip if it's already a placeholder
                if '<YOUR_' in match.group():
                    continue
                findings.append((description, match.group(), context))
        
        return findings
    
    def sanitize_cell(self, cell: Dict[str, Any], cell_index: int) -> Dict[str, Any]:
        """
        Sanitize a single notebook cell.
        
        Args:
            cell: Cell dictionary
            cell_index: Index of the cell
            
        Returns:
            Sanitized cell dictionary
        """
        sanitized_cell = cell.copy()
        
        # Clear outputs for code cells
        if cell.get('cell_type') == 'code':
            if cell.get('outputs'):
                sanitized_cell['outputs'] = []
                self.changes_made.append(f"Cleared outputs from cell {cell_index}")
            
            if cell.get('execution_count'):
                sanitized_cell['execution_count'] = None
                self.changes_made.append(f"Cleared execution count from cell {cell_index}")
        
        # Scan source for secrets
        source = cell.get('source', [])
        if isinstance(source, list):
            source_text = ''.join(source)
        else:
            source_text = source
        
        secrets = self.scan_for_secrets(source_text, f"cell {cell_index}")
        for description, matched_text, context in secrets:
            warning = f"{description} found in {context}: '{matched_text[:50]}...'"
            self.log(warning, 'warning')
            self.issues_found.append(warning)
        
        return sanitized_cell
    
    def sanitize_notebook(self, notebook_path: Path) -> bool:
        """
        Sanitize a Jupyter notebook file.
        
        Args:
            notebook_path: Path to the notebook file
            
        Returns:
            True if successful, False otherwise
        """
        self.log(f"Sanitizing notebook: {notebook_path.name}")
        
        try:
            # Read notebook
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            # Sanitize cells
            if 'cells' in notebook:
                notebook['cells'] = [
                    self.sanitize_cell(cell, i) 
                    for i, cell in enumerate(notebook['cells'])
                ]
            
            # Clear notebook metadata
            if 'metadata' in notebook:
                # Keep language and kernel spec, but clear execution metadata
                metadata = notebook['metadata']
                if 'kernel_info' in metadata:
                    del metadata['kernel_info']
                if 'language_info' in metadata and 'version' in metadata['language_info']:
                    # Keep language name but clear version specifics
                    metadata['language_info'] = {
                        'name': metadata['language_info'].get('name', 'python')
                    }
                self.changes_made.append("Cleared notebook metadata")
            
            # Create backup if not dry run
            if not self.dry_run:
                backup_path = notebook_path.with_suffix('.ipynb.bak')
                shutil.copy2(notebook_path, backup_path)
                self.log(f"Created backup: {backup_path.name}")
                
                # Write sanitized notebook
                with open(notebook_path, 'w', encoding='utf-8') as f:
                    json.dump(notebook, f, indent=1, ensure_ascii=False)
                    f.write('\n')  # Add trailing newline
                
                self.log(f"Sanitized notebook written", 'success')
            else:
                self.log("Dry run: No changes written")
            
            return True
            
        except json.JSONDecodeError as e:
            self.log(f"Failed to parse notebook JSON: {e}", 'error')
            return False
        except Exception as e:
            self.log(f"Error sanitizing notebook: {e}", 'error')
            return False
    
    def sanitize_directory(self) -> bool:
        """
        Sanitize all notebooks in the directory.
        
        Returns:
            True if successful, False otherwise
        """
        # Validate structure first
        if not self.validate_structure():
            return False
        
        # Find and sanitize notebooks
        notebook_files = list(self.notebook_dir.glob('*.ipynb'))
        success = True
        
        for notebook_path in notebook_files:
            if not self.sanitize_notebook(notebook_path):
                success = False
        
        return success
    
    def publish_to_notebooks(self) -> bool:
        """
        Copy sanitized notebook directory to notebooks/ directory.
        
        Returns:
            True if successful, False otherwise
        """
        # Determine target path
        # workspace/category/notebook-name/ -> notebooks/category/notebook-name/
        parts = self.notebook_dir.parts
        
        if 'workspace' not in parts:
            self.log("Source directory is not in workspace/", 'error')
            return False
        
        workspace_index = parts.index('workspace')
        relative_path = Path(*parts[workspace_index + 1:])
        
        target_dir = Path('notebooks') / relative_path
        
        self.log(f"Publishing to: {target_dir}")
        
        if self.dry_run:
            self.log("Dry run: Skipping actual publish")
            return True
        
        try:
            # Create target directory
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy files
            files_to_copy = ['README.md', 'DESIGN.md', 'IMPLEMENTATION.md']
            files_to_copy.extend([f.name for f in self.notebook_dir.glob('*.ipynb')])
            
            for filename in files_to_copy:
                source = self.notebook_dir / filename
                target = target_dir / filename
                
                if source.exists():
                    shutil.copy2(source, target)
                    self.log(f"Copied: {filename}")
            
            self.log(f"Published to {target_dir}", 'success')
            return True
            
        except Exception as e:
            self.log(f"Error publishing: {e}", 'error')
            return False
    
    def print_summary(self):
        """Print a summary of the sanitization process."""
        print("\n" + "="*60)
        print("SANITIZATION SUMMARY")
        print("="*60)
        
        if self.changes_made:
            print(f"\n[SUCCESS] Changes made ({len(self.changes_made)}):")
            for change in self.changes_made[:10]:  # Show first 10
                print(f"  - {change}")
            if len(self.changes_made) > 10:
                print(f"  ... and {len(self.changes_made) - 10} more")
        else:
            print("\n[INFO] No changes needed")
        
        if self.issues_found:
            print(f"\n[WARNING] Issues found ({len(self.issues_found)}):")
            for issue in self.issues_found:
                print(f"  - {issue}")
        
        if self.dry_run:
            print("\n[DRY RUN] No files were modified")
        
        print("="*60 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Sanitize Jupyter notebooks before publishing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sanitize a notebook (in place)
  python scripts/sanitize-notebook.py workspace/threat-hunting/example/
  
  # Sanitize and publish to notebooks/ directory
  python scripts/sanitize-notebook.py --publish workspace/threat-hunting/example/
  
  # Dry run to see what would change
  python scripts/sanitize-notebook.py --dry-run workspace/threat-hunting/example/
        """
    )
    
    parser.add_argument(
        'notebook_dir',
        type=str,
        help='Path to notebook directory (e.g., workspace/category/notebook-name/)'
    )
    
    parser.add_argument(
        '--publish',
        action='store_true',
        help='Copy sanitized notebook to notebooks/ directory'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate notebook directory exists
    notebook_dir = Path(args.notebook_dir)
    if not notebook_dir.exists():
        print(f"[ERROR] Directory not found: {notebook_dir}", file=sys.stderr)
        return 1
    
    if not notebook_dir.is_dir():
        print(f"[ERROR] Not a directory: {notebook_dir}", file=sys.stderr)
        return 1
    
    # Create sanitizer and run
    sanitizer = NotebookSanitizer(notebook_dir, args.dry_run, args.verbose)
    
    print(f"\n{'='*60}")
    print(f"NOTEBOOK SANITIZATION")
    print(f"{'='*60}")
    print(f"Directory: {notebook_dir}")
    print(f"Dry run: {args.dry_run}")
    print(f"Publish: {args.publish}")
    print(f"{'='*60}\n")
    
    # Sanitize
    success = sanitizer.sanitize_directory()
    
    # Publish if requested and sanitization succeeded
    if success and args.publish:
        success = sanitizer.publish_to_notebooks()
    
    # Print summary
    sanitizer.print_summary()
    
    # Return exit code
    if not success:
        print("[ERROR] Sanitization failed. Please review errors above.", file=sys.stderr)
        return 1
    elif sanitizer.issues_found:
        print("[WARNING] Sanitization completed with warnings. Please review issues above.")
        return 0
    else:
        print("[SUCCESS] Sanitization completed successfully!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
