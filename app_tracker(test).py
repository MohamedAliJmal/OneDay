import datetime
import pickle
import os.path
import time
import pygetwindow as gw
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def create_event(service, start_time, end_time, summary, description):
    event = {
        'summary': summary,
        'description': description,
        'start': {'dateTime': start_time},
        'end': {'dateTime': end_time},
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')

def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    print("Tracking active application... (Press Ctrl+C to stop)")
    try:
        start_time = None
        while True:
            active_app_title = gw.getActiveWindow().title
            if active_app_title:
                if start_time is None:
                    start_time = datetime.datetime.now()
                elif gw.getActiveWindow().title != active_app_title:
                    end_time = datetime.datetime.now()
                    duration = end_time - start_time

                    summary = active_app_title
                    description = f"Time spent: {duration}"
                    event_start = start_time.isoformat()
                    event_end = end_time.isoformat()

                    create_event(service, event_start, event_end, summary, description)

                    print(f"Event created for {active_app_title} - Duration: {duration}")
                    start_time = None
            else:
                start_time = None

            time.sleep(5) 
    except KeyboardInterrupt:
        print("Tracking stopped.")

if __name__ == "__main__":
    main()
