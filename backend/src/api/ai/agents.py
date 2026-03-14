from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

from api.ai.llms import get_llm

from api.ai.tools import (
    send_mail,
    get_unread_emails,
    research_email
)

EMAIL_TOOLS_LIST = [
    send_mail,
    get_unread_emails
]


def get_email_agent():
    model = get_llm()
    agent = create_react_agent(
        model=model,  
        tools=EMAIL_TOOLS_LIST,  
        prompt="You are a helpful assistant for managing my email inbox for generating, sending, and reviewing emails.",
        name="email_agent"
    )

    return agent


def get_research_agent():
    model = get_llm()
    agent = create_react_agent(
        model=model,  
        tools=[research_email],
        prompt="You are a helpful research assistant for preparing email data",
        name='research_agent',
    )

    return agent

# Removed MemorySaver to manually manage token limits via API instead.

def get_supervisor():
    llm = get_llm()
    email_agent = get_email_agent()
    research_agent = get_research_agent()

    supe = create_supervisor(
        agents=[email_agent, research_agent],
        model = llm,
         prompt=(
            "You manage a research assistant and an "
            "email inbox manager assistant. Assign work to them. "
            "CRITICAL: If the user asks you to send an email, you MUST "
            "instruct the email_agent to invoke the send_mail tool. Do not just "
            "give the user a draft to copy/paste if they explicitly asked you to send it."
        ),
       
    ).compile()
    return supe