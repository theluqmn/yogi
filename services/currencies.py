# index = 

import requests, json, sqlite3
db = './databases/assets.db'
currencies = {}

# update the index with coinbase data
def index_update():
    global currencies

    res= requests.get('https://api.coinbase.com/v2/currencies')
    res= json.loads(res.text)
    data= res['data']
    for i in data:
        currencies[i['id']] = {'name': i['name'], 'type': 'fiat','min_size': i['min_size']}

    res= requests.get('https://api.coinbase.com/v2/currencies/crypto')
    res= json.loads(res.text)
    data= res['data']
    for i in data:
        currencies[i['code']] = {'name': i['name'], 'type': 'crypto','asset_id': i['asset_id']}

# initialise
def initialise():
    with sqlite3.connect(db) as conn:
        with conn: conn.execute("CREATE TABLE IF NOT EXISTS currencies (account_id INTEGER, currency_id TEXT, amount FLOAT, UNIQUE(account_id, currency_id))")
    index_update()

# verify if input currency is supported
def index_verify(currency_id):
    if (currency_id in currencies):
        return True
    else:
        return False

# get id data from the index
def index_get(currency_id):
    if index_verify(currency_id) == True:
        return currencies[currency_id]

# verify if the user has a certain currency
def wallet_exists(account: int, currency_id: str):
    with sqlite3.connect(db) as conn:
        with conn:
            cursor= conn.cursor()
            cursor.execute("SELECT amount FROM currencies WHERE account_id=? AND currency_id=?", (account, currency_id))
            result= cursor.fetchone()

            if result == None:
                return False
            else:
                return True

# initialise a currency for the user
def wallet_init(account_id: int, currency_id: str):
    with sqlite3.connect(db) as conn:
        with conn: conn.execute("INSERT OR IGNORE INTO currencies (account_id, currency_id, amount) VALUES (?, ?, ?)", (account_id, currency_id, 0))

# fetch user balance
def wallet_balance(account_id: int, currency_id: str):
    currency_id = currency_id.upper()
    if wallet_exists(account_id, currency_id) != False: wallet_init(account_id, currency_id)
    with sqlite3.connect(db) as conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT amount FROM currencies WHERE account_id=? AND currency_id=?", (account_id, currency_id))
            return cursor.fetchone()[0]

# add to balance of a user
def transfer_in(account_id: int, currency_id: str, amount: float):
    with sqlite3.connect(db) as conn:
        with conn: conn.execute("UPDATE currencies SET amount = amount + ? WHERE account_id=? AND currency_id=?", (amount, account_id, currency_id))

# subtract to balance of a user
def transfer_out(account_id: int, currency_id: str, amount: float):
    balance= wallet_balance(account_id, currency_id)
    if balance >= amount:
        with sqlite3.connect(db) as conn:
            with conn: conn.execute("UPDATE currencies SET amount = amount - ? WHERE account_id=? AND currency_id=?", (amount, account_id, currency_id))
            return True
    else: # insufficient balance
        return False

# get pair buy rate
def pair_buy_rate(base_currency_id: str, target_currency_id: str):
    res= requests.get(f'https://api.coinbase.com/v2/prices/{base_currency_id}-{target_currency_id}/buy')
    res= json.loads(res.text)
    data= res['data']
    return data['amount']

# get pair sell rate
def pair_buy_rate(base_currency_id: str, target_currency_id: str):
    res= requests.get(f'https://api.coinbase.com/v2/prices/{base_currency_id}-{target_currency_id}/sell')
    res= json.loads(res.text)
    data= res['data']
    return data['amount']
