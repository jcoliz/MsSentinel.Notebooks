# PySpark DataFrame Join Best Practices

## Rule: Avoid Ambiguous Column References in Joins

### Problem
When joining DataFrames in PySpark, duplicate column names can cause `AnalysisException: [AMBIGUOUS_REFERENCE]` errors, especially when:
1. Joining on a column that exists in both DataFrames
2. Re-running cells that add columns (non-idempotent operations)
3. Using `col()` function without DataFrame qualification

### Root Causes Encountered
- **Join creates duplicate columns**: Both the join condition and the retained columns have the same name
- **Previous cell runs leave columns**: Re-executing cells adds duplicate columns to existing DataFrames
- **Unqualified column references**: Using `col("column_name")` without specifying which DataFrame

### Solution Pattern

When joining DataFrames with overlapping column names:

```python
# 1. ALWAYS drop existing columns first for idempotency
if "new_column" in base_df.columns:
    base_df = base_df.drop("new_column")
if "join_agg_column" in base_df.columns:
    base_df = base_df.drop("join_agg_column")

# 2. Perform the join
base_df = (
    base_df
    .join(
        aggregate_df,
        base_df.common_column == aggregate_df.common_column,  # Use DataFrame.column syntax
        "left"
    )
    # 3. Use explicit DataFrame qualification in any transformations
    .withColumn(
        "new_column",
        coalesce(aggregate_df["join_agg_column"], lit(default_value))
    )
    # 4. Select columns explicitly to avoid duplicates
    .select(
        base_df["*"],      # All original columns from base
        col("new_column")  # Only the new column
    )
)
```

### Key Principles

1. **Idempotency First**: Drop any columns that will be created before creating them
2. **Qualify Everything**: Use `DataFrame.column` or `DataFrame["column"]` syntax in join conditions and transformations
3. **Explicit Selection**: Use `.select()` after joins to control exactly which columns are kept
4. **Test Re-execution**: Ensure code can be run multiple times without errors

### Example: Department Baseline Join (Section 7 Pattern)

```python
# Calculate aggregates
dept_baselines = (
    combined_metrics
    .filter(col("department").isNotNull())
    .groupBy("department")
    .agg(avg("total_signins").alias("dept_avg_signins"))
)

# Clean up existing columns for idempotency
if "baseline_signins" in combined_metrics.columns:
    combined_metrics = combined_metrics.drop("baseline_signins")
if "dept_avg_signins" in combined_metrics.columns:
    combined_metrics = combined_metrics.drop("dept_avg_signins")

# Join with explicit qualification
combined_metrics = (
    combined_metrics
    .join(
        dept_baselines,
        combined_metrics.department == dept_baselines.department,  # Qualified!
        "left"
    )
    .withColumn(
        "baseline_signins",
        coalesce(dept_baselines["dept_avg_signins"], lit(global_avg))  # Qualified!
    )
    .select(
        combined_metrics["*"],  # All original columns
        col("baseline_signins")  # Only the new column
    )
)
```

### Anti-Patterns to Avoid

❌ **Unqualified join conditions**:
```python
.join(other_df, "common_column", "left")  # Creates duplicate column
```

❌ **Unqualified column references in coalesce**:
```python
.withColumn("result", coalesce(col("agg_column"), lit(default)))  # Ambiguous!
```

❌ **No cleanup before re-running**:
```python
# Running this twice creates duplicates
combined = combined.withColumn("new_col", ...)
```

❌ **Implicit column selection after join**:
```python
df = df.join(other_df, condition)  # Keeps all columns from both, including duplicates
```

### When to Apply This Rule

- Any LEFT/RIGHT/INNER JOIN operation
- Joining on columns that exist in both DataFrames
- Code that will be run multiple times (notebooks, iterative development)
- Using aggregate DataFrames with overlapping column names
- Any operation using `coalesce()` with joined columns

### Additional Notes

For CustomDataFrame objects (Microsoft Sentinel Provider):
- Cannot use subscript notation: `df["column"]` will fail
- Must use `DataFrame.column` or `col("column")` with qualification
- Same join ambiguity issues apply as regular PySpark DataFrames