import datetime
import os.path
import sqlite3

from dateutil import parser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        print("Token file 'token.json' not found. Please run the script to generate it.")
        return

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())

    commit_hours(creds)
    AddEvent(creds, 3, 'HI MAHA',)


def commit_hours(creds):
    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        today = datetime.date.today()
        time_start = str(today) + "T10:00:00Z"
        time_end = str(today) + "T23:59:59Z"  # Z indicates UTC time
        print("Getting today's coding hours")
        events_result = (
            service.events()
            .list(
                calendarId="maha.riad@e-polytechnique.ma",
                timeMin=time_start,
                timeMax=time_end,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return
        # adding up the duration of all the hours that we find based on our API call
        total_duration = datetime.timedelta(
            seconds=0,
            minutes=0,
            hours=0,
        )
        print('MY CODING HOURS :')

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))

            start_formatted = parser.isoparse(start)  # changing the start time to datetime format
            end_formatted = parser.isoparse(end)  # changing the end time to datetime format
            duration = end_formatted - start_formatted
            total_duration += duration
            print(f"{event.get('summary')}, duration: {duration}")
        print(f'Total coding time: {total_duration}')

        # here I want to save time data to SQL database sqlite3
        conn = sqlite3.connect('hours.db')
        cur = conn.cursor()
        print("Opened database successfully")
        date = datetime.date.today()

        formatted_total_duration = total_duration.seconds / 60 / 60
        coding_hours = (date, 'CODING', formatted_total_duration)
        cur.execute("INSERT INTO hours VALUES(?,?,?);", coding_hours)
        conn.commit()
        print("Coding hours added successfully! Yay ")

    except HttpError as error:
        print(f"An error occurred: {error}")


def AddEvent(creds, duration, description):
    start = datetime.datetime.utcnow()

    # Correct end time calculation
    end = start + datetime.timedelta(hours=duration)

    start_formatted = start.isoformat() + 'Z'
    end_formatted = end.isoformat() + 'Z'

    event = {
        'summary': description,
        'start': {
            'dateTime': start_formatted,
            'timeZone': 'UTC',  # Specify the timezone as UTC
        },
        'end': {
            'dateTime': end_formatted,
            'timeZone': 'UTC',
        },
    }

    try:
        service = build("calendar", "v3", credentials=creds)
        created_event = service.events().insert(calendarId='maha.riad@e-polytechnique.ma', body=event).execute()
        print("Event created successfully! Link:", created_event.get('htmlLink'))

    except HttpError as error:
        print(f"An error occurred: {error}")


def get_coding_stats():
    conn = sqlite3.connect('hours.db')
    cur = conn.cursor()

    # Récupérer toutes les lignes de la table 'hours'
    cur.execute("SELECT * FROM hours")
    rows = cur.fetchall()

    total_hours = 0
    for row in rows:
        total_hours += row[2]  # La colonne 2 contient les heures codées

    average_hours = total_hours / len(rows) if len(rows) > 0 else 0

    conn.close()

    return total_hours, average_hours

# Exemple d'utilisation
total, average = get_coding_stats()
print(f"Nombre total d'heures codées : {total} heures")
print(f"Moyenne d'heures codées : {average} heures")
if __name__ == "__main__":
    main()
