"""Tests for security utilities: password hashing and JWT token handling."""

from datetime import timedelta

from jose import jwt

from app.core.config import settings
from app.core.security import (
    ALGORITHM,
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)


def test_get_password_hash_differs_from_plaintext() -> None:
    hashed = get_password_hash("mysecretpassword")
    assert hashed != "mysecretpassword"
    assert len(hashed) > 20


def test_verify_password_correct() -> None:
    hashed = get_password_hash("correct-horse-battery")
    assert verify_password("correct-horse-battery", hashed) is True


def test_verify_password_wrong() -> None:
    hashed = get_password_hash("correct-horse-battery")
    assert verify_password("wrong-password", hashed) is False


def test_create_and_decode_access_token() -> None:
    token = create_access_token("user-42")
    payload = decode_access_token(token)
    assert payload["sub"] == "user-42"


def test_create_access_token_with_custom_expiry() -> None:
    token = create_access_token("user-99", expires_delta=timedelta(hours=2))
    payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    assert payload["sub"] == "user-99"
