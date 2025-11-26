from typing import Dict, Any
import requests
from .config import get_config

def _get_auth(cfg):
    if cfg.ai_sdk_username and cfg.ai_sdk_password:
        return (cfg.ai_sdk_username, cfg.ai_sdk_password)
    return None

def call_answer_question(question: str, extra_payload: Dict[str, Any] | None = None) -> Dict[str, Any] | None:
    """Call Denodo AI SDK /answerQuestion endpoint, if configured.

    Returns parsed JSON or None on error.
    """
    cfg = get_config()
    base = cfg.ai_sdk_base_url.rstrip("/")
    if not base:
        return None

    url = f"{base}/answerQuestion"
    payload: Dict[str, Any] = {
        "question": question,
        "plot": False,
        "markdown_response": True,
        "verbose": False,
    }
    if extra_payload:
        payload.update(extra_payload)

    try:
        resp = requests.post(url, json=payload, auth=_get_auth(cfg), timeout=120)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        # In production, log this instead of printing
        print("[AI SDK] Error calling /answerQuestion:", e)
        return None

def generate_narrative_from_kpis(kpi_summary: Dict[str, Any], kpi_table) -> str | None:
    """Use AI SDK's /answerQuestion to generate a DQ narrative.

    If AI SDK is not configured or fails, returns None.
    """
    question = (
        "You are a data quality analyst. I will give you high-level KPI metrics "
        "(before/after completeness, total violations) and a column-level table "
        "of null % and violation counts. Write a short markdown summary for an "
        "executive dashboard, focusing on improvements and remaining issues.\n\n"
        f"KPI summary: {kpi_summary}\n\n"
        f"Column KPIs (first rows): {kpi_table.head(20).to_dict(orient='records')}"
    )
    result = call_answer_question(question)
    if not result:
        return None
    # Typical AI SDK response includes 'answer'
    return result.get("answer") or result.get("response") or None
