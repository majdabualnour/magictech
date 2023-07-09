import datetime
import os
import pickle
from google.auth.transport.requests import Request
# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Set up API credentials file name
CREDENTIALS_FILE = 'credentials.json'

# Set up meeting details
meeting_topic = 'My Meeting'
meeting_start = datetime.datetime(2023, 7, 1, 12, 0, 0)
meeting_end = datetime.datetime(2023, 7, 1, 16, 0, 0)

# Set up scopes for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_google_meet_link(emails):
    # Load or generate credentials
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            pass
            # flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            # creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Create a service object for the Google Calendar API
    service = build('calendar', 'v3', credentials=creds)

    # Create a new event with a Google Meet link
    event = {
        'summary': meeting_topic,
        'start': {
            'dateTime': meeting_start.isoformat(),
            'timeZone': 'Your Time Zone',
        },
        'end': {
            'dateTime': meeting_end.isoformat(),
            'timeZone': 'Your Time Zone',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': 'random-string-123456789',
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet',
                },
                'additionalGuests': emails,
            },
        },
    }

    # Insert the event into the user's primary calendar
    event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()

    # Get the Google Meet link from the created event
    meet_link = event['conferenceData']['entryPoints'][0]['uri']
    return meet_link

# Prompt the user to enter email addresses separated by commas
email_list = input('Enter email addresses separated by commas: ').split(',')

# Remove leading/trailing whitespace from email addresses
email_list = [email.strip() for email in email_list]

# Call the function to create the Google Meet link with the specified email addresses
meeting_link = create_google_meet_link(email_list)
print(f'Meeting Link: {meeting_link}')
