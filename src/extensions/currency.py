import requests, json, sqlite3, discord
from discord.ext import commands

currencies = {}

# verify if input currency exists in the index
def verify_input(currency):
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
    if verify_input(currency) == True:
        return currencies[currency]

# gets the exchange rate in target

# discord handlers
class currency_ext(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
        currency_group= bot.create_group("currency")
        index_update()

        # /currency info [currency]
        @currency_group.command(name= "info", description= "Information about a currency")
        async def command_info(ctx: discord.ApplicationContext, currency: str):
            currency= currency.upper()
            if verify_input(currency):
                data= index_get(currency)

                embed = discord.Embed(
                    title= "Currency Info",
                    color= discord.Color.brand_green()
                )
                embed.add_field(name= "ID", value=f"`{currency}`", inline= True)
                embed.add_field(name= "Name", value=f"`{data['name']}`", inline= True)
                if data['type'] == "fiat": embed.add_field(name= "Min. size", value=f"`{data['min_size']}`", inline= False)
                else: embed.add_field(name= "Asset ID:", value= f"f`{data['asset_id']}`", inline= False)

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