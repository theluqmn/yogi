# account = id of the discord account
# access_code = hashed and salted access code for the account, used for large transactions or account locks
# tier = account tier; 1 = member, 2 = novice, 3 = executive, 4 = icon, 5 = elite. refer documentation for privileges.

import sqlite3

# create an account in the database
def account_create(account):
    with sqlite3.connect("../database/accounts.db") as conn:
        with conn:
            conn.execute("CREATE TABLE IF NOT EXISTS user (account INTEGER PRIMARY KEY, tier INTEGER, access_code TEXT, locked INTEGER)")

# check if the account is in the database
def account_exists(account):
    with sqlite3.connect("../database/accounts.db") as conn:
        with conn:
            cursor = conn.execute("SELECT * FROM user WHERE account = ?", (account,))
            if cursor.fetchone() is None:
                return False
            else:
                return True

# verify access code
def access_code_verify(account, access_code):
    with sqlite3.connect("../database/accounts.db") as conn:
        with conn:
            cursor = conn.execute("SELECT access_code FROM user WHERE account = ?", (account,))
            check = cursor.fetchone()[0]

            if (check == access_code):
                return True
            else:
                return False
            
# set access code
def access_code_set(account, access_code, new_access_code):
    with sqlite3.connect("../database/accounts.db") as conn:
        with conn:
            if access_code_verify(account, access_code) == True:
                conn.execute("UPDATE user SET access_code = ? WHERE account = ?", (new_access_code, account))
                return True
            else:
                return False
