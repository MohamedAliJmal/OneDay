import datetime
import pickle
import os.path
import time
import pygetwindow as gw
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


""" def track_app(app_name):
    print(f"Tracking {app_name}... (Press Ctrl+C to stop)")
    try:
        sessions = []
        while True:
            l=psutil.process_iter(attrs=["name"])
            current_state = any(p.info["name"] == app_name for p in psutil.process_iter(attrs=["name"]))
            if current_state and not sessions:
                sessions.append(time.time())  # Start new session
                print(f"{app_name} was opened.")
            elif not current_state and sessions:
                sessions.append(time.time())  # End session
                duration = sessions[1] - sessions[0]
                print(f"{app_name} was closed. Session duration: {duration:.2f} seconds.")
                sessions.clear()
            time.sleep(1)  # Adjust the interval (in seconds) as needed
    except KeyboardInterrupt:
        if sessions:
            print("Tracking stopped while the app is open. Closing the session.")
            sessions.append(time.time())  # End session
            duration = sessions[1] - sessions[0]
            print(f"Session duration: {duration:.2f} seconds.")
        print("Tracking stopped.") """

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def connect():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_414035138371-k0hvrbe8tdlfr7narq6k3mvp4mhvcbnm.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_event(service, start_time, end_time, summary):
    event = {
        'summary': summary,
        'start': {'dateTime': start_time},
        'end': {'dateTime': end_time},
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')


def get_active_app_title():
    try:
        active_app = gw.getActiveWindow()
        return active_app.title if active_app else None
    except gw.PyGetWindowException:
        return None






def main():


    creds=connect()
    service=build('calendar','v3',credentials=creds)

    print("Tracking active application... (Press Ctrl+C to stop)")
    try:
        while True:
            active_app_title = get_active_app_title()
            if active_app_title:
                start_time=datetime.datetime.now()
                
                while(active_app_title==get_active_app_title()): 
                    continue

                end_time=datetime.datetime.now()
                create_event(service,start_time,end_time,active_app_title)
            
            else:
                print("No active application.")
                while(not active_app_title): active_app_title=get_active_app_title() 
            
            
    except KeyboardInterrupt:
        print("Tracking stopped.")

if __name__ == "__main__":

    main()
