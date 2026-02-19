# account = discord_ID
# passcode = hashed and salted text code to toggle account lock, as well as validify major transactions
# tier = 1 (member), 2 (novice), 3 (executive), 4 (icon), 5 (elite)

import sqlite3, discord, datetime
from discord.ext import commands

# create an account in the database
def account_create(account):
    with sqlite3.connect("./src/databases/accounts.db") as conn:
        with conn: conn.execute("INSERT INTO user VALUES (?)", (account,))

# check if an account exists in the database
def account_exists(account):
    with sqlite3.connect("./src/database/accounts.db") as conn:
        with conn:
            timestamp= datetime.datetime.now().strftime("%Y-%m-%d %H:%M%S")
            cursor= conn.execute("SELECT * FROM user WHERE account = (?, ?, ?, ?, ?, ?, ?)", (account, 1, 0, "password", 0, "", timestamp))
            if cursor.fetchone() is None:
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
            if account_exists:
                account_create(ctx.author.id)
                embed= discord.Embed(
                    title= "Account Creation Successful!",
                    description= f"Hello {ctx.author.mention}, you are now part of the Yogi community!",
                    color= discord.Color.brand_green()
                )
                embed.set_footer(text="/account create")

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