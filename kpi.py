import pandas as pd

def compute_kpis(original: pd.DataFrame, cleaned: pd.DataFrame, violations: pd.DataFrame):
    total_cells = original.size
    nulls_before = original.isna().sum().sum()
    nulls_after = cleaned.isna().sum().sum()

    completeness_before = 1 - (nulls_before / total_cells) if total_cells else 1.0
    completeness_after = 1 - (nulls_after / total_cells) if total_cells else 1.0

    rows = []
    total_rows = len(original)
    for col in original.columns:
        before_null = original[col].isna().sum()
        after_null = cleaned[col].isna().sum()
        v_count = violations[violations["column_name"] == col].shape[0]
        rows.append({
            "column_name": col,
            "null_count_before": int(before_null),
            "null_count_after": int(after_null),
            "null_percent_before": float(before_null) / total_rows * 100 if total_rows else 0.0,
            "null_percent_after": float(after_null) / total_rows * 100 if total_rows else 0.0,
            "violation_count": int(v_count),
        })

    col_kpis = pd.DataFrame(rows)
    kpi_summary = {
        "overall_completeness_before": completeness_before,
        "overall_completeness_after": completeness_after,
        "total_violations": int(violations.shape[0]),
    }
    return kpi_summary, col_kpis
