import os


from pydantic import BaseModel, Field


class EmailMessage(BaseModel):
    subject: str
    contents: str
    invalid_request: bool = Field(default=False)