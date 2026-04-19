# FairHire AI Full-Stack MVP

This implementation follows the provided PRD/TRD and uses the existing WEB and MOBILE screen designs as the frontend views.

## What is included

- Frontend screens preserved from:
  - `frontend/WEB/*/code.html`
  - `MOBILE/*/code.html`
- FastAPI backend with required APIs:
  - `POST /upload`
  - `POST /train`
  - `GET /bias`
  - `GET /explain`
  - `GET /report`
- Additional utilities:
  - `GET /health`
  - `GET /docs` (Swagger UI)
  - screen launcher routes for web/mobile pages

## Backend architecture

- App entry: `backend/app/main.py`
- ML pipeline: `backend/app/ml_pipeline.py`
- Schemas: `backend/app/schemas.py`
- Runtime store: `backend/app/store.py`

Pipeline flow:

1. Upload dataset (CSV/JSON/XLSX)
2. Train baseline model (Random Forest or Logistic Regression)
3. Compute fairness metrics (Demographic Parity Difference, Equal Opportunity Difference)
4. Generate explainability output (SHAP global + local feature impact)
5. Aggregate report

## Run locally

1. Create a virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the API server from the project root:

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

3. Open in browser:

- Launcher: `http://localhost:8000/`
- API Docs: `http://localhost:8000/docs`
- Example web page: `http://localhost:8000/web/dashboard`
- Example mobile page: `http://localhost:8000/mobile/dashboard`

## Notes

- Screen layouts are served directly from your existing `code.html` files to keep design parity with provided screenshots.
- Training runs are stored in memory for this MVP session and run summaries are appended to `backend/data/runs.json`.
- For production, move in-memory state to PostgreSQL/Firebase and add authentication.
