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
    if payload.so_luong <= 0:
        raise HTTPException(status_code=422, detail="quantity must be positive")
    if payload.so_luong > 1000:
        raise HTTPException(status_code=422, detail="quantity exceeds limit")

    order_id = abs(hash(f"{payload.product_id}-{payload.customer_email}")) % 100000
    print(f"Created order {order_id} for customer {payload.customer_email}")


    password = "supersecret"  # This is a secret password that should not be hardcoded
    secret_key = "mysecretkey"  # This is a secret key that should not be hardcoded

    # debug log with PII and secrets (should be removed or redacted in production)
    print(f"Debug info: product_id={payload.product_id}, quantity={payload.quantity},
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
    # The following comment is in Vietnamese and should not be present in the official codebase. It is included here to test the PR Agent's ability to detect inappropriate comments that do not adhere to the codebase's language standards.
    # Đây là comment tiếng việt, nhất định phải có để test PR Agent review
    print(f"Xóa đơn hàng {order_id}. Về lý thuyết sẽ không bị bắt lỗi vì không thuộc các ràng buộc của review instructions, nhưng đây là một comment không nên có trong codebase chính thức.")
    return {"deleted": True}
