from __future__ import annotations

import json
import pickle
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1] / 'data'
DATASETS_DIR = BASE_DIR / 'datasets'
RUNS_DIR = BASE_DIR / 'runs'
STATE_FILE = BASE_DIR / 'state.json'


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
        self.users: dict[str, dict[str, Any]] = {}
        BASE_DIR.mkdir(parents=True, exist_ok=True)
        DATASETS_DIR.mkdir(parents=True, exist_ok=True)
        RUNS_DIR.mkdir(parents=True, exist_ok=True)
        self._state = self._load_state()

    def _load_state(self) -> dict[str, Any]:
        if not STATE_FILE.exists():
            return {'datasets': {}, 'runs': {}, 'users': {}}
        try:
            with STATE_FILE.open('r', encoding='utf-8') as file:
                return json.load(file)
        except Exception:
            return {'datasets': {}, 'runs': {}, 'users': {}}

    def _save_state(self) -> None:
        with STATE_FILE.open('w', encoding='utf-8') as file:
            json.dump(self._state, file, indent=2)

    def put_dataset(self, dataset_id: str, frame: pd.DataFrame, metadata: dict[str, Any] | None = None) -> None:
        with self._lock:
            self.datasets[dataset_id] = frame
            dataset_path = DATASETS_DIR / f'{dataset_id}.csv'
            frame.to_csv(dataset_path, index=False)
            self._state.setdefault('datasets', {})[dataset_id] = {
                'dataset_id': dataset_id,
                'rows': int(frame.shape[0]),
                'columns': list(frame.columns),
                'metadata': metadata or {},
                'path': str(dataset_path.relative_to(BASE_DIR)),
            }
            self._save_state()

    def get_dataset(self, dataset_id: str) -> pd.DataFrame:
        with self._lock:
            if dataset_id in self.datasets:
                return self.datasets[dataset_id]

            dataset_info = self._state.get('datasets', {}).get(dataset_id)
            if not dataset_info:
                raise KeyError(f"Dataset '{dataset_id}' not found")

            dataset_path = BASE_DIR / dataset_info['path']
            if not dataset_path.exists():
                raise KeyError(f"Dataset '{dataset_id}' file is missing")

            frame = pd.read_csv(dataset_path)
            self.datasets[dataset_id] = frame
            return frame

    def put_run(self, run: TrainingRun) -> None:
        with self._lock:
            self.runs[run.run_id] = run
            run_path = RUNS_DIR / f'{run.run_id}.pkl'
            with run_path.open('wb') as file:
                pickle.dump(run, file)
            self._state.setdefault('runs', {})[run.run_id] = {
                'run_id': run.run_id,
                'dataset_id': run.dataset_id,
                'model_type': run.model_type,
                'target_column': run.target_column,
                'created_at': run.created_at.isoformat(),
                'metrics': run.metrics,
                'path': str(run_path.relative_to(BASE_DIR)),
            }
            self._save_state()

    def get_run(self, run_id: str) -> TrainingRun:
        with self._lock:
            if run_id in self.runs:
                return self.runs[run_id]

            run_info = self._state.get('runs', {}).get(run_id)
            if not run_info:
                raise KeyError(f"Run '{run_id}' not found")

            run_path = BASE_DIR / run_info['path']
            if not run_path.exists():
                raise KeyError(f"Run '{run_id}' file is missing")

            with run_path.open('rb') as file:
                run = pickle.load(file)
            self.runs[run_id] = run
            return run

    def put_user(self, user_record: dict[str, Any]) -> None:
        email = user_record['email'].lower()
        with self._lock:
            self.users[email] = user_record
            self._state.setdefault('users', {})[email] = user_record
            self._save_state()

    def get_user(self, email: str) -> dict[str, Any] | None:
        email = email.lower()
        with self._lock:
            if email in self.users:
                return self.users[email]
            user = self._state.get('users', {}).get(email)
            if user:
                self.users[email] = user
            return user

    def list_runs(self) -> list[dict[str, Any]]:
        return list(self._state.get('runs', {}).values())

    def list_datasets(self) -> list[dict[str, Any]]:
        return list(self._state.get('datasets', {}).values())
        with STATE_FILE.open('w', encoding='utf-8') as file:
            json.dump(self._state, file, indent=2)

    def put_dataset(self, dataset_id: str, frame: pd.DataFrame, metadata: dict[str, Any] | None = None) -> None:
        with self._lock:
            self.datasets[dataset_id] = frame
            dataset_path = DATASETS_DIR / f'{dataset_id}.csv'
            frame.to_csv(dataset_path, index=False)
            self._state.setdefault('datasets', {})[dataset_id] = {
                'dataset_id': dataset_id,
                'rows': int(frame.shape[0]),
                'columns': list(frame.columns),
                'metadata': metadata or {},
                'path': str(dataset_path.relative_to(BASE_DIR)),
            }
            self._save_state()

    def get_dataset(self, dataset_id: str) -> pd.DataFrame:
        with self._lock:
            if dataset_id in self.datasets:
                return self.datasets[dataset_id]

            dataset_info = self._state.get('datasets', {}).get(dataset_id)
            if not dataset_info:
                raise KeyError(f"Dataset '{dataset_id}' not found")

            dataset_path = BASE_DIR / dataset_info['path']
            if not dataset_path.exists():
                raise KeyError(f"Dataset '{dataset_id}' file is missing")

            frame = pd.read_csv(dataset_path)
            self.datasets[dataset_id] = frame
            return frame

    def put_run(self, run: TrainingRun) -> None:
        with self._lock:
            self.runs[run.run_id] = run
            run_path = RUNS_DIR / f'{run.run_id}.pkl'
            with run_path.open('wb') as file:
                pickle.dump(run, file)
            self._state.setdefault('runs', {})[run.run_id] = {
                'run_id': run.run_id,
                'dataset_id': run.dataset_id,
                'model_type': run.model_type,
                'target_column': run.target_column,
                'created_at': run.created_at.isoformat(),
                'metrics': run.metrics,
                'path': str(run_path.relative_to(BASE_DIR)),
            }
            self._save_state()

    def get_run(self, run_id: str) -> TrainingRun:
        with self._lock:
            if run_id in self.runs:
                return self.runs[run_id]

            run_info = self._state.get('runs', {}).get(run_id)
            if not run_info:
                raise KeyError(f"Run '{run_id}' not found")

            run_path = BASE_DIR / run_info['path']
            if not run_path.exists():
                raise KeyError(f"Run '{run_id}' file is missing")

            with run_path.open('rb') as file:
                run = pickle.load(file)
            self.runs[run_id] = run
            return run

    def put_user(self, user_record: dict[str, Any]) -> None:
        email = user_record['email'].lower()
        with self._lock:
            self.users[email] = user_record
            self._state.setdefault('users', {})[email] = user_record
            self._save_state()

    def get_user(self, email: str) -> dict[str, Any] | None:
        email = email.lower()
        with self._lock:
            if email in self.users:
                return self.users[email]
            user = self._state.get('users', {}).get(email)
            if user:
                self.users[email] = user
            return user

    def list_runs(self) -> list[dict[str, Any]]:
        return list(self._state.get('runs', {}).values())

    def list_datasets(self) -> list[dict[str, Any]]:
        return list(self._state.get('datasets', {}).values())
