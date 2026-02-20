# timestamp format = yyyy-mm-dd HH:MM:SS
# statistics flags = 0 - info, 1 - warning, 2 - error

import sqlite3, datetime
db = './src/databases/logs.db'

def timestamp_get(): return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def log_initialise():
    with sqlite3.connect(db) as conn:
        with conn:
            conn.execute("CREATE TABLE IF NOT EXISTS events (flag INTEGER, event TEXT, timestamp TEXT)")

def log_event(flag: int, event: str):
    timestamp = timestamp_get()
    with sqlite3.connect(db) as conn:
        with conn: conn.execute("INSERT INTO events VALUES (?, ?, ?)", (flag, event, timestamp))
        print(f"[{timestamp}] {event}")