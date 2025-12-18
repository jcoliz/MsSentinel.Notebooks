# Microsoft Sentinel CustomDataFrame Syntax

## Rule: Use Attribute Notation for CustomDataFrame Column Access

### Problem
The Microsoft Sentinel Provider returns `CustomDataFrame` objects that **do not support subscript notation** for column access. Using subscript notation causes a `TypeError`.

### Error Example
```python
# ❌ WRONG - Causes TypeError: 'CustomDataFrame' object is not subscriptable
combined_df = (
    signin_metrics
    .join(users_df, signin_metrics.UserId == users_df.id, "left")
    .select(
        signin_metrics["UserId"],           # ❌ TypeError
        signin_metrics["UserPrincipalName"], # ❌ TypeError
        users_df["displayName"],            # ❌ TypeError
        col("unique_ip_count")
    )
)
```

### Correct Syntax

Use one of these approaches with CustomDataFrame objects:

#### 1. Attribute Notation (Preferred for DataFrame-Qualified Columns)
```python
# ✅ CORRECT - Use DataFrame.column_name
combined_df = (
    signin_metrics
    .join(users_df, signin_metrics.UserId == users_df.id, "left")
    .select(
        signin_metrics.UserId,              # ✅ Attribute notation
        signin_metrics.UserPrincipalName,   # ✅ Attribute notation
        users_df.displayName.alias("UserDisplayName"),  # ✅ With alias
        users_df.department,                # ✅ Attribute notation
        col("unique_ip_count")              # ✅ col() for unqualified
    )
)
```

#### 2. col() Function (For Unqualified Column References)
```python
# ✅ CORRECT - Use col() for columns that don't need qualification
combined_df = (
    signin_metrics
    .join(users_df, signin_metrics.UserId == users_df.id, "left")
    .select(
        col("UserId"),                      # ✅ Works when column is unique
        col("UserPrincipalName"),           # ✅ Works when column is unique
        users_df.displayName.alias("UserDisplayName"),  # ✅ Qualified
        users_df.department,                # ✅ Qualified
        col("unique_ip_count"),             # ✅ Unambiguous after join
        col("total_signins")                # ✅ Unambiguous after join
    )
)
```

### When to Use Each Syntax

| Scenario | Syntax | Example |
|----------|--------|---------|
| DataFrame-qualified column needed | `DataFrame.column` | `users_df.displayName` |
| Column with alias | `DataFrame.column.alias("new_name")` | `users_df.displayName.alias("UserDisplayName")` |
| Unique column after join | `col("column_name")` | `col("unique_ip_count")` |
| Column in join condition | `DataFrame.column == otherDF.column` | `signin_metrics.UserId == users_df.id` |
| Never use | `DataFrame["column"]` | ❌ **Will fail** |

### Join Pattern Best Practices

```python
# Complete example following best practices
from pyspark.sql.functions import col

# Join with proper column qualification
combined_df = (
    base_df
    .join(
        enrichment_df,
        base_df.join_key == enrichment_df.join_key,  # ✅ Qualified in condition
        "left"
    )
    .select(
        # From base DataFrame - use attribute notation
        base_df.UserId,
        base_df.UserPrincipalName,
        
        # From enrichment DataFrame - use attribute notation
        enrichment_df.displayName.alias("UserDisplayName"),
        enrichment_df.department,
        
        # Aggregated columns (unambiguous) - use col()
        col("unique_ip_count"),
        col("total_signins")
    )
)
```

### Why This Matters

1. **CustomDataFrame Limitation**: The Sentinel provider's CustomDataFrame class does not implement the `__getitem__` method, making subscript notation unsupported
2. **Standard PySpark Compatibility**: Regular PySpark DataFrames support both syntaxes, but CustomDataFrame only supports attribute notation
3. **Production Code**: All Sentinel notebook code must use compatible syntax to avoid runtime errors

### When You'll Encounter This

- Any notebook using `MicrosoftSentinelProvider.read_table()`
- Joins between Sentinel tables (SigninLogs, EntraUsers, AuditLogs, SecurityAlert)
- Any DataFrame operations after loading from Sentinel

### Related Patterns

See also:
- [`pyspark-join-patterns.md`](.roo/rules/pyspark-join-patterns.md) - For handling ambiguous columns in joins
- Risk Score notebooks for proven working examples

### Quick Reference

```python
# ❌ NEVER
df["column"]
df["column"].alias("new")
base_df["column"] + other_df["column"]

# ✅ ALWAYS
df.column
df.column.alias("new")
col("column")
base_df.column + other_df.column
```

### Example from Working Code

From `User Risk Score Simple.ipynb`:
```python
# Section 5: Join with User Profiles
combined_df = (
    signin_metrics
    .join(
        users_df,
        signin_metrics.UserId == users_df.id,  # ✅ Attribute notation
        "left"
    )
    .select(
        col("UserId"),                         # ✅ col() for unique columns
        col("UserPrincipalName"),              # ✅ col() for unique columns
        users_df.displayName.alias("UserDisplayName"),  # ✅ Qualified
        users_df.department,                   # ✅ Qualified
        col("unique_ip_count"),                # ✅ Aggregated column
        col("total_signins")                   # ✅ Aggregated column
    )
)
```

This pattern is proven to work across all Sentinel notebooks including the full Risk Score.ipynb.