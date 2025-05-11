from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from .database import ChatDatabase

router = APIRouter()
db = ChatDatabase()

class ChatMessage(BaseModel):
    user_message: str
    assistant_message: str

class ChatHistoryResponse(BaseModel):
    user_message: str
    assistant_message: str
    timestamp: str

@router.post("/chat/save")
async def save_message(message: ChatMessage):
    try:
        db.save_message(message.user_message, message.assistant_message)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history", response_model=List[ChatHistoryResponse])
async def get_chat_history():
    try:
        messages = db.get_chat_history()
        return [
            ChatHistoryResponse(
                user_message=msg[0],
                assistant_message=msg[1],
                timestamp=msg[2]
            )
            for msg in messages
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 