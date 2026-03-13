from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from .models import ChatMessagePayload, ChatMessage, ChatMessageListItem
from api.db import get_session


router = APIRouter()

#/api/chats
@router.get("/")
def chat_health():
    return {"status": "ok"}


#/api/chats/recent
@router.get("/recent", response_model=List[ChatMessageListItem])
def chat_list_messages(session: Session = Depends(get_session)):
    query = select(ChatMessage)
    results = session.exec(query).fetchall()[:10]
    return results


#HTTP POST
# curl -X POST -d '{"message": "Hello world"}' -H "Content-Type: application/json" "http://localhost:8000/api/chats"
@router.post("/", response_model=ChatMessage)
def chat_create_message(
    payload:ChatMessagePayload,
    session: Session = Depends(get_session)
):
    data = payload.model_dump()
    print(data)
    obj = ChatMessage.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    #Store in database
    return obj