#!/usr/bin/env python3
"""
Notebook Validation Script

CI/CD validation script to ensure all published notebooks are properly sanitized.

Validates that notebooks in the notebooks/ directory:
- Have no cell outputs
- Have no execution counts
- Use template placeholders instead of real credentials
- Don't contain potential secrets
- Have required documentation files (optional)

Usage:
    python scripts/validate-notebooks.py
    python scripts/validate-notebooks.py --directory notebooks/risk-scoring/
    python scripts/validate-notebooks.py --strict
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional


class NotebookValidator:
    """Validates that notebooks are properly sanitized."""
    
    # Expected placeholder patterns
    EXPECTED_PLACEHOLDERS = [
        '<YOUR_WORKSPACE_NAME>',
        '<YOUR_TENANT_ID>',
        '<YOUR_SUBSCRIPTION_ID>',
        '<YOUR_RESOURCE_GROUP>',
        '<YOUR_WORKSPACE_ID>',
        '<YOUR_CLIENT_ID>',
        '<YOUR_STORAGE_ACCOUNT>',
    ]
    
    # Patterns that indicate secrets (should NOT be present)
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
    
    # Pattern to detect non-placeholder workspace names
    WORKSPACE_NAME_PATTERN = r'WORKSPACE_NAME\s*=\s*["\']([^"\']+)["\']'
    
    def __init__(self, base_dir: Path, strict: bool = False, verbose: bool = False):
        """
        Initialize the validator.
        
        Args:
            base_dir: Base directory to search for notebooks
            strict: If True, treat warnings as errors
            verbose: If True, print detailed output
        """
        self.base_dir = Path(base_dir)
        self.strict = strict
        self.verbose = verbose
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.validated_count = 0
        
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
    
    def scan_for_secrets(self, content: str, context: str) -> List[Tuple[str, str, str]]:
        """
        Scan content for potential secrets.
        
        Args:
            content: Content to scan
            context: Context description (e.g., "notebook.ipynb:cell 3")
            
        Returns:
            List of (pattern_description, matched_text, context) tuples
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
    
    def check_workspace_placeholders(self, content: str, context: str) -> List[str]:
        """
        Check that WORKSPACE_NAME uses placeholders, not actual values.
        
        Args:
            content: Content to check
            context: Context description
            
        Returns:
            List of issues found
        """
        issues = []
        matches = re.finditer(self.WORKSPACE_NAME_PATTERN, content)
        
        for match in matches:
            value = match.group(1)
            if not value.startswith('<YOUR_'):
                issues.append(
                    f"{context}: WORKSPACE_NAME contains non-placeholder value: '{value}'"
                )
        
        return issues
    
    def validate_cell(self, cell: Dict[str, Any], cell_index: int, notebook_name: str) -> List[str]:
        """
        Validate a single notebook cell.
        
        Args:
            cell: Cell dictionary
            cell_index: Index of the cell
            notebook_name: Name of the notebook for context
            
        Returns:
            List of validation errors
        """
        errors = []
        context = f"{notebook_name}:cell {cell_index}"
        
        # Check for outputs in code cells
        if cell.get('cell_type') == 'code':
            if cell.get('outputs'):
                errors.append(f"{context}: Cell has outputs (should be cleared)")
            
            if cell.get('execution_count') is not None:
                errors.append(f"{context}: Cell has execution_count (should be null)")
        
        # Get source content
        source = cell.get('source', [])
        if isinstance(source, list):
            source_text = ''.join(source)
        else:
            source_text = source
        
        # Check for non-placeholder workspace names
        placeholder_issues = self.check_workspace_placeholders(source_text, context)
        errors.extend(placeholder_issues)
        
        # Scan for potential secrets
        secrets = self.scan_for_secrets(source_text, context)
        for description, matched_text, ctx in secrets:
            errors.append(f"{ctx}: {description} found: '{matched_text[:50]}...'")
        
        return errors
    
    def validate_notebook(self, notebook_path: Path) -> Tuple[List[str], List[str]]:
        """
        Validate a single notebook file.
        
        Args:
            notebook_path: Path to the notebook file
            
        Returns:
            Tuple of (errors, warnings)
        """
        errors = []
        warnings = []
        notebook_name = notebook_path.name
        
        self.log(f"Validating: {notebook_path.relative_to(self.base_dir)}")
        
        try:
            # Read notebook
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            # Validate cells
            if 'cells' in notebook:
                for i, cell in enumerate(notebook['cells']):
                    cell_errors = self.validate_cell(cell, i, notebook_name)
                    errors.extend(cell_errors)
            else:
                errors.append(f"{notebook_name}: No 'cells' field found in notebook")
            
            # Check metadata (should be minimal)
            if 'metadata' in notebook:
                metadata = notebook['metadata']
                if 'kernel_info' in metadata:
                    warnings.append(f"{notebook_name}: Contains kernel_info metadata")
                if 'language_info' in metadata:
                    lang_info = metadata['language_info']
                    if 'version' in lang_info:
                        warnings.append(f"{notebook_name}: Contains language version metadata")
            
            self.validated_count += 1
            
        except json.JSONDecodeError as e:
            errors.append(f"{notebook_name}: Invalid JSON: {e}")
        except Exception as e:
            errors.append(f"{notebook_name}: Error reading file: {e}")
        
        return errors, warnings
    
    def validate_notebook_directory(self, notebook_dir: Path) -> Tuple[List[str], List[str]]:
        """
        Validate a notebook directory (notebook + documentation).
        
        Args:
            notebook_dir: Path to notebook directory
            
        Returns:
            Tuple of (errors, warnings)
        """
        errors = []
        warnings = []
        
        # Check for .ipynb files
        notebook_files = list(notebook_dir.glob('*.ipynb'))
        if not notebook_files:
            errors.append(f"{notebook_dir.relative_to(self.base_dir)}: No .ipynb file found")
            return errors, warnings
        
        # Validate each notebook
        for notebook_path in notebook_files:
            nb_errors, nb_warnings = self.validate_notebook(notebook_path)
            errors.extend(nb_errors)
            warnings.extend(nb_warnings)
        
        # Optional documentation files are truly optional - just log them if verbose
        if self.verbose:
            optional_docs = ['README.md', 'DESIGN.md', 'IMPLEMENTATION.md']
            for doc_file in optional_docs:
                if (notebook_dir / doc_file).exists():
                    self.log(f"{notebook_dir.relative_to(self.base_dir)}: Found {doc_file}")
                else:
                    self.log(f"{notebook_dir.relative_to(self.base_dir)}: Optional file not present: {doc_file}")
        
        return errors, warnings
    
    def find_notebook_directories(self) -> List[Path]:
        """
        Find all notebook directories in base_dir.
        A notebook directory contains at least one .ipynb file.
        
        Returns:
            List of paths to notebook directories
        """
        notebook_dirs = []
        
        # Search for all .ipynb files
        for notebook_file in self.base_dir.rglob('*.ipynb'):
            notebook_dir = notebook_file.parent
            if notebook_dir not in notebook_dirs:
                notebook_dirs.append(notebook_dir)
        
        return sorted(notebook_dirs)
    
    def validate_all(self) -> bool:
        """
        Validate all notebooks in the base directory.
        
        Returns:
            True if validation passed, False otherwise
        """
        self.log(f"Searching for notebooks in: {self.base_dir}")
        
        notebook_dirs = self.find_notebook_directories()
        
        if not notebook_dirs:
            self.log("No notebooks found", 'warning')
            return True
        
        self.log(f"Found {len(notebook_dirs)} notebook directory(ies)")
        
        # Validate each notebook directory
        for notebook_dir in notebook_dirs:
            dir_errors, dir_warnings = self.validate_notebook_directory(notebook_dir)
            self.errors.extend(dir_errors)
            self.warnings.extend(dir_warnings)
        
        return len(self.errors) == 0 and (not self.strict or len(self.warnings) == 0)
    
    def print_summary(self):
        """Print a summary of the validation results."""
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        print(f"Notebooks validated: {self.validated_count}")
        
        if self.errors:
            print(f"\n[ERROR] Validation errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            warning_level = "ERROR" if self.strict else "WARNING"
            print(f"\n[{warning_level}] Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if not self.errors and not self.warnings:
            print("\n[SUCCESS] All notebooks passed validation!")
        elif not self.errors and not self.strict:
            print("\n[SUCCESS] All notebooks passed validation (with warnings)")
        
        if self.strict and self.warnings:
            print("\n[INFO] Running in strict mode: warnings treated as errors")
        
        print("="*60 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Validate that published notebooks are properly sanitized',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate all notebooks in notebooks/ directory
  python scripts/validate-notebooks.py
  
  # Validate notebooks in a specific subdirectory
  python scripts/validate-notebooks.py --directory notebooks/risk-scoring/
  
  # Strict mode: treat warnings as errors
  python scripts/validate-notebooks.py --strict
  
  # Verbose output
  python scripts/validate-notebooks.py --verbose

Exit Codes:
  0 - All notebooks passed validation
  1 - Validation errors found
  2 - Warnings found (strict mode only)
        """
    )
    
    parser.add_argument(
        '--directory',
        type=str,
        default='notebooks',
        help='Directory to validate (default: notebooks)'
    )
    
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate base directory exists
    base_dir = Path(args.directory)
    if not base_dir.exists():
        print(f"[ERROR] Directory not found: {base_dir}", file=sys.stderr)
        return 1
    
    if not base_dir.is_dir():
        print(f"[ERROR] Not a directory: {base_dir}", file=sys.stderr)
        return 1
    
    # Create validator and run
    validator = NotebookValidator(base_dir, args.strict, args.verbose)
    
    print(f"\n{'='*60}")
    print(f"NOTEBOOK VALIDATION")
    print(f"{'='*60}")
    print(f"Directory: {base_dir}")
    print(f"Strict mode: {args.strict}")
    print(f"{'='*60}\n")
    
    # Run validation
    success = validator.validate_all()
    
    # Print summary
    validator.print_summary()
    
    # Return appropriate exit code
    if validator.errors:
        print("[ERROR] Validation failed. Please fix errors above.", file=sys.stderr)
        return 1
    elif validator.warnings and args.strict:
        print("[ERROR] Validation failed in strict mode. Please fix warnings above.", file=sys.stderr)
        return 2
    else:
        if validator.warnings:
            print("[SUCCESS] Validation passed with warnings!")
        else:
            print("[SUCCESS] Validation passed!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
