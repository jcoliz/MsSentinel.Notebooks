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
# Edit README.md to add notebook to "Published" section

# Optionally archive in preview repo
git mv notebooks/category/notebook-name \
       notebooks/category/notebook-name-ARCHIVED-YYYYMMDD
       
git commit -m "docs: mark [Notebook Name] as published to main repo"
git push
```

- [ ] Preview README updated with published status
- [ ] Notebook marked as archived (optional)
- [ ] Team notified of publication

## Migration Example

### Before Migration (Preview Repo)

**Notebook cell:**
```python
# ⚠️ This notebook uses preview features
# Requires: Azure Sentinel ML Models (Preview)
from azure.sentinel.ml.preview import ThreatDetectionModel  # Preview API
```

**README.md:**
```markdown
## Prerequisites
- Microsoft Sentinel workspace with ML Models preview enabled
- Preview enrollment for advanced threat detection
```

### After Migration (Public Repo)

**Notebook cell:**
```python
# Uses generally available features
from azure.sentinel.ml import ThreatDetectionModel  # GA API
```

**README.md:**
```markdown
## Prerequisites
- Microsoft Sentinel workspace
- Advanced threat detection enabled
```

## Maintaining Published Notebook List

**In Preview Repository README:**

Add a "Published Notebooks" section:

```markdown
## Published Notebooks

The following notebooks have been published to the [public repository](https://github.com/jcoliz/MsSentinel.Notebooks):

| Notebook | Published Date | Public Link |
|----------|---------------|-------------|
| User Behavior Analytics | 2024-03-15 | [View →](https://github.com/jcoliz/MsSentinel.Notebooks/tree/main/notebooks/analytics/user-behavior) |
```

## Troubleshooting

### Preview APIs Changed During GA

**Issue**: API signatures or behavior changed between preview and GA

**Solution**:
- Update code to use GA API signatures
- Test thoroughly in clean environment
- Document breaking changes in IMPLEMENTATION.md
- Add migration notes for users who had preview version

### Documentation References Preview URLs

**Issue**: Microsoft Learn links still point to preview documentation

**Solution**:
- Update all Microsoft Learn links to GA documentation
- Remove preview-specific configuration steps
- Verify all linked resources are publicly accessible
- Check for broken links

### Notebook Category Doesn't Exist in Public Repo

**Issue**: Preview notebook is in a category not yet in public repo

**Solution**:
- Create category organically (don't create empty categories)
- Ensure category name follows naming conventions from main repo
- Update notebooks/README.md with new category section
- Consider if notebook fits better in existing category

### Preview Features Partially Released

**Issue**: Notebook uses multiple preview features, only some are GA

**Solution**:
- Wait until all required features are GA
- Or split notebook into GA and preview versions
- Document which features are still preview in IMPLEMENTATION.md

## Best Practices

### For Preview Repository Maintainers

1. **Document Preview Requirements**: Clearly state which preview features and enrollments are needed
2. **Keep Scripts Synchronized**: Periodically sync scripts from main repo to ensure consistency
3. **Test Migration Process**: Validate the migration workflow regularly with test notebooks
4. **Track Feature Status**: Monitor Microsoft's release notes for GA announcements
5. **Maintain Access List**: Keep collaborator list current as team members change

### For Notebook Authors

1. **Mark Preview Status Clearly**: Add warnings in notebook cells and documentation
2. **Use Version Comments**: Note which preview API versions are used
3. **Document Breaking Changes**: Track expected differences from preview to GA
4. **Test Regularly**: Verify notebooks still work as preview features evolve
5. **Plan for Migration**: Write notebooks with eventual publication in mind

## Timeline Expectations

- **Preview Duration**: Features typically remain in preview for 3-12 months
- **Migration Effort**: 1-3 hours per notebook depending on complexity
- **Testing**: Allow extra time for GA feature validation in clean environment
- **Review Process**: Public repo may require PR review before merge

## Automation Opportunities

Consider automating parts of the migration process:

```bash
# Example: Migration helper script (future enhancement)
python scripts/migrate-to-public.py \
  --notebook category/notebook-name \
  --target-repo ../MsSentinel.Notebooks \
  --verify-ga-features
```

## Related Documentation

- [Preview Repository Setup Guide](../preview-repository-setup.md) - Complete setup instructions
- [Quick Start Guide](../preview-repository-quickstart.md) - Fast setup reference
- [Main Repository Structure](https://github.com/jcoliz/MsSentinel.Notebooks/blob/main/docs/repository-structure.md)
- [Script Documentation](../../scripts/README.md)

## Questions?

Contact repository maintainer or open an issue in the preview repository for migration questions.

---

*This guide will be updated as the migration process evolves through practice.*
