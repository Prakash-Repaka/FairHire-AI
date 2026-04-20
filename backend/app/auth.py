from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import HTTPException, status


def _get_secret() -> bytes:
    secret = os.getenv('FIREHIRE_AUTH_SECRET') or os.getenv('SECRET_KEY') or 'fairhire-dev-secret'
    return secret.encode('utf-8')


def hash_password(password: str, salt: bytes | None = None) -> dict[str, str]:
    salt_bytes = salt or secrets.token_bytes(16)
    hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_bytes, 390_000)
    return {
        'salt': base64.urlsafe_b64encode(salt_bytes).decode('ascii'),
        'hash': base64.urlsafe_b64encode(hash_bytes).decode('ascii'),
    }


def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    salt_bytes = base64.urlsafe_b64decode(salt.encode('ascii'))
    expected = base64.urlsafe_b64decode(stored_hash.encode('ascii'))
    candidate = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_bytes, 390_000)
    return hmac.compare_digest(candidate, expected)


def issue_token(subject: str, expires_minutes: int = 120) -> str:
    payload = {
        'sub': subject,
        'exp': (datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)).timestamp(),
        'iat': datetime.now(timezone.utc).timestamp(),
    }
    payload_bytes = json.dumps(payload, separators=(',', ':'), sort_keys=True).encode('utf-8')
    payload_part = base64.urlsafe_b64encode(payload_bytes).decode('ascii').rstrip('=')
    signature = hmac.new(_get_secret(), payload_part.encode('ascii'), hashlib.sha256).digest()
    signature_part = base64.urlsafe_b64encode(signature).decode('ascii').rstrip('=')
    return f'{payload_part}.{signature_part}'


def decode_token(token: str) -> dict[str, Any]:
    try:
        payload_part, signature_part = token.split('.', 1)
        expected_signature = hmac.new(_get_secret(), payload_part.encode('ascii'), hashlib.sha256).digest()
        provided_signature = base64.urlsafe_b64decode(signature_part + '==')
        if not hmac.compare_digest(expected_signature, provided_signature):
            raise ValueError('Invalid token signature')
        payload_bytes = base64.urlsafe_b64decode(payload_part + '==')
        payload = json.loads(payload_bytes.decode('utf-8'))
        if float(payload.get('exp', 0)) < datetime.now(timezone.utc).timestamp():
            raise ValueError('Token expired')
        return payload
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid authentication token') from exc


@dataclass(slots=True)
class AuthenticatedUser:
    user_id: str
    employee_id: str
    email: str
    name: str
    role: str
    created_at: str
