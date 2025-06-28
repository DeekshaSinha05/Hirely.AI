import datetime
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'  # Download this from Google Cloud Console
TOKEN_FILE = 'token.pickle'


def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service


def create_interview_event(candidate_name, candidate_email, slot, description="Interview with Hirely.AI"):
    service = get_calendar_service()
    start_time = slot["start"]  # slot should be a dict with 'start' and 'end' as RFC3339 strings
    end_time = slot["end"]
    event = {
        'summary': f'Interview: {candidate_name}',
        'location': '',
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC',
        },
        'attendees': [
            {'email': candidate_email},
        ],
        'reminders': {
            'useDefault': True,
        },
    }
    event = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
    return event.get('htmlLink')
