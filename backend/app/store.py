from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from threading import Lock
from typing import Any

import pandas as pd


@dataclass
class TrainingRun:
    run_id: str
    dataset_id: str
    model_type: str
    target_column: str
    model: Any
    test_frame: pd.DataFrame
    y_true: pd.Series
    y_pred: pd.Series
    metrics: dict[str, Any]
    created_at: datetime


class InMemoryStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self.datasets: dict[str, pd.DataFrame] = {}
        self.runs: dict[str, TrainingRun] = {}

    def put_dataset(self, dataset_id: str, frame: pd.DataFrame) -> None:
        with self._lock:
            self.datasets[dataset_id] = frame

    def get_dataset(self, dataset_id: str) -> pd.DataFrame:
        with self._lock:
            if dataset_id not in self.datasets:
                raise KeyError(f"Dataset '{dataset_id}' not found")
            return self.datasets[dataset_id]

    def put_run(self, run: TrainingRun) -> None:
        with self._lock:
            self.runs[run.run_id] = run

    def get_run(self, run_id: str) -> TrainingRun:
        with self._lock:
            if run_id not in self.runs:
                raise KeyError(f"Run '{run_id}' not found")
            return self.runs[run_id]
