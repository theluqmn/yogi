import requests, json, discord
from discord.ext import commands

fiat_currencies = {}
crypto_currencies = {}

# verify if input currency exists in the index
def verify_input(currency):
    if (currency in fiat_currencies or crypto_currencies):
        return True
    else:
        return False

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

# get an item from the indexes
def index_get(type, currency):
    if verify_input(currency) == True:
        if type == "fiat": return fiat_currencies[currency]
        if type == "crypto": return crypto_currencies[currency]

# gets the exchange rate in target currency of a base currency
def exchange_rate_get(base_currency, target_currency):
    global fiat_currencies, crypto_currencies

    if (verify_input(base_currency) and verify_input(target_currency)):
        response = requests.get(f"https://api.coinbase.com/v2/exchange-rates?currency={base_currency}")
        response = json.loads(response.text)
        data = response["data"]["rates"]
        return data[target_currency]

class currency_ext(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        currency_group = bot.create_group("currency", "Currency-related commands.")
        index_update()

        # /currency info {type} {currency}
        @currency_group.command(name="info", description="Get information about a fiat/crypto currency.")
        async def command_info(
        ctx: discord.ApplicationContext,
        type: discord.Option(name= "type", description="Currency type.", choices= [
            discord.OptionChoice(name="crypto", value="crypto"),
            discord.OptionChoice(name="fiat", value="fiat")
        ]), # type: ignore
        currency: str):
            currency = currency.upper()
            data = index_get(type, currency)
            exchange_rate = exchange_rate_get(currency, "USD")

            embed = discord.Embed(
                title= "Currency Info",
                description= f"Here is some information on `{currency}`",
                color= discord.Color.brand_green()
            )
            embed.add_field(name= "ID", value= f"`{currency}`", inline= True)
            embed.add_field(name= "Name", value= f"`{data["name"]}`", inline= True)
            embed.add_field(name= "Exchange rate", value= f"`USD {exchange_rate}`", inline= False)
            embed.set_footer(text= "Powered by the Coinbase API.")
            
            await ctx.respond(embed= embed)

def setup(bot):
    bot.add_cog(currency_ext(bot))