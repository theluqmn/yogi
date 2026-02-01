import requests, json, discord
from discord.ext import commands

fiat_currencies = {}
crypto_currencies = {}

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
        crypto_currencies[i["code"]] = {"name": i["name"]}

index_update()