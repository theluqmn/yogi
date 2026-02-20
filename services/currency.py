import requests, json, sqlite3
from services import accounts

# verify if input currency is supported
def index_verify(currency):
    if (currency in currencies):
        return True
    else:
        return False

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

# get currency data from the index
def index_get(currency):
    if index_verify(currency) == True:
        return currencies[currency]

# verify if the user has a certain currency
def account_exists(account: int, currency: str):
    with sqlite3.connect('./src/databases/assets.db') as conn:
        with conn:
            cursor= conn.cursor()
            cursor.execute("SELECT amount FROM currencies WHERE account=? AND currency=?", (account, currency))
            result= cursor.fetchone()

            if result == None:
                return False
            else:
                return True

# initialise a currency for the user
def account_init(account: int, currency: str):
    with sqlite3.connect('./src/databases/assets.db') as conn:
        with conn: conn.execute("INSERT OR IGNORE INTO currencies (account, currency, amount) VALUES (?, ?, ?)", (account, currency, 0))

# fetch user balance
def balance(account: int, currency: str):
    currency = currency.upper()
    if account_exists(account, currency) != False: account_currency_init(account, currency)
    with sqlite3.connect('./src/databases/assets.db') as conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT amount FROM currencies WHERE account=? AND currency=?", (account, currency))
            return cursor.fetchone()[0]

# add to balance of a user
def transfer_in(account: int, currency: str, amount: float):
    with sqlite3.connect('./src/databases/assets.db') as conn:
        with conn: conn.execute("UPDATE currencies SET amount = amount + ? WHERE account=? AND currency=?", (amount, account, currency))

# subtract to balance of a user
def transfer_out(account: int, currency: str, amount: float):
    balance= balance(account, currency)
    if balance >= amount:
        with sqlite3.connect('./src/databases/assets.db') as conn:
            with conn: conn.execute("UPDATE currencies SET amount = amount - ? WHERE account=? AND currency=?", (amount, account, currency))
            return True
    else: # insufficient balance
        return False

# get pair buy rate
def pair_buy_rate(base: str, target: str):
    res= requests.get(f'https://api.coinbase.com/v2/prices/{base}-{target}/buy')
    res= json.loads(res.text)
    data= res['data']
    return data['amount']

# get pair sell rate
def pair_buy_rate(base: str, target: str):
    res= requests.get(f'https://api.coinbase.com/v2/prices/{base}-{target}/sell')
    res= json.loads(res.text)
    data= res['data']
    return data['amount']
