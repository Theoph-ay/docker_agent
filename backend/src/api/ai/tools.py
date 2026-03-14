from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from api.myemailer.sender import send_mail as execute_send_mail
from api.myemailer.inbox_reader import read_inbox
from api.ai.services import generate_email


@tool
def research_email(query:str, config: RunnableConfig, to_email:str=None):
    """
    Perform research based on the query, and optionally email the results.

    Arguments:
    - query: str - Topic of research
    - to_email: str - Optional. Email address to send the generated research to. If provided, the email is sent automatically.
    """
    # print(config)
    metadata = config.get('metadata')
    add_field = metadata.get("additional_field")
    print('add_field', add_field)
    try:
        response = generate_email(query)
        msg = f"Subject {response.subject}:\nBody: {response.contents}"
        if to_email:
            try:
                execute_send_mail(subject=response.subject, contents=response.contents, to_email=to_email)
                return f"Successfully researched and sent the email to {to_email}! \n\n{msg}"
            except Exception as e:
                return f"Researched successfully, but failed to send email: {e} \n\n{msg}"
        return msg 
    except Exception as e:
        print(f"Research email tool error: {e}")
        return f"Failed to generate structured email content due to error: {e}. Please try again or provide the research directly."

import traceback

@tool
def send_mail(subject:str, contents:str, to_email:str=None) -> str:
    """
    Send an email with a subject and content.

    Arguments:
    - subject: str - Text subject of the email
    - contents: str - Text body content of the email
    - to_email: str - Optional email address to send to. If not provided, it sends it to myself.
    """
    print(f"Executing send_mail tool... Subject: {subject}, To: {to_email}")
    try:
        if to_email:
            execute_send_mail(subject=subject, contents=contents, to_email=to_email)
        else:
            execute_send_mail(subject=subject, contents=contents)
    except Exception as e:
        print(f"Email error: {e}")
        traceback.print_exc()
        return f"Not sent: {e}"
    
    print("Email sent successfully from tool!")
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