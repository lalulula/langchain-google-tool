from dotenv import load_dotenv
from langchain_community.agent_toolkits.gmail.toolkit import GmailToolkit
from langchain_openai import AzureChatOpenAI
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from langgraph.prebuilt import create_react_agent

def send_email_tool(recipient_email, email_content, token_file="token.json", client_secrets_file="credentials.json"):
    """
    Sends an email using the Gmail API and a language model to generate the content.

    Parameters:
    - recipient_email (str): The email address of the recipient.
    - email_content (str): The content of the email to be sent.
    - token_file (str): Path to the token file for Gmail API credentials.
    - client_secrets_file (str): Path to the client secrets file for Gmail API credentials.

    Returns:
    - response: The response from the email sending process.
    """
    load_dotenv()

    credentials = get_gmail_credentials(
        token_file=token_file,
        scopes=["https://mail.google.com/"],
        client_secrets_file=client_secrets_file,
    )

    api_resource = build_resource_service(credentials=credentials)
    toolkit = GmailToolkit(api_resource=api_resource)
    llm = AzureChatOpenAI(temperature=0)

    email_prompt = f"""
    You are an assistant helping me write emails. 
    I want the recipient to be '{recipient_email}'.
    {email_content}
    """

    agent_executor = create_react_agent(llm, toolkit.get_tools())

    response = agent_executor.invoke({
        "messages": email_prompt 
    })

    return response


# 예시 사용
response = send_email_tool(
    recipient_email="ABCcompany@gmail.com",
    email_content="I want you to write an email thanking the client for their interest in our ESG solutions and offering a meeting to discuss how our product can meet their business needs."
)
print(response)
