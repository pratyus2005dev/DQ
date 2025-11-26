# GenDQ360 – Denodo AI SDK DQ Dashboard + Sample Chatbot Integration

This project is a **companion dashboard** for the **Denodo AI SDK**. It gives you:

- An **interactive Streamlit dashboard** where you can:
  - Upload a **data CSV**
  - Upload a **rules file (CSV/Excel)**
  - Run a **dynamic data-quality pipeline** (profiling → rules → remediation → KPIs)
  - Download cleaned / DQ outputs as CSVs for **Power BI**
- A **built-in Chatbot tab** that embeds the **official Denodo AI SDK Sample Chatbot UI**
  (served from the AI SDK repo) inside the same dashboard.
- Optional use of the **Denodo AI SDK `/answerQuestion` endpoint** to generate a
  **narrative DQ summary** from KPIs.

> ⚠️ This project does **not** bundle the Denodo AI SDK or its sample chatbot code.
> You must obtain and run the Denodo AI SDK separately from the official GitHub / Denodo
> instructions, then point this project at it via `.env`.

---

## 1. Prerequisites

1. **Denodo Platform** (Express or Enterprise Plus) and **Denodo AI SDK** installed and running.
2. The **AI SDK API server** running (usually on port `8008`).
   - From the AI SDK directory (follow Denodo docs):
     ```bash
     python run.py api
     ```
   - Or to run **both** AI SDK + sample chatbot:
     ```bash
     python run.py both
     ```
   - The API Swagger docs are generally available at:
     `http://localhost:8008/docs`.
3. The **Denodo Sample Chatbot** running (React front-end served by AI SDK).
   - When you run `python run.py both`, the chatbot typically runs at `http://localhost:3000`.
4. Python 3.10+ on your machine.

---

## 2. Project Structure

```text
genDQ_ai_sdk_project/
├─ app.py                 # Streamlit app (DQ dashboard + Chatbot tab)
├─ requirements.txt
├─ .env.example
├─ README.md
└─ dq_pipeline/
   ├─ __init__.py
   ├─ config.py
   ├─ io_utils.py
   ├─ profiling.py
   ├─ rules_engine.py
   ├─ remediation.py
   ├─ kpi.py
   ├─ orchestrator.py
   └─ ai_sdk_client.py
```

---

## 3. Installation (This Project)

1. Unzip the folder, open a terminal in the root directory (where `app.py` is).
2. Create a virtual environment:

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux / macOS
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set:

   - `AI_SDK_BASE_URL` → the URL of your AI SDK API (e.g. `http://localhost:8008`)
   - `AI_SDK_USERNAME` / `AI_SDK_PASSWORD` → credentials for AI SDK / Denodo
   - `CHATBOT_URL` → URL where the **Denodo Sample Chatbot** UI is running
     (e.g. `http://localhost:3000`)
   - `DQ_OUTPUT_DIR` → folder for saving CSV outputs (default `out`).

---

## 4. Running the Dashboard

1. Make sure **Denodo AI SDK** and **Sample Chatbot** are running.
2. In this project folder:

   ```bash
   streamlit run app.py
   ```

3. Open the URL in your browser (typically `http://localhost:8501`).

---

## 5. Using the DQ Pipeline Tab

On the **"DQ Pipeline"** tab:

1. Upload:
   - **Data CSV** — your dataset with a header row.
   - **Rules file (CSV/Excel)** — contains data-quality rules.
2. Click **"Run Data Quality Pipeline"**.

The pipeline will:

- Profile the dataset (null %, distinct counts, etc).
- Apply rules to detect violations.
- Run a simple deterministic remediation layer.
- Compute KPIs (completeness before/after, per-column stats).
- Optionally call **Denodo AI SDK** `/answerQuestion` to generate a narrative summary.

### 5.1 Rules File Format

Rules file (CSV or Excel) must include the following columns:

| column       | description                                                |
|--------------|------------------------------------------------------------|
| rule_id      | Unique ID for the rule (e.g., `R001`)                      |
| column_name  | Column in the dataset the rule applies to                  |
| rule_type    | `NOT_NULL`, `MIN`, `MAX`, `IN_LIST`, or `REGEX`           |
| param1       | Main parameter (min value, max value, list, regex, etc.)   |
| param2       | Optional second parameter (currently unused)               |
| severity     | `low` / `medium` / `high`                                  |
| description  | Human-readable explanation of the rule                     |

Example rows:

- `NOT_NULL` rule (no `param1` needed)
- `MIN` rule (e.g., `param1 = 0`)
- `IN_LIST` rule (e.g., `param1 = Active, Lapsed, Cancelled`)
- `REGEX` rule (e.g., `param1 = ^[A-Z0-9]+$`)

### 5.2 Outputs (for Power BI)

The app writes to `DQ_OUTPUT_DIR` (default `out/`):

- `cleaned_data.csv`   — cleaned dataset (use this as main fact table in Power BI)
- `dq_violations.csv`  — violation-level records
- `dq_profile.csv`     — per-column profiling
- `dq_kpis.csv`        — per-column KPI metrics

You can import these into **Power BI** using **Get Data → Text/CSV**.

---

## 6. Using the Chatbot Tab

On the **"Chatbot (Denodo Sample)"** tab:

- The app embeds the **official Denodo AI SDK Sample Chatbot UI** in an iframe.
- It uses `CHATBOT_URL` from `.env` (e.g., `http://localhost:3000`).

This way, you get:

- The **full Denodo Sample Chatbot** experience
- In the same browser tab as your **DQ dashboard**.

> If you haven't started the chatbot yet, go to your AI SDK repo and run:
> ```bash
> python run.py both
> ```

---

## 7. What You Need to Do From Your Side

1. Install and configure **Denodo Platform** and **Denodo AI SDK** following the official docs.
2. Run AI SDK (`python run.py api` or `python run.py both`).
3. Run the **Sample Chatbot** (usually already done by `python run.py both`).
4. Clone this project, install requirements, configure `.env`.
5. Run the Streamlit app (`streamlit run app.py`).
6. Upload your data + rules, run pipeline.
7. Import generated CSVs into **Power BI**.
8. Use the **Chatbot tab** to query your Denodo data via AI SDK.

---

## 8. Extending the Project

- To add more rule types → edit `dq_pipeline/rules_engine.py`.
- To change remediation logic → edit `dq_pipeline/remediation.py`.
- To change the narrative prompt → edit `dq_pipeline/ai_sdk_client.py`'s `generate_narrative_from_kpis()`.
