from __future__ import annotations

import os
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

MAX_UPLOAD_BYTES = int(os.getenv('FAIRHIRE_MAX_UPLOAD_BYTES', str(10 * 1024 * 1024)))
ALLOWED_EXTENSIONS = {'.csv', '.json', '.xlsx', '.xls'}
ALLOWED_CONTENT_TYPES = {
    'text/csv',
    'application/csv',
    'application/json',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/octet-stream',
}


def validate_upload(file: UploadFile, content: bytes) -> None:
    suffix = Path(file.filename or '').suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail='Unsupported file format. Use CSV, JSON, or XLSX.')

    if file.content_type and file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail='Unsupported content type for upload.')

    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Uploaded file is empty')

    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=f'File exceeds maximum size of {MAX_UPLOAD_BYTES} bytes')
