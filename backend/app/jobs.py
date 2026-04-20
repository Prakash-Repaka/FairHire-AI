from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Callable
from uuid import uuid4


@dataclass(slots=True)
class JobRecord:
    job_id: str
    kind: str
    status: str = 'queued'
    message: str = 'Queued'
    result: dict[str, Any] | None = None
    error: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class JobManager:
    def __init__(self, max_workers: int = 4) -> None:
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._lock = Lock()
        self._jobs: dict[str, JobRecord] = {}

    def submit(self, kind: str, func: Callable[..., dict[str, Any]], *args: Any, **kwargs: Any) -> JobRecord:
        job = JobRecord(job_id=f'job_{uuid4().hex[:12]}', kind=kind)
        with self._lock:
            self._jobs[job.job_id] = job

        def _runner() -> None:
            self._update(job.job_id, status='running', message='Running')
            try:
                result = func(*args, **kwargs)
                self._update(job.job_id, status='completed', message='Completed', result=result)
            except Exception as exc:  # noqa: BLE001
                self._update(job.job_id, status='failed', message='Failed', error=str(exc))

        self._executor.submit(_runner)
        return job

    def get(self, job_id: str) -> JobRecord:
        with self._lock:
            if job_id not in self._jobs:
                raise KeyError(f"Job '{job_id}' not found")
            return self._jobs[job_id]

    def _update(self, job_id: str, **changes: Any) -> None:
        with self._lock:
            job = self._jobs[job_id]
            for key, value in changes.items():
                setattr(job, key, value)
            job.updated_at = datetime.now(timezone.utc).isoformat()
