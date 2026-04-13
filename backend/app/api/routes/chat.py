import json
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.chat import ChatRequest
from app.services import chat_service

router = APIRouter(prefix="/chat", tags=["chat"])

DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.post("")
async def chat(request: ChatRequest, db: DbSession) -> StreamingResponse:
    # Resolve conversation before streaming so we can send the ID first
    conversation = await chat_service.get_or_create_conversation(db, request)
    conversation_id = str(conversation.id)

    async def event_stream() -> ...:  # type: ignore[override]
        # Send conversation ID as first event
        yield f"data: {json.dumps({'conversation_id': conversation_id})}\n\n"

        async for token in chat_service.stream_chat_response(db, request, conversation):
            yield f"data: {json.dumps({'token': token})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
