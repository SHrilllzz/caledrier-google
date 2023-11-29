"# caledrier-google" 
Project Title: Time Manager with Google Calendar Integration

Overview
This Python script serves as a Time Manager that integrates with Google Calendar API to track and analyze coding hours. The script interacts with the Google Calendar API to fetch coding events, calculates the total coding time for the day, and adds the data to an SQLite database. Additionally, it provides functionality to add custom coding events to the calendar.

Features
Google Calendar Integration:

Fetches coding events from the user's Google Calendar for the current day.
Calculates the total coding time and displays individual event durations.
SQLite Database Storage:

Stores coding hours data in an SQLite database (hours.db).
The database includes columns for the date, coding category, and hours.
Add Custom Coding Events:

Allows users to add custom coding events with specified durations to the Google Calendar.
Statistics and Analytics:

Provides a function to retrieve coding statistics from the SQLite database.
Displays the total number of coding hours and the average coding time.
Getting Started
Prerequisites:

Ensure Python is installed.
Set up Google API credentials by running the script and generating the token.json file.
Installation:

Clone the repository and install dependencies using pip install -r requirements.txt.
Usage:

Run the script (timeManager.py) to fetch Google Calendar events and store coding hours data.
Use the AddEvent function to manually add custom coding events.
Check coding statistics with the get_coding_stats function.
Dependencies
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
dateutil
sqlite3
Notes
Make sure to secure and keep your API credentials (credentials.json) and the token.json file confidential.
