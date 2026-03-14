from api.ai.llms import get_llm
from api.ai.schemas import EmailMessage

def generate_email(query: str):
    llm_base = get_llm()
    llm = llm_base.with_structured_output(EmailMessage)

    messages = [
        (
            "system",
            "You are an helpful assistant for a research composing plaintext emails. Do not use markdown in yout response"
        ),
        (
            "human",
            f"{query}" + "Do not use markdown in your response only plaintext"
        )
    ]

    return llm.invoke(messages)