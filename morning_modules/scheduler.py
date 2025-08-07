import datetime
import os.path
from tzlocal import get_localzone

# Got instructions on this file from Google's Python quickstart
# https://developers.google.com/workspace/calendar/api/quickstart/python

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Defines permissions program is requesting
# Allows to read the calendar, but not modify it
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly",
          'https://www.googleapis.com/auth/userinfo.profile',
          'https://www.googleapis.com/auth/userinfo.email',
          'openid']

def start_scheduler():

    creds = get_creds()

    try:
        # Builds the calendar API
        service = build("calendar", "v3", credentials=creds)

        # Calls the calendar API
        # Local timezone
        local_tz = get_localzone() # returns a pytz timezone object

        # Gets todays date
        local_today = datetime.datetime.now(local_tz).date()

        start_of_day_local = datetime.datetime.combine(local_today, datetime.time.min).replace(tzinfo = local_tz)
        start_of_next_day_local = start_of_day_local + datetime.timedelta(days=1)
        
        # Start of today in ISO
        time_min = start_of_day_local.astimezone(datetime.timezone.utc).isoformat()
        
        # Start of tomorrow (midnight) in ISO
        time_max = start_of_next_day_local.astimezone(datetime.timezone.utc).isoformat()

        print("Upcoming events today")
        
        # Today's events in order of start time
        events_result = (
            service.events().list(
                calendarId = "primary",
                timeMin = time_min,
                timeMax = time_max,
                singleEvents = True,
                orderBy = "startTime",
            )
            .execute()
        )

        # event is a list of event dictionaries
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events")
            return []
            
        # Prints start and name of next 10 events
        for event in events:
            start = event['start'].get("dateTime", event['start'].get('date'))
            summary = event['summary']
            print(start)
            print(summary)
        
        return events

    except HttpError as error:
        print(f"An error occurred: {error}")

def get_creds():
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    # If a token was saved previously, load it
    if os.path.exists("token.json"):
        # Creates a Credentials instance from an authorized user json file.
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If no valid credentials available (first time), user logs in
    # Also if invalid or expired
    if not creds or not creds.valid:
        # If credentials are expired but refreshable, refresh
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port = 0)
        # Save credentials
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

if __name__ == "__main__":
    start_scheduler()