from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from api.myemailer.sender import send_mail as execute_send_mail
from api.myemailer.inbox_reader import read_inbox
from api.ai.services import generate_email


@tool
def research_email(query:str, config: RunnableConfig):
    """
    Perform research based on the query

    Arguments:
    - query: str - Topic of research
    """
    # print(config)
    metadata = config.get('metadata')
    add_field = metadata.get("additional_field")
    print('add_field', add_field)
    try:
        response = generate_email(query)
        msg = f"Subject {response.subject}:\nBody: {response.contents}"
        return msg 
    except Exception as e:
        print(f"Research email tool error: {e}")
        return f"Failed to generate structured email content due to error: {e}. Please try again or provide the research directly."

import traceback

@tool
def send_mail(subject:str, contents:str) -> str:
    """
    Send an email to myself with a subject and content.

    Arguments:
    - subject: str - Text subject of the email
    - contents: str - Text body content of the email
    """
    try:
        execute_send_mail(subject=subject, contents=contents)
    except Exception as e:
        print(f"Email error: {e}")
        traceback.print_exc()
        return f"Not sent: {e}"
    return "Sent email"


@tool
def get_unread_emails(hours_ago:int=48) -> str:
    """
    Read all emails from my inbox within the last N hours

    Arguments:
    - hours_ago: int = 24 - number of hours ago to retrieve in the inbox
    
    Returns:
    A string of emails separated by a line "----"
    """
    try:
        emails = read_inbox(hours_ago=hours_ago, verbose=False)
    except:
        return "Error getting latest emails"
    cleaned = []
    for email in emails:
        data = email.copy()
        if "html_body" in data:
            data.pop('html_body')
        msg = ""
        for k, v in data.items():
            msg += f"{k}:\t{v}"
        cleaned.append(msg)
    return "\n-----\n".join(cleaned)[:500]