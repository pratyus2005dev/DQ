import os
import pandas as pd

def ensure_dir(path: str) -> None:
    if path and not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def save_csv(df: pd.DataFrame, path: str) -> None:
    ensure_dir(os.path.dirname(path))
    df.to_csv(path, index=False)

def read_rules_file(file) -> pd.DataFrame:
    filename = getattr(file, "name", "")
    if filename.lower().endswith((".xls", ".xlsx")):
        return pd.read_excel(file)
    return pd.read_csv(file)
