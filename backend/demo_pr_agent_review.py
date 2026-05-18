"""
Order management endpoints — demo file for PR Agent review.

PR Agent should REQUEST CHANGES on this file.
Ruff, Bandit, and Mypy will all pass (they only scan app/).
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/demo/orders", tags=["demo"])


class OrderBase(BaseModel):
    product_id: int
    quantity: int
    customer_email: str


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int
    status: str


# SEMANTIC VIOLATIONS (linters cannot catch these):
#
# 1. No response_model declared on any endpoint
# 2. POST returns 200 (implicit), should return 201
# 3. Business logic (validation, ID generation) in route handler — should be in a service
# 4. print() used instead of structlog
# 5. f-string log formatting instead of structured key=value binding
# 6. customer_email (PII) written to log
# 7. GET /orders has no pagination (no limit/offset params)
# 8. DELETE returns {"deleted": True} with 200 instead of 204 No Content


@router.post("/")
async def create_order(payload: OrderCreate) -> dict:
    if payload.quantity <= 0:
        raise HTTPException(status_code=422, detail="quantity must be positive")
    if payload.quantity > 1000:
        raise HTTPException(status_code=422, detail="quantity exceeds limit")

    order_id = abs(hash(f"{payload.product_id}-{payload.customer_email}")) % 100000
    print(f"Created order {order_id} for customer {payload.customer_email}")

    return {
        "id": order_id,
        "product_id": payload.product_id,
        "quantity": payload.quantity,
        "customer_email": payload.customer_email,
        "status": "pending",
    }


@router.get("/")
async def list_orders() -> list[dict]:
    print("Fetching all orders")
    return []


@router.delete("/{order_id}")
async def delete_order(order_id: int) -> dict:
    print(f"Deleted order {order_id}")
    return {"deleted": True}
