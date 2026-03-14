from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy import desc
from .models import ChatMessagePayload, ChatMessage, ChatMessageListItem, ChatSession, ChatSessionListItem
from api.db import get_session

from api.ai.agents import get_supervisor

router = APIRouter()

#/api/chats
@router.get("/")
def chat_health():
    return {"status": "ok"}

# --- Sessions Endpoints ---

@router.get("/sessions", response_model=List[ChatSessionListItem])
def list_sessions(session: Session = Depends(get_session)):
    query = select(ChatSession).order_by(desc(ChatSession.created_at))
    results = session.exec(query).fetchall()
    return results

@router.post("/sessions", response_model=ChatSessionListItem)
def create_session(session: Session = Depends(get_session)):
    new_session = ChatSession(name="New Chat")
    session.add(new_session)
    session.commit()
    session.refresh(new_session)
    return new_session

@router.delete("/sessions/{session_id}")
def delete_session(session_id: int, session: Session = Depends(get_session)):
    obj = session.get(ChatSession, session_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Delete associated messages
    msgs = session.exec(select(ChatMessage).where(ChatMessage.session_id == session_id)).fetchall()
    for msg in msgs:
        session.delete(msg)
        
    session.delete(obj)
    session.commit()
    return {"status": "deleted"}

@router.put("/sessions/{session_id}", response_model=ChatSessionListItem)
def update_session(session_id: int, payload: dict, session: Session = Depends(get_session)):
    obj = session.get(ChatSession, session_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if "name" in payload:
        obj.name = payload["name"]
        
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


# --- Messages Endpoints ---

@router.get("/{session_id}/recent", response_model=List[ChatMessageListItem])
def chat_list_messages(session_id: int, session: Session = Depends(get_session)):
    query = select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc())
    results = session.exec(query).fetchall()
    return results[-50:] if len(results) > 50 else results

@router.post("/")
def chat_create_message(
    payload: ChatMessagePayload,
    session: Session = Depends(get_session)
):
    session_id = payload.session_id
    chat_session = session.get(ChatSession, session_id)
    if not chat_session:
        raise HTTPException(status_code=404, detail="Session not found")

    data = payload.model_dump()
    obj = ChatMessage.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)

    # Rename session lazily if it's the first message
    if chat_session.name == "New Chat":
        words = payload.message.split()
        chat_session.name = " ".join(words[:5]) + ("..." if len(words) > 5 else "")
        session.add(chat_session)
        session.commit()

    # Get the last 5 messages for context
    query = select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(desc(ChatMessage.created_at)).limit(5)
    recent_msgs = session.exec(query).fetchall()
    recent_msgs.reverse() # chronological order for memory

    messages_payload = []
    for msg in recent_msgs:
        role = "assistant" if msg.is_ai else "user"
        messages_payload.append({
            "role": role,
            "content": msg.message
        })

    msg_data = {
        "messages": messages_payload
    }

    supe = get_supervisor()
    config = {"configurable": {"thread_id": str(session_id)}}
    result = supe.invoke(msg_data, config)
    
    # Extract AI response
    messages = result.get("messages", [])
    ai_response = ""
    for msg in reversed(messages):
        role = getattr(msg, "type", None) or getattr(msg, "role", None)
        if role in ("ai", "assistant"):
            ai_response = msg.content
            break
            
    if not ai_response:
        raise HTTPException(status_code=400, detail="No response from AI")
    
    # Log the AI reply into the database
    ai_msg_obj = ChatMessage(session_id=session_id, message=ai_response, is_ai=True)
    session.add(ai_msg_obj)
    session.commit()
    
    return {"response": ai_response}