from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from .models import ChatMessagePayload, ChatMessage, ChatMessageListItem
from api.db import get_session

from api.ai.agents import get_supervisor
from api.ai.schemas import EmailMessage, SupervisorMessage

from api.ai.services import generate_email

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
@router.post("/")
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
    supe = get_supervisor()
    msg_data = {
        "messages": [
            {
                "role": "user", 
                "content": payload.message
            }
        ]
    }
    
    config = {"configurable": {"thread_id": "main"}}
    result = supe.invoke(msg_data, config)
    # Extract the last AI/assistant message from the supervisor result
    messages = result.get("messages", [])
    ai_response = ""
    for msg in reversed(messages):
        role = getattr(msg, "type", None) or getattr(msg, "role", None)
        if role in ("ai", "assistant"):
            ai_response = msg.content
            break
    if not ai_response:
        raise HTTPException(status_code=400, detail="No response from AI")
    return {"response": ai_response}