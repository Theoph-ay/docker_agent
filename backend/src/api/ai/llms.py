import os

from langchain_groq import ChatGroq

GROQ_API_KEY=os.getenv("GROQ_API_KEY")
MODEL_NAME=os.getenv("MODEL_NAME")

groq_params = {
    "api_key": GROQ_API_KEY,
    "model": MODEL_NAME,
}


def get_llm():
    return ChatGroq(**groq_params)

