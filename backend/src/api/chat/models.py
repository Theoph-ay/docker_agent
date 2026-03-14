from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, DateTime

def get_utc_now():
    return datetime.now().replace(tzinfo=timezone.utc)

class ChatSession(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default="New Chat")
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),
        nullable=False
    )

class ChatMessagePayload(SQLModel):
    #pydantic model
    #validation
    message: str
    session_id: int

class ChatMessage(SQLModel, table=True):
    #Database table
    #saving, updating, getting, deleting
    id: int | None = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="chatsession.id")
    message: str
    is_ai: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),
        nullable=False
    )

class ChatMessageListItem(SQLModel):
    id: int | None = None
    session_id: int | None = None
    message: str
    is_ai: bool = Field(default=False)
    created_at: datetime = Field(default=None)

class ChatSessionListItem(SQLModel):
    id: int
    name: str
    created_at: datetime