# account = discord_ID
# passcode = hashed and salted text code to toggle account lock, as well as validify major transactions
# tier = 1 (member), 2 (novice), 3 (executive), 4 (icon), 5 (elite)

import sqlite3, discord, datetime
from discord.ext import commands
from extensions import currency

# create an account in the database
def account_create(account, timestamp):
    with sqlite3.connect("./src/databases/accounts.db") as conn:
        with conn: conn.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?)", (account, 1, 0, "password", 0, "{}", timestamp))
    currency.account_currency_init(account, "USD")
    currency.account_currency_add(account, "USD", 2500)

# check if an account exists in the database
def account_exists(account: str):
    with sqlite3.connect("./src/databases/accounts.db") as conn:
        with conn:
            cursor= conn.cursor()
            cursor.execute("SELECT tier FROM user WHERE account=?", (account,))
            result= cursor.fetchone()
            if result is None:
                return False
            else:
                return True

# discord handler
class account_ext(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
        account_group= bot.create_group("account", "Account-related commands.")
        with sqlite3.connect("./src/databases/accounts.db") as conn:
            with conn: conn.execute("CREATE TABLE IF NOT EXISTS user (account INTEGER PRIMARY KEY, tier INTEGER, lockdown INTEGER, passcode TEXT, flag INTEGER, settings TEXT, created TEXT)")

        # /account create
        @account_group.command(name= "create", description= "Create your Yogi account")
        async def command_create(ctx: discord.ApplicationContext):
            if account_exists(ctx.author.id) == False:
                account_create(ctx.author.id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                embed= discord.Embed(
                    title= "Account Creation Successful!",
                    description= f"Hello {ctx.author.mention}, you are now part of the Yogi community!",
                    color= discord.Color.brand_green()
                )
                embed.set_author(name="/account create")
                embed.set_footer(text= "A warm welcome!")

                await ctx.respond(embed= embed)
            else:
                embed= discord.Embed(
                    title= "Account Already Exists!",
                    description= "Your account already exists!",
                    color= discord.Color.brand_red()
                )

                await ctx.respond(embed= embed)
    
def setup(bot):
    bot.add_cog(account_ext(bot))