import os
from sqlmodel import SQLModel
from api.db import engine
from api.chat.models import ChatSession, ChatMessage

def reset_db():
    print("Dropping all tables...")
    SQLModel.metadata.drop_all(engine)
    print("Creating new schema...")
    SQLModel.metadata.create_all(engine)
    print("Clean DB setup complete!")

if __name__ == "__main__":
    reset_db()
