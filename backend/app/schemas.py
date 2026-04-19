from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    dataset_id: str
    filename: str
    rows: int
    columns: list[str]
    target_suggestions: list[str]
    preview: list[dict[str, Any]]


class TrainRequest(BaseModel):
    dataset_id: str
    target_column: str
    model_type: Literal["logistic_regression", "random_forest"] = "random_forest"
    test_size: float = Field(default=0.2, ge=0.1, le=0.4)
    random_state: int = 42


class TrainResponse(BaseModel):
    run_id: str
    dataset_id: str
    model_type: str
    target_column: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: dict[str, int]
    prediction_preview: list[dict[str, Any]]


class BiasResponse(BaseModel):
    run_id: str
    sensitive_column: str
    demographic_parity_difference: float
    equal_opportunity_difference: float
    selection_rate_by_group: dict[str, float]
    true_positive_rate_by_group: dict[str, float]
    fairness_index: float


class ExplainResponse(BaseModel):
    run_id: str
    sample_size: int
    top_global_features: list[dict[str, Any]]
    local_explanation: list[dict[str, Any]]


class ReportResponse(BaseModel):
    run_id: str
    train: TrainResponse
    bias: BiasResponse
    explain: ExplainResponse
