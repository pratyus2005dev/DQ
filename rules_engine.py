import re
from typing import List, Dict, Any
import pandas as pd
import numpy as np

SUPPORTED_RULE_TYPES = {"NOT_NULL", "MIN", "MAX", "IN_LIST", "REGEX"}

def normalize_rules_df(rules_df: pd.DataFrame) -> pd.DataFrame:
    required_cols = [
        "rule_id", "column_name", "rule_type",
        "param1", "param2", "severity", "description"
    ]
    for col in required_cols:
        if col not in rules_df.columns:
            rules_df[col] = np.nan
    rules_df["rule_type"] = rules_df["rule_type"].astype(str).str.upper().str.strip()
    rules_df["rule_id"] = rules_df["rule_id"].astype(str)
    return rules_df

def evaluate_rules(df: pd.DataFrame, rules_df: pd.DataFrame) -> pd.DataFrame:
    rules_df = normalize_rules_df(rules_df)
    records: List[Dict[str, Any]] = []

    for _, rule in rules_df.iterrows():
        rule_id = rule["rule_id"]
        col = rule["column_name"]
        rtype = rule["rule_type"]
        param1 = rule.get("param1")
        param2 = rule.get("param2")
        severity = rule.get("severity", "medium")
        desc = rule.get("description", "")

        if rtype not in SUPPORTED_RULE_TYPES:
            continue
        if col not in df.columns:
            continue

        s = df[col]

        if rtype == "NOT_NULL":
            mask = s.isna()
            reason = "Value is NULL"

        elif rtype == "MIN":
            try:
                min_val = float(param1)
                s_num = pd.to_numeric(s, errors="coerce")
                mask = s_num < min_val
                reason = f"Value < MIN ({min_val})"
            except Exception:
                continue

        elif rtype == "MAX":
            try:
                max_val = float(param1)
                s_num = pd.to_numeric(s, errors="coerce")
                mask = s_num > max_val
                reason = f"Value > MAX ({max_val})"
            except Exception:
                continue

        elif rtype == "IN_LIST":
            if pd.isna(param1):
                continue
            allowed = [v.strip() for v in str(param1).split(",")]
            mask = ~s.isin(allowed)
            reason = f"Value not in allowed list: {allowed}"

        elif rtype == "REGEX":
            if pd.isna(param1):
                continue
            pattern = re.compile(str(param1))
            mask = ~s.fillna("").astype(str).str.match(pattern)
            reason = f"Value does not match regex: {param1}"

        else:
            continue

        violating_indices = df.index[mask].tolist()
        for idx in violating_indices:
            records.append({
                "row_index": int(idx),
                "rule_id": rule_id,
                "column_name": col,
                "severity": severity,
                "description": desc,
                "reason": reason,
                "value": df.at[idx, col],
            })

    return pd.DataFrame(records)
