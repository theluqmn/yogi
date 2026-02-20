# account= discord ID
# currency= currency ticker/symbol (eg: BTC, USDT, USD, etc.)
# input validation and formatting done at discord handler level, hence no checks or formatting are in the core functions to simplify code and reduce repetition.

import discord
from discord.ext import commands
from services import currencies

# discord handlers
class currency_ext(commands.Cog):
    def __init__(self, bot):
        # initialisation
        self.bot= bot
        currency_group= bot.create_group("currency")
        currencies.index_update()
        currencies.initialise()

        # /currency info [currency]
        @currency_group.command(name= "info", description= "Information about a currency")
        async def command_info(ctx: discord.ApplicationContext, currency_id: str):
            currency_id= currency_id.upper()
            if (currency_id):
                data= currencies.index_get(currency_id)

                embed= discord.Embed(
                    title= "Currency info",
                    color= discord.Color.yellow()
                )
                embed.set_author(name= f"/currency info {currency_id}")
                embed.add_field(name= "ID", value=f"`{currency_id}`", inline= True)
                embed.add_field(name= "Name", value=f"`{data['name']}`", inline= True)
                if data['type'] == "fiat":
                    embed.add_field(name= "Currency min. size", value=f"`{data['min_size']}`", inline= False)
                else:
                    embed.add_field(name= "Crypto asset ID:", value= f"f`{data['asset_id']}`", inline= False)
                embed.set_footer(text= "Data provided by the Coinbase API.")

                await ctx.respond(embed= embed)
            else: # invalid currency
                embed= discord.Embed(
                    title= "Currency info",
                    description= "**Error**: Invalid currency/token ID provided.\nPlease refer to `/currency list [fiat/crypto]` for the list of supported currencies.\n\nCommon currencies include `USD`, `USDT`, `BTC`, `ETH`.",
                    color= discord.Color.brand_red()
                )
                embed.set_author(name= f"/currency info {currency_id}")
                embed.set_image(url="https://http.cat/400.jpg")
                embed.set_footer(text= "Looks like you need '/yogi help'...")

                await ctx.respond(embed= embed)

        # /currency list [type]

        # /currency balance [currency]
        @currency_group.command(name= "balance", description= "Your balance for a particular currency (defaults to your base)")
        async def command_balance(ctx: discord.ApplicationContext, currency_id: str = "USD"):
            currency_id= currency_id.upper()
            if (currency_id):
                if currencies.wallet_exists(ctx.author.id, currency_id) == False: currencies.wallet_init(ctx.author.id, currency_id)
                balance= currencies.wallet_balance(ctx.author.id, currency_id)
                currency_data = currencies.index_get(currency_id)

                embed= discord.Embed(
                    title= f"{ctx.author.name}'s balance",
                    color= discord.Color.brand_green()
                )
                embed.set_author(name= f"/currency balance {currency_id}")
                embed.add_field(name= "Currency", value= f"{currency_id} ({currency_data['name']})")
                embed.add_field(name= "Balance", value= f"{balance}", inline= True)
                embed.set_footer(text= "Need more money? Work harder lol")

                await ctx.respond(embed= embed)
            else: # invalid currency
                embed= discord.Embed(
                    title= f"{ctx.author.name}'s {currency_id} balance",
                    description= "**Error**: Invalid currency/token ID provided.\nPlease refer to `/currency list [fiat/crypto]` for the list of supported currencies.\n\nCommon currencies include `USD`, `USDT`, `BTC`, `ETH`.",
                    color= discord.Color.brand_red()
                )
                embed.set_author(name= f"/currency balance {currency_id}")
                embed.set_image(url="https://http.cat/400.jpg")
                embed.set_footer(text= "Looks like you need '/yogi help'...")

                await ctx.respond(embed= embed)

        # /currency buy [currency] [amount]

        # /currency sell [currency] [amount]

        # /currency swap [currency]
        @currency_group.command(name= "swap", description= "Swap between fiat and crypto pairs")
        async def command_swap(ctx: discord.ApplicationContext, pair: discord.Option(name= "pair", description= "Currency pair", choices= [
            discord.OptionChoice(name="USD->USDT", value="USD-USDT"),
            discord.OptionChoice(name="USDT->USD", value="USDT-USD")
        ]), amount: float): # type: ignore
            if (pair == "USD-USDT"):
                if currencies.wallet_exists(ctx.author.id, "USDT") == False: currencies.wallet_init(ctx.author.id, "USDT")
                usd_balance= currencies.wallet_balance(ctx.author.id, "USD")

                if currencies.transfer_out(ctx.author.id, "USD", amount):
                    currencies.transfer_in(ctx.author.id, "USDT", amount)
                    embed= discord.Embed(
                        title= f"Currency Swap Successful",
                        description= f"Successfully swapped `USD {amount}` to `USDT {amount}.`",
                        color= discord.Color.brand_green()
                    )
                    embed.set_author(name= f"/currency swap USD-USDT {amount}")

                    await ctx.respond(embed= embed)
                else: # insufficient balance
                    embed= discord.Embed(
                        title= f"Currency Swap Failed",
                        description= f"**Error**: Insufficient `USD` balance to perform `USD-USDT` swap with the specified amount ({amount}).\n\nYour balance is only `USD {usd_balance}.`",
                        color= discord.Color.brand_red()
                    )
                    embed.set_author(name= f"/currency swap USD-USDT {amount}")
                    embed.set_footer(text= "You need more money bro.")

                    await ctx.respond(embed= embed)
        # swap logic will reference config.json to allow for dynamic addition/subtraction of pairs

        # /currency base [currency]

        # /currency portfolio [type]

        # /currency transfer [account] [amount] [note] (currency)

def setup(bot):
    bot.add_cog(currency_ext(bot))