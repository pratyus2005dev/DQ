from typing import Dict, Any
import pandas as pd
from .config import get_config
from . import profiling, rules_engine, remediation, kpi, io_utils, ai_sdk_client

def run_pipeline(data: pd.DataFrame, rules_df: pd.DataFrame) -> Dict[str, Any]:
    cfg = get_config()

    # 1. Profiling
    profile_df = profiling.profile_dataframe(data)

    # 2. Rules & violations
    normalized_rules = rules_engine.normalize_rules_df(rules_df)
    violations_df = rules_engine.evaluate_rules(data, normalized_rules)

    # 3. Remediation
    cleaned_df = remediation.remediate(data, violations_df, normalized_rules)

    # 4. KPIs
    kpi_summary, col_kpis_df = kpi.compute_kpis(data, cleaned_df, violations_df)

    # 5. Optional AI SDK narrative
    narrative = ai_sdk_client.generate_narrative_from_kpis(kpi_summary, col_kpis_df)

    # 6. Persist outputs for Power BI
    out_dir = cfg.output_dir
    io_utils.ensure_dir(out_dir)
    io_utils.save_csv(cleaned_df, f"{out_dir}/cleaned_data.csv")
    io_utils.save_csv(violations_df, f"{out_dir}/dq_violations.csv")
    io_utils.save_csv(profile_df, f"{out_dir}/dq_profile.csv")
    io_utils.save_csv(col_kpis_df, f"{out_dir}/dq_kpis.csv")

    return {
        "profile": profile_df,
        "violations": violations_df,
        "cleaned": cleaned_df,
        "kpi_summary": kpi_summary,
        "kpi_table": col_kpis_df,
        "narrative": narrative,
    }
