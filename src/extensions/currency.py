# account= discord ID
# currency= currency ticker/symbol (eg: BTC, USDT, USD, etc.)

import requests, json, sqlite3, discord
from discord.ext import commands

currencies= {}

# verify if input currency exists in the index
def index_verify(currency):
    if (currency in currencies):
        return True
    else:
        return False

# updates the currency index
def index_update():
    global currencies

    res= requests.get("https://api.coinbase.com/v2/currencies")
    res= json.loads(res.text)
    data= res['data']
    for i in data:
        currencies[i['id']] = {'name': i['name'], 'type': 'fiat','min_size': i['min_size']}

    res= requests.get("https://api.coinbase.com/v2/currencies/crypto")
    res= json.loads(res.text)
    data= res['data']
    for i in data:
        currencies[i['code']] = {'name': i['name'], 'type': 'crypto','asset_id': i['asset_id']}

# get an item from the currency index
def index_get(currency):
    if index_verify(currency) == True:
        return currencies[currency]

# verify if account has a certain currency
def account_currency_exists(account: int, currency: str):
    currency= currency.upper()
    with sqlite3.connect("./src/databases/assets.db") as conn:
        with conn:
            cursor= conn.cursor()
            cursor.execute("SELECT amount FROM currencies WHERE account=? AND currency=?", (account, currency))
            result= cursor.fetchone()

            if result == None:
                return False
            else:
                return True
            
# create a currency for the user
def account_currency_add(account: int, currency: str):
    if account_currency_exists(account, currency) == False:
        currency= currency.upper()
        with sqlite3.connect("./src/databases/assets.db") as conn:
            with conn: conn.execute("INSERT INTO currencies (account, currency, amount) VALUES (?, ?, ?)", (account, currency, 0))
            
# discord handlers
class currency_ext(commands.Cog):
    def __init__(self, bot):
        # initialisation
        self.bot= bot
        currency_group= bot.create_group("currency")
        index_update()

        with sqlite3.connect("./src/databases/assets.db") as conn:
            with conn:
                conn.execute("CREATE TABLE IF NOT EXISTS currencies (account INTEGER, currency TEXT, amount FLOAT)")

        # /currency info [currency]
        @currency_group.command(name= "info", description= "Information about a currency")
        async def command_info(ctx: discord.ApplicationContext, currency: str):
            currency= currency.upper()
            if index_verify(currency):
                data= index_get(currency)

                embed= discord.Embed(
                    title= "🪙 Currency Info",
                    color= discord.Color.yellow()
                )
                embed.add_field(name= "ID", value=f"`{currency}`", inline= True)
                embed.add_field(name= "Name", value=f"`{data['name']}`", inline= True)
                if data['type'] == "fiat":
                    embed.add_field(name= "Currency min. size", value=f"`{data['min_size']}`", inline= False)
                else:
                    embed.add_field(name= "Crypto asset ID:", value= f"f`{data['asset_id']}`", inline= False)
                embed.set_author(name= f"/currency info {currency}")
                embed.set_footer(text= "Powered by the Coinbase API.")

                await ctx.respond(embed= embed)

        # /currency list [type]

        # /currency balance [currency]

        # /currency buy [currency] [amount]

        # /currency sell [currency] [amount]

        # /currency swap [currency]

        # /currency base [currency]

        # /currency portfolio [type]

        # /currency transfer [account] [amount] [note] (currency)

def setup(bot):
    bot.add_cog(currency_ext(bot))