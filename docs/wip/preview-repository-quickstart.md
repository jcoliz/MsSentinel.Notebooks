# Preview Repository Quick Start

Quick reference for setting up and using a separate private repository for notebooks with unreleased features.

## Why Separate Private Repository?

✅ **Security**: No risk of accidental public exposure  
✅ **Access Control**: GitHub native collaborator permissions  
✅ **Clean Migration**: Simple path to publish when features release  
✅ **Workflow Consistency**: Same tools and structure as main repo  

## Quick Setup

### 1. Create Repository (5 minutes)

```bash
# On GitHub: Create new private repository
# Name: MsSentinel.Notebooks.Preview (or your choice)
# Visibility: Private
# Don't initialize with README

# Clone it
git clone https://github.com/YOUR-ORG/MsSentinel.Notebooks.Preview.git
cd MsSentinel.Notebooks.Preview
```

### 2. Copy Core Files (2 minutes)

```bash
# From main repository, copy essential structure
cp ../MsSentinel.Notebooks/.gitignore .
cp -r ../MsSentinel.Notebooks/.roo .
cp -r ../MsSentinel.Notebooks/scripts .
cp -r ../MsSentinel.Notebooks/templates .

# Create directories
mkdir -p notebooks docs workspace
touch workspace/.gitkeep
```

### 3. Create Preview-Specific README

See template in [`preview-repository-setup.md`](preview-repository-setup.md#preview-repository-readme-template)

Key points to include:
- Which preview features are required
- Link back to public repo (for context)
- Access instructions for collaborators
- Migration process reference

### 4. Add Collaborators

GitHub Settings → Collaborators → Add specific users

### 5. Initial Commit

```bash
git add .
git commit -m "chore: initialize preview repository structure"
git push origin main
```

## Daily Workflow

Identical to main repository:

```bash
# Develop in workspace
python scripts/setup-workspace.py --create category/notebook-name

# Edit workspace/category/notebook-name/*.ipynb
# Run and test

# Sanitize for sharing with collaborators
python scripts/sanitize-notebook.py workspace/category/notebook-name/*.ipynb

# Commit sanitized version
git add notebooks/category/notebook-name/
git commit -m "feat: add notebook-name notebook"
git push
```

## Migration When Feature Releases

Simple 3-step process:

```bash
# 1. In preview repo: Ensure notebook is sanitized and up to date
python scripts/validate-notebooks.py notebooks/category/notebook-name/

# 2. Copy to main repo
cp -r notebooks/category/notebook-name/ \
      ../MsSentinel.Notebooks/notebooks/category/notebook-name/

# 3. In main repo: Create PR
cd ../MsSentinel.Notebooks
git checkout -b add-notebook-name
git add notebooks/category/notebook-name/
git commit -m "feat: add notebook-name (feature now GA)"
git push origin add-notebook-name
```

Full details in [`preview-repository-setup.md`](preview-repository-setup.md)

## Key Files to Create

Minimal setup needs:
1. ✅ `.gitignore` (copy from main)
2. ✅ `README.md` (preview-specific)
3. ✅ `scripts/` (copy all from main)
4. ✅ `templates/` (copy from main)
5. ✅ `.roo/` (copy conventions from main)
6. ✅ `docs/migration-guide.md` (from setup guide)

Optional but recommended:
- Copy `docs/getting-started.md` from main repo
- Copy `docs/repository-structure.md` from main repo
- Create `docs/preview-features.md` listing required features

## Common Questions

**Q: Do I need to maintain both repositories?**  
A: Yes, but they're independent. Preview repo is for development with unreleased features. Main repo is for public consumption.

**Q: How do I keep scripts synchronized?**  
A: Periodically copy updated scripts from main repo. They should work identically.

**Q: Can I have different notebooks in preview vs. main?**  
A: Yes! Completely independent content. Notebooks only migrate when features are GA.

**Q: What if a preview feature never goes GA?**  
A: Notebook stays in preview repo indefinitely or gets archived.

## See Also

- [`preview-repository-setup.md`](preview-repository-setup.md) - Complete setup guide with templates
- [Main repository](https://github.com/jcoliz/MsSentinel.Notebooks) - Public notebook repository
- [Repository Structure](../repository-structure.md) - Main repo organization

---

**Ready to start?** Follow the 5-minute setup above, then start creating notebooks!
