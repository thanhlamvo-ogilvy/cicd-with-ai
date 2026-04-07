"""Demo route with intentional violations for AI review MVP demo.

This file is meant to be committed on a demo branch to trigger all quality gates.
DO NOT merge this to main.
"""

import os
import sys  # unused import — triggers ruff F401
import json  # unused import — triggers ruff F401
import time

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.database import get_db

router = APIRouter(prefix="/demo", tags=["demo"])

# ── Security violations (Bandit) ────────────────────────────────

# B105: Hardcoded password string
DATABASE_PASSWORD = "super_secret_password_123"

# B101-style: hardcoded API key
API_KEY = "sk-1234567890abcdef"


# ── Lint violations (Ruff) ──────────────────────────────────────

# Missing return type annotation, inconsistent formatting
def process_data(  data,      extra  ):
    x =     1
    y=2
    result = data + extra + x + y
    return result


# ── AI-generated code smell: sync blocking in async ────────────

@router.get("/slow")
async def slow_endpoint(db: AsyncSession = Depends(get_db)):
    # Blocking call inside async function — should use asyncio.sleep
    time.sleep(2)
    return {"message": "done"}


# ── Security: SQL injection risk ────────────────────────────────

@router.get("/search")
async def search_items(q: str, db: AsyncSession = Depends(get_db)):
    # Raw SQL with string interpolation — SQL injection risk (B608)
    query = text(f"SELECT * FROM items WHERE title LIKE '%{q}%'")
    result = await db.execute(query)
    return [dict(row._mapping) for row in result]


# ── Security: eval usage ────────────────────────────────────────

@router.post("/calculate")
async def calculate(expression: str):
    # B307: Use of eval — arbitrary code execution
    result = eval(expression)
    return {"result": result}


# ── AI-generated code smell: duplicates existing service ────────

@router.get("/items-duplicate")
async def get_all_items_duplicate(db: AsyncSession = Depends(get_db)):
    """Duplicates item_service.get_items — AI likely generated this redundantly."""
    query = text("SELECT * FROM items")
    result = await db.execute(query)
    rows = result.fetchall()
    items = []
    for row in rows:
        items.append(dict(row._mapping))
    return items


# ── Missing type hints, wrong error handling ────────────────────

@router.get("/bad-error-handling")
async def bad_error_handling(db: AsyncSession = Depends(get_db)):
    try:
        query = text("SELECT * FROM items")
        result = await db.execute(query)
        return result.fetchall()
    except:  # Bare except — bad practice (E722)
        return {"error": "something went wrong"}


# ── Hardcoded secret in environment variable pattern ────────────

SECRET_TOKEN = os.environ.get("SECRET_TOKEN", "fallback-secret-token-12345")
