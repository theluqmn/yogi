# account= discord ID
# currency= currency ticker/symbol (eg: BTC, USDT, USD, etc.)
# input validation and formatting done at discord handler level, hence no checks or formatting are in the core functions to simplify code and reduce repetition.

import requests, json, sqlite3, discord
from discord.ext import commands

currencies= {}

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
def account_currency_exists(account: int, currency: str):
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
def account_currency_init(account: int, currency: str):
    with sqlite3.connect('./src/databases/assets.db') as conn:
        with conn: conn.execute("INSERT OR IGNORE INTO currencies (account, currency, amount) VALUES (?, ?, ?)", (account, currency, 0))

# fetch user balance
def account_currency_balance(account: int, currency: str):
    currency = currency.upper()
    if account_currency_exists(account, currency) != False: account_currency_init(account, currency)
    with sqlite3.connect('./src/databases/assets.db') as conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT amount FROM currencies WHERE account=? AND currency=?", (account, currency))
            return cursor.fetchone()[0]

# add to balance of a user
def account_currency_add(account: int, currency: str, amount: float):
    with sqlite3.connect('./src/databases/assets.db') as conn:
        with conn: conn.execute("UPDATE currencies SET amount = amount + ? WHERE account=? AND currency=?", (amount, account, currency))

# subtract to balance of a user
def account_currency_sub(account: int, currency: str, amount: float):
    balance= account_currency_balance(account, currency)
    if balance >= amount:
        with sqlite3.connect('./src/databases/assets.db') as conn:
            with conn: conn.execute("UPDATE currencies SET amount = amount - ? WHERE account=? AND currency=?", (amount, account, currency))
            return True
    else: # insufficient balance
        return False

# discord handlers
class currency_ext(commands.Cog):
    def __init__(self, bot):
        # initialisation
        self.bot= bot
        currency_group= bot.create_group("currency")
        index_update()

        with sqlite3.connect("./src/databases/assets.db") as conn:
            with conn:
                conn.execute("CREATE TABLE IF NOT EXISTS currencies (account INTEGER, currency TEXT, amount FLOAT, UNIQUE(account, currency))")

        # /currency info [currency]
        @currency_group.command(name= "info", description= "Information about a currency")
        async def command_info(ctx: discord.ApplicationContext, currency: str):
            currency= currency.upper()
            if index_verify(currency):
                data= index_get(currency)

                embed= discord.Embed(
                    title= "Currency info",
                    color= discord.Color.yellow()
                )
                embed.set_author(name= f"/currency info {currency}")
                embed.add_field(name= "ID", value=f"`{currency}`", inline= True)
                embed.add_field(name= "Name", value=f"`{data['name']}`", inline= True)
                if data['type'] == "fiat":
                    embed.add_field(name= "Currency min. size", value=f"`{data['min_size']}`", inline= False)
                else:
                    embed.add_field(name= "Crypto asset ID:", value= f"f`{data['asset_id']}`", inline= False)
                embed.set_footer(text= "Data provided by the Coinbase API.")

                await ctx.respond(embed= embed)
            else:
                embed= discord.Embed(
                    title= "Currency info",
                    description= "**Error**: Invalid currency/token ID provided.\nPlease refer to `/currency list [fiat/crypto]` for the list of supported currencies.\n\nCommon currencies include `USD`, `USDT`, `BTC`, `ETH`.",
                    color= discord.Color.brand_red()
                )
                embed.set_author(name= f"/currency info {currency}")
                embed.set_image(url="https://http.cat/400.jpg")
                embed.set_footer(text= "Looks like you need '/yogi help'...")

                await ctx.respond(embed= embed)

        # /currency list [type]

        # /currency balance [currency]
        @currency_group.command(name= "balance", description= "Your balance for a particular currency (defaults to your base)")
        async def command_balance(ctx: discord.ApplicationContext, currency: str = "USD"):
            currency= currency.upper()
            if index_verify(currency):
                if account_currency_exists(ctx.author.id, currency) == False: account_currency_init(ctx.author.id, currency)
                balance= account_currency_balance(ctx.author.id, currency)
                currency_data = index_get(currency)

                embed= discord.Embed(
                    title= f"{ctx.author.name}'s balance",
                    color= discord.Color.brand_green()
                )
                embed.set_author(name= f"/currency balance {currency}")
                embed.add_field(name= "Currency", value= f"{currency} ({currency_data['name']})")
                embed.add_field(name= "Balance", value= f"{balance}", inline= True)
                embed.set_footer(text= "Need more money? Work harder lol")

                await ctx.respond(embed= embed)
            else:
                embed= discord.Embed(
                    title= f"{ctx.author.name}'s {currency} balance",
                    description= "**Error**: Invalid currency/token ID provided.\nPlease refer to `/currency list [fiat/crypto]` for the list of supported currencies.\n\nCommon currencies include `USD`, `USDT`, `BTC`, `ETH`.",
                    color= discord.Color.brand_red()
                )
                embed.set_author(name= f"/currency balance {currency}")
                embed.set_image(url="https://http.cat/400.jpg")
                embed.set_footer(text= "Looks like you need '/yogi help'...")

                await ctx.respond(embed= embed)

        # /currency buy [currency] [amount]

        # /currency sell [currency] [amount]

        # /currency swap [currency]

        # /currency base [currency]

        # /currency portfolio [type]

        # /currency transfer [account] [amount] [note] (currency)

def setup(bot):
    bot.add_cog(currency_ext(bot))