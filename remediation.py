import pandas as pd
import numpy as np

def remediate(df: pd.DataFrame, violations: pd.DataFrame, rules_df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    rules_df = rules_df.set_index("rule_id", drop=False)

    for rule_id, group in violations.groupby("rule_id"):
        if rule_id not in rules_df.index:
            continue

        rule = rules_df.loc[rule_id]
        col = rule["column_name"]
        rtype = rule["rule_type"]
        param1 = rule.get("param1")

        if col not in cleaned.columns:
            continue

        idxs = group["row_index"].tolist()

        if rtype == "NOT_NULL":
            default_value = param1 if not pd.isna(param1) else "UNKNOWN"
            cleaned.loc[idxs, col] = cleaned.loc[idxs, col].fillna(default_value)

        elif rtype == "MIN":
            try:
                min_val = float(param1)
                cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")
                cleaned.loc[idxs, col] = cleaned.loc[idxs, col].clip(lower=min_val)
            except Exception:
                continue

        elif rtype == "MAX":
            try:
                max_val = float(param1)
                cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")
                cleaned.loc[idxs, col] = cleaned.loc[idxs, col].clip(upper=max_val)
            except Exception:
                continue

        elif rtype == "IN_LIST":
            if pd.isna(param1):
                continue
            allowed = [v.strip() for v in str(param1).split(",")]
            replacement = allowed[0] if allowed else "OTHER"
            mask = cleaned.index.isin(idxs)
            cleaned.loc[mask, col] = cleaned.loc[mask, col].where(
                cleaned.loc[mask, col].isin(allowed),
                other=replacement
            )

        # REGEX: in this simple demo, we only flag; no automatic fix

    return cleaned
