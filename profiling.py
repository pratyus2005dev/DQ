import pandas as pd

def profile_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    total_rows = len(df)

    for col in df.columns:
        s = df[col]
        non_null = s.notna().sum()
        nulls = s.isna().sum()
        distinct = s.nunique(dropna=True)
        dtype = str(s.dtype)
        rows.append({
            "column_name": col,
            "dtype": dtype,
            "row_count": total_rows,
            "non_null_count": int(non_null),
            "null_count": int(nulls),
            "null_percent": float(nulls) / total_rows * 100 if total_rows else 0.0,
            "distinct_count": int(distinct),
        })

    return pd.DataFrame(rows)
