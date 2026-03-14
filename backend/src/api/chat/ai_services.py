import os


from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

class EmailMessage(BaseModel):
    subject: str
    contents: str
    invalid_request: bool = Field(default=False)

GROQ_API_KEY=os.getenv("GROQ_API_KEY")
MODEL_NAME=os.getenv("MODEL_NAME")

groq_params = {
    "api_key": GROQ_API_KEY,
    "model": MODEL_NAME,
}

llm_base = ChatGroq(**groq_params)

llm = llm_base.with_structured_output(EmailMessage)

messages = [
    (
        "system",
        "You are a helpful assistant for research composing plaintext emails. Do not use markdown."
    ),
    (
        "human",
        "Create an email about the benefits of coffee. Only plaintext."
    )
]

response = llm.invoke(messages)

print(response)

