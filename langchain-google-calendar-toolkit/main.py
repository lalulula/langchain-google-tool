import os
from dotenv import load_dotenv
from pathlib import Path
from file_to_create_token import main as file_to_create_token
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.agents import tool
import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from langchain_core.prompts import PromptTemplate

load_dotenv()

@tool
def search_google_calendar_events(start_date: str, end_date: str) -> str:
    """
    This tool searches Google Calendar for events between the specified start and end dates.
    Returns event details as a string.
    """

    creds = Credentials.from_authorized_user_file("token.json")

    
    service = build("calendar", "v3", credentials=creds)
    
    calendar_id = "iesg.poscointl@gmail.com"
    
    start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d").isoformat() + 'Z'
    end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d").isoformat() + 'Z'

    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_datetime,
        timeMax=end_datetime,
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    
    events = events_result.get("items", [])
    print(events)
    if not events:
        return "No events found in the specified date range."
    
    event_details = []
    for event in events:
        event_start = event['start'].get('dateTime', event['start'].get('date'))
        event_summary = event.get('summary', "No title")
        event_details.append(f"{event_start}: {event_summary}")
    
    return "\n".join(event_details)

def execute_agent(start_date, end_date):
    llm = AzureChatOpenAI(deployment_name="gpt-4.1", temperature=0.2)
    tools = [search_google_calendar_events]
    template = """
    You are a helpful assistant. When the user asks for events, search Google Calendar for the relevant date range.
    The current state of the agent is:
    {agent_scratchpad}

    ### Data range
    start_date:{start_date}
    end_date:{end_date}

    Your task is to find the events in the given date range, based on the user's request. 
    Use the tool 'search_google_calendar_events' to fetch the events. 
    Ensure you extract the date range from the user's input and pass it to the tool. 
    Provide the event details in the following format:
    Event Start Time: Event Title
    """
    prompt = PromptTemplate.from_template(template)

    agent = create_tool_calling_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        max_execution_time=10,
        handle_parsing_errors=True,
    )

    user_input = {"start_date": start_date, "end_date": end_date}
    try:
        result = agent_executor.invoke(user_input)
        print("Agent executed result:")
        print(result["output"])
    except Exception as e:
        print(f"Error during agent execution: {e}")

if __name__ == "__main__":
    if not Path("token.json").exists():
        file_to_create_token()
    execute_agent("2025-05-01", "2025-05-02")
