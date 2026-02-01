import requests, json, discord
from discord.ext import commands

fiat_currencies = {}
crypto_currencies = {}

# updates the local index
def index_update():
    global fiat_currencies, crypto_currencies

    response = requests.get("https://api.coinbase.com/v2/currencies")
    response = json.loads(response.text)
    data = response["data"]
    for i in data:
        fiat_currencies[i["id"]] = {"name": i["name"], "min_size": i["min_size"]}

    response = requests.get("https://api.coinbase.com/v2/currencies/crypto")
    response = json.loads(response.text)
    data = response["data"]
    for i in data:
        crypto_currencies[i["code"]] = {"name": i["name"], "asset_id": i["asset_id"]}

# verify if input currency exists in the index
def verify_input(currency):
    if (currency in fiat_currencies or crypto_currencies):
        return True
    else:
        return False

# gets the exchange rate in target currency of a base currency
def exchange_rate(base_currency, target_currency):
    global fiat_currencies, crypto_currencies

    if (base_currency in fiat_currencies or crypto_currencies):
        response = requests.get(f"https://api.coinbase.com/v2/exchange-rates?currency={base_currency}")
        response = json.loads(response.text)
        data = response["data"]["rates"]
        return data[target_currency]

index_update()
exchange_rate("BTC", "USD")