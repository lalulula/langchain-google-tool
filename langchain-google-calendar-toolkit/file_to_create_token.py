from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle

# If modifying scopes, delete the token.json file
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Save the credentials for future use
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Test: list upcoming 10 events
    events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"{start}: {event['summary']}")

if __name__ == '__main__':
    main()

