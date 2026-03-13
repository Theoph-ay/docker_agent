from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, DateTime

def get_utc_now():
    return datetime.now().replace(tzinfo=timezone.utc)

class ChatMessagePayload(SQLModel):
    #pydantic model
    #validation
    message: str

class ChatMessage(SQLModel, table=True):
    #Database table
    #saving, updating, getting, deleting
    id: int | None = Field(default=None, primary_key=True)
    message: str
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),
        primary_key=False,
        nullable=False
    )

class ChatMessageListItem(SQLModel):
    message: str
    created_at: datetime = Field(default=None)