from __future__ import annotations

import json
import os
from datetime import datetime
from io import BytesIO
from pathlib import Path
from uuid import uuid4

import pandas as pd
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse

from .ml_pipeline import compute_bias, compute_explainability, suggest_target_columns, train_pipeline
from .schemas import BiasResponse, ExplainResponse, ReportResponse, TrainRequest, TrainResponse, UploadResponse
from .store import InMemoryStore, TrainingRun

ROOT_DIR = Path(__file__).resolve().parents[2]
WEB_DIR = ROOT_DIR / "frontend" / "WEB"
MOBILE_DIR = ROOT_DIR / "MOBILE"
DATA_DIR = ROOT_DIR / "backend" / "data"
RUNS_JSON = DATA_DIR / "runs.json"

WEB_PAGES = {
    "landing": "landing_page",
    "login": "login",
    "dashboard": "dashboard_overview",
    "upload": "upload_dataset",
    "model-analysis": "model_analysis",
    "bias-report": "bias_detection",
    "explainability": "explainability_engine",
    "reports": "audit_reports",
    "settings": "settings",
}

MOBILE_PAGES = {
    "landing": "landing_page_mobile_v2",
    "login": "login_mobile_v2",
    "dashboard": "dashboard_mobile_v2",
    "upload": "upload_mobile_v2",
    "model-analysis": "model_analysis_mobile_v3",
    "bias-report": "bias_detection_mobile_v2",
    "explainability": "explainability_mobile_v2",
    "reports": "reports_mobile_v2",
}

store = InMemoryStore()

app = FastAPI(
    title="FairHire AI Backend",
    description="Responsible AI audit API implementing PRD/TRD requirements.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _persist_run_summary(run: TrainingRun, bias_payload: dict | None = None, explain_payload: dict | None = None) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []
    if RUNS_JSON.exists():
        with RUNS_JSON.open("r", encoding="utf-8") as f:
            records = json.load(f)

    record = {
        "run_id": run.run_id,
        "dataset_id": run.dataset_id,
        "model_type": run.model_type,
        "target_column": run.target_column,
        "created_at": run.created_at.isoformat(),
        "metrics": run.metrics,
        "bias": bias_payload,
        "explain": explain_payload,
    }
    records.append(record)

    with RUNS_JSON.open("w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def _read_uploaded_file(upload: UploadFile, content: bytes) -> pd.DataFrame:
    filename = (upload.filename or "dataset.csv").lower()
    try:
        if filename.endswith(".csv"):
            return pd.read_csv(BytesIO(content))
        if filename.endswith(".json"):
            return pd.read_json(BytesIO(content))
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            return pd.read_excel(BytesIO(content))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {exc}") from exc

    raise HTTPException(status_code=400, detail="Unsupported file format. Use CSV, JSON, or XLSX.")


def _load_page(platform_map: dict[str, str], base_dir: Path, page: str) -> FileResponse:
    folder = platform_map.get(page)
    if not folder:
        raise HTTPException(status_code=404, detail=f"Page '{page}' not found")

    file_path = base_dir / folder / "code.html"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Missing view file: {file_path}")

    return FileResponse(str(file_path), media_type="text/html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def root() -> str:
    web_links = "".join([f'<li><a href="/web/{slug}">{slug}</a></li>' for slug in WEB_PAGES])
    mobile_links = "".join([f'<li><a href="/mobile/{slug}">{slug}</a></li>' for slug in MOBILE_PAGES])
    return f"""
    <html>
      <head><title>FairHire AI Launcher</title></head>
      <body style=\"font-family: Inter, sans-serif; padding: 24px;\">
        <h1>FairHire AI Full-Stack Application</h1>
        <p>Backend docs: <a href=\"/docs\">/docs</a></p>
        <h2>Web Screens</h2>
        <ul>{web_links}</ul>
        <h2>Mobile Screens</h2>
        <ul>{mobile_links}</ul>
      </body>
    </html>
    """


@app.get("/web/{page}")
def web_page(page: str) -> FileResponse:
    return _load_page(WEB_PAGES, WEB_DIR, page)


@app.get("/mobile/{page}")
def mobile_page(page: str) -> FileResponse:
    return _load_page(MOBILE_PAGES, MOBILE_DIR, page)


@app.post("/upload", response_model=UploadResponse)
async def upload_dataset(file: UploadFile = File(...), target_column: str | None = Form(default=None)) -> UploadResponse:
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    frame = _read_uploaded_file(file, content)
    if frame.empty:
        raise HTTPException(status_code=400, detail="Parsed dataset is empty")

    dataset_id = f"ds_{uuid4().hex[:10]}"
    frame.columns = [str(c).strip() for c in frame.columns]
    store.put_dataset(dataset_id, frame)

    suggestions = suggest_target_columns(frame)
    if target_column and target_column in frame.columns and target_column not in suggestions:
        suggestions = [target_column] + suggestions

    preview = frame.head(8).fillna("").to_dict(orient="records")
    return UploadResponse(
        dataset_id=dataset_id,
        filename=file.filename or "dataset.csv",
        rows=int(frame.shape[0]),
        columns=list(frame.columns),
        target_suggestions=suggestions,
        preview=preview,
    )


@app.post("/train", response_model=TrainResponse)
def train_model(payload: TrainRequest) -> TrainResponse:
    try:
        frame = store.get_dataset(payload.dataset_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    try:
        artifacts = train_pipeline(
            frame=frame,
            target_column=payload.target_column,
            model_type=payload.model_type,
            test_size=payload.test_size,
            random_state=payload.random_state,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    run_id = f"run_{uuid4().hex[:10]}"
    run = TrainingRun(
        run_id=run_id,
        dataset_id=payload.dataset_id,
        model_type=payload.model_type,
        target_column=payload.target_column,
        model=artifacts.model,
        test_frame=artifacts.test_frame,
        y_true=artifacts.y_true,
        y_pred=artifacts.y_pred,
        metrics=artifacts.metrics,
        created_at=datetime.utcnow(),
    )
    store.put_run(run)

    preview_df = artifacts.test_frame.copy()
    preview_df["prediction"] = artifacts.y_pred
    preview = preview_df.head(10).fillna("").to_dict(orient="records")

    response = TrainResponse(
        run_id=run_id,
        dataset_id=payload.dataset_id,
        model_type=payload.model_type,
        target_column=payload.target_column,
        accuracy=artifacts.metrics["accuracy"],
        precision=artifacts.metrics["precision"],
        recall=artifacts.metrics["recall"],
        f1_score=artifacts.metrics["f1_score"],
        confusion_matrix=artifacts.metrics["confusion_matrix"],
        prediction_preview=preview,
    )
    _persist_run_summary(run)
    return response


@app.get("/bias", response_model=BiasResponse)
def bias_metrics(run_id: str, sensitive_column: str = "gender") -> BiasResponse:
    try:
        run = store.get_run(run_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    try:
        bias = compute_bias(
            test_frame=run.test_frame,
            y_true=run.y_true,
            y_pred=run.y_pred,
            sensitive_column=sensitive_column,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    payload = BiasResponse(
        run_id=run_id,
        sensitive_column=bias["sensitive_column"],
        demographic_parity_difference=bias["demographic_parity_difference"],
        equal_opportunity_difference=bias["equal_opportunity_difference"],
        selection_rate_by_group=bias["selection_rate_by_group"],
        true_positive_rate_by_group=bias["true_positive_rate_by_group"],
        fairness_index=bias["fairness_index"],
    )
    _persist_run_summary(run, bias_payload=payload.model_dump())
    return payload


@app.get("/explain", response_model=ExplainResponse)
def explain_metrics(run_id: str, sample_size: int = 40) -> ExplainResponse:
    try:
        run = store.get_run(run_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    feature_frame = run.test_frame.drop(columns=[run.target_column], errors="ignore")
    try:
        explain = compute_explainability(run.model, feature_frame, sample_size=sample_size)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    payload = ExplainResponse(run_id=run_id, **explain)
    _persist_run_summary(run, explain_payload=payload.model_dump())
    return payload


@app.get("/report", response_model=ReportResponse)
def report(run_id: str, sensitive_column: str = "gender", sample_size: int = 40) -> ReportResponse:
    train_run = train_metrics(run_id)
    bias = bias_metrics(run_id=run_id, sensitive_column=sensitive_column)
    explain = explain_metrics(run_id=run_id, sample_size=sample_size)
    return ReportResponse(run_id=run_id, train=train_run, bias=bias, explain=explain)


@app.get("/train/{run_id}", response_model=TrainResponse)
def train_metrics(run_id: str) -> TrainResponse:
    try:
        run = store.get_run(run_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    preview_df = run.test_frame.copy()
    preview_df["prediction"] = run.y_pred
    preview = preview_df.head(10).fillna("").to_dict(orient="records")

    return TrainResponse(
        run_id=run_id,
        dataset_id=run.dataset_id,
        model_type=run.model_type,
        target_column=run.target_column,
        accuracy=run.metrics["accuracy"],
        precision=run.metrics["precision"],
        recall=run.metrics["recall"],
        f1_score=run.metrics["f1_score"],
        confusion_matrix=run.metrics["confusion_matrix"],
        prediction_preview=preview,
    )
