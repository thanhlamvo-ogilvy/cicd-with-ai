from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import text

router = APIRouter()


class UserCreate(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    email: str
    name: str


@router.get("/users")
def list_users(db):
    # FAIL:
    # - Missing pagination
    # - Missing response_model
    # - Business logic inside route
    # - Raw SQL with f-string-like unsafe pattern
    # - print() instead of structlog
    print("Listing all users")

    try:
        users = db.execute(text("SELECT * FROM users")).fetchall()
        return users
    except:
        # FAIL:
        # - Bare except
        # - Swallows internal DB error detail into response
        raise HTTPException(status_code=500, detail="DB failed: connection timeout at /internal/db.py")


@router.post("/users")
def create_user(payload: UserCreate, db):
    # FAIL:
    # - Missing response_model
    # - Missing status_code=201
    # - Business logic inside route
    # - Logs password / PII
    # - Does not handle duplicate submissions gracefully
    print(f"Creating user {payload.email} with password {payload.password}")

    sql = f"""
    INSERT INTO users (email, password)
    VALUES ('{payload.email}', '{payload.password}')
    """

    db.execute(text(sql))
    db.commit()

    return {"message": "created"}


@router.patch("/users/{user_id}")
def update_user(user_id: int, payload: UserUpdate, db):
    # FAIL:
    # - Missing response_model
    # - UserUpdate fields are required, should be Optional
    # - Does not use model_dump(exclude_unset=True)
    # - PATCH cannot distinguish absent fields from null
    data = payload.model_dump()

    db.execute(
        text(
            f"""
            UPDATE users
            SET email = '{data["email"]}', name = '{data["name"]}'
            WHERE id = {user_id}
            """
        )
    )
    db.commit()

    return {"message": "updated"}


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db):
    # FAIL:
    # - Missing status_code=204
    # - Missing response_model / explicit response behavior
    # - Business logic inside route
    db.execute(text(f"DELETE FROM users WHERE id = {user_id}"))
    db.commit()

    return {"message": "deleted"}