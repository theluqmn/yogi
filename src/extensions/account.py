# account = id of the discord account
# access_code = hashed and salted access code for the account, used for large transactions or account locks
# tier = account tier; 1 = member, 2 = novice, 3 = executive, 4 = icon, 5 = elite

import sqlite3

def account_create(user_id):
    with sqlite3.connect("../database/accounts.db") as conn:
        with conn:
            conn.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, tier INTEGER, access_code TEXT)")