"""Demo route with intentional violations for AI review MVP demo.

This file is meant to be committed on a demo branch to trigger all quality gates.
DO NOT merge this to main.
"""

import asyncio
import os
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import exc, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

router = APIRouter(prefix="/demo", tags=["demo"])

# ── Security: Proper environment variable handling ──────────────────────

DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
if not DATABASE_PASSWORD:
    raise ValueError("DATABASE_PASSWORD environment variable must be set")

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable must be set")


# ── Lint violations (Ruff) ──────────────────────────────────────


def process_data(data: int, extra: int) -> int:
    """Process data by summing inputs with constants.

    Args:
        data: First input value.
        extra: Second input value.

    Returns:
        Sum of data, extra, and constants.
    """
    const_sum = 3  # 1 + 2
    return data + extra + const_sum


# ── AI-generated code smell: sync blocking in async ────────────


@router.get("/slow")
async def slow_endpoint(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Demonstrate async operation without blocking."""
    await asyncio.sleep(2)
    return {"message": "done"}


# ── Security: SQL injection risk ────────────────────────────────


@router.get("/search")
async def search_items(q: str, db: AsyncSession = Depends(get_db)) -> list[dict[str, Any]]:
    """Search items with parameterized query to prevent SQL injection."""
    query = text("SELECT * FROM items WHERE title LIKE :search_term")
    result = await db.execute(query, {"search_term": f"%{q}%"})
    return [dict(row._mapping) for row in result]


# ── Security: eval usage ────────────────────────────────────────


@router.post("/calculate")
async def calculate(expression: str) -> dict[str, Any]:
    """Evaluate simple arithmetic (safe subset only).

    Args:
        expression: Arithmetic expression with +, -, *, / only.

    Returns:
        Dictionary with result or error message.
    """
    # Security: Only allow safe arithmetic operations
    import ast
    import operator

    # Whitelist allowed operations
    allowed_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    try:
        tree = ast.parse(expression, mode="eval")
        # Validate only numbers and allowed operations
        for node in ast.walk(tree):
            if not isinstance(
                node,
                (
                    ast.Expression,
                    ast.BinOp,
                    ast.Constant,
                    ast.Add,
                    ast.Sub,
                    ast.Mult,
                    ast.Div,
                ),
            ):
                raise ValueError("Only arithmetic operations allowed")

        # Evaluate safely with restricted operators
        def eval_node(node: Any) -> Any:  # noqa: ANN401
            if isinstance(node, ast.Constant):
                return node.value
            if isinstance(node, ast.BinOp):
                left = eval_node(node.left)
                right = eval_node(node.right)
                op = allowed_ops.get(type(node.op))
                if op is None:
                    raise ValueError("Operation not allowed")
                return op(left, right)
            raise ValueError("Invalid expression")

        result = eval_node(tree.body)
        return {"result": result}
    except (ValueError, SyntaxError, ZeroDivisionError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


# ── AI-generated code smell: duplicates existing service ────────


# DEPRECATED: This endpoint was removed to eliminate code duplication.
# Use the standardized item_service.get_items() via /items endpoint instead.


# ── Missing type hints, wrong error handling ────────────────────


@router.get("/bad-error-handling")
async def bad_error_handling(
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, Any]]:
    """Handle database errors explicitly with specific exception types."""
    try:
        query = text("SELECT * FROM items")
        result = await db.execute(query)
        return [dict(row._mapping) for row in result.fetchall()]
    except exc.SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database query failed") from e


# ── Environment variable with no fallback (no hardcoded secrets) ─────────

SECRET_TOKEN = os.environ.get("SECRET_TOKEN")
if not SECRET_TOKEN:
    raise ValueError("SECRET_TOKEN environment variable must be set")
