# account = discord_ID
# passcode = hashed and salted text code to toggle account lock, as well as validify major transactions
# tier = 1 (member), 2 (novice), 3 (executive), 4 (icon), 5 (elite)

import sqlite3

# create an account in the database
def create(account, timestamp):
    with sqlite3.connect("./src/databases/accounts.db") as conn:
        with conn: conn.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?)", (account, 1, 0, "password", 0, "{}", timestamp))
    # currency.account_currency_init(account, "USD")
    # currency.account_currency_add(account, "USD", 2500)

# check if an account exists in the database
def if_exists(account: str):
    with sqlite3.connect("./src/databases/accounts.db") as conn:
        with conn:
            cursor= conn.cursor()
            cursor.execute("SELECT tier FROM user WHERE account=?", (account,))
            result= cursor.fetchone()
            if result is None:
                return False
            else:
                return True