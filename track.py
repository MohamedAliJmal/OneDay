import datetime
import pickle
import os.path
import time
import pygetwindow as gw
import tzlocal 
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

MINIMUM_DURATION = datetime.timedelta(minutes=1) 




def convert_to_RFC_datetime(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")



def get_timezone():
    local_tz = tzlocal.get_localzone()
    local_tzname = local_tz.tzname(datetime.datetime.now(local_tz))
    return local_tzname



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
                'client_secret_921474185101-mit5b1k7sn4fej7n45k7bklbe8aqchh6.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event(service, start_time, end_time, summary):
    event = {
        'summary': summary,
        'description': "",
        'start': {'dateTime': convert_to_RFC_datetime(start_time), "timezone":get_timezone()},
        'end': {'dateTime': convert_to_RFC_datetime(end_time), "timezone": get_timezone()},
    }
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event_result.get("htmlLink")}')

def get_active_app_title():
    try:
        active_app = gw.getActiveWindow()
        return active_app.title if active_app else None
    except gw.PyGetWindowException:
        return None

def get_timezone():
    local_tz = tzlocal.get_localzone()
    local_tzname = local_tz.tzname(datetime.datetime.now(local_tz))
    return local_tzname

def main():
    service = connect()
    local_tz = tzlocal.get_localzone()  

    print(f"Tracking active application... Press CTRL+C to Stop")
    
    active_app_title = None
    start_time = None
    
    try:
        while True:
            current_active_app_title = get_active_app_title()
            
            if current_active_app_title != active_app_title:
                if active_app_title and start_time:
                    end_time = datetime.datetime.now(local_tz)
                    duration = end_time - start_time
                    if duration >= MINIMUM_DURATION:
                        create_event(service, start_time, end_time, active_app_title)
                        print(f"Event created for {active_app_title} - Duration: {duration}")
                
                active_app_title = current_active_app_title
                start_time = datetime.datetime.now(local_tz)
            
            time.sleep(1)  
            
    except KeyboardInterrupt:
        if active_app_title and start_time:
            end_time = datetime.datetime.now(local_tz)
            duration = end_time - start_time
            if duration >= MINIMUM_DURATION:
                create_event(service, start_time, end_time, active_app_title)
                print(f"Event created for {active_app_title} - Duration: {duration}")
        
        print("Tracking stopped.")

if __name__ == "__main__":
    main()
