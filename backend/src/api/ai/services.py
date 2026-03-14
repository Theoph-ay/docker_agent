from api.ai.llms import get_llm
from api.ai.schemas import EmailMessage

def generate_email(query: str):
    llm_base = get_llm()
    llm = llm_base.with_structured_output(EmailMessage)

    messages = [
        (
            "system",
            "You are a helpful assistant for researching and composing plain text emails. "
            "You MUST use the provided tool/schema to return the drafted email in the exact JSON format required. "
            "Do not return conversational text; return only the structured output."
        ),
        (
            "human",
            f"Draft an email about: {query}\n\n"
            "Remember: return ONLY the JSON representation of the email using the provided EmailMessage tool. Do not use markdown."
        )
    ]

    return llm.invoke(messages)