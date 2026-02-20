# account = discord_ID
# passcode = hashed and salted text code to toggle account lock, as well as validify major transactions
# tier = 1 (member), 2 (novice), 3 (executive), 4 (icon), 5 (elite)

import sqlite3
from services import currencies
db = './databases/accounts.db'

# initialise
def initialise():
    with sqlite3.connect(db) as conn:
            with conn: conn.execute("CREATE TABLE IF NOT EXISTS user (account_id INTEGER PRIMARY KEY, tier INTEGER, lockdown INTEGER, passcode TEXT, flag INTEGER, settings TEXT, created TEXT)")

# create an account in the database
def create(account_id, timestamp):
    with sqlite3.connect(db) as conn:
        with conn: conn.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?)", (account_id, 1, 0, "password", 0, "{}", timestamp))
    currencies.wallet_init(account_id, "USD")
    currencies.transfer_in(account_id, "USD", 2500)

# check if an account exists in the database
def if_exists(account_id: str):
    with sqlite3.connect(db) as conn:
        with conn:
            cursor= conn.cursor()
            cursor.execute("SELECT tier FROM user WHERE account_id=?", (account_id,))
            result= cursor.fetchone()
            if result is None:
                return False
            else:
                return True