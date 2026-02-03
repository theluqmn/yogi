# timestamp format = yyyy-mm-dd HH:MM:SS

import sqlite3, datetime

def log_command(command, account, channel, guild):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M%S")

    with sqlite3.connect("./src/databases/statistics.db") as conn:
        with conn:
            conn.execute("")
