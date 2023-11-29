import sqlite3

conn = sqlite3.connect('hours.db')
cur = conn.cursor()
print("Opened database successfully")

# Drop the existing table if it exists
conn.execute('DROP TABLE IF EXISTS hours')

# Create the new table
conn.execute('''CREATE TABLE IF NOT EXISTS hours
              (DATE       DATE       NOT NULL,
             CATEGORY     TEXT       NOT NULL,
             HOURS        INT        NOT NULL
             );''')
print("Created database successfully")