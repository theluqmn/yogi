# account = id of the discord account
# access_code = hashed and salted access code for the account, used for large transactions or account locks
# tier = account tier; 1 = member, 2 = novice, 3 = executive, 4 = icon, 5 = elite. refer documentation for privileges.

import sqlite3, discord
from discord.ext import commands

# create an account in the database
def account_create(account):
    with sqlite3.connect("./src/databases/accounts.db") as conn:
        with conn:
            conn.execute("INSERT INTO user VALUES (?)", (account,))            

# check if the account is in the database
def account_exists(account):
    with sqlite3.connect("./src/databases/accounts.db") as conn:
        with conn:
            cursor = conn.execute("SELECT * FROM user WHERE account = ?", (account,))
            if cursor.fetchone() is None:
                return False
            else:
                return True

# verify access code
def access_code_verify(account, access_code):
    with sqlite3.connect("./src/databases/accounts.db") as conn:
        with conn:
            cursor = conn.execute("SELECT access_code FROM user WHERE account = ?", (account,))
            check = cursor.fetchone()[0]

            if (check == access_code):
                return True
            else:
                return False
            
# set access code
def access_code_set(account, access_code, new_access_code):
    with sqlite3.connect("./src/databases/accounts.db") as conn:
        with conn:
            if access_code_verify(account, access_code):
                conn.execute("UPDATE user SET access_code = ? WHERE account = ?", (new_access_code, account))
                return True
            else:
                return False

class account_ext(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        account_group = bot.create_group("account", "Account-related commands.")
        with sqlite3.connect("./src/databases/accounts.db") as conn:
            with conn:
                conn.execute("CREATE TABLE IF NOT EXISTS user (account INTEGER PRIMARY KEY, tier INTEGER DEFAULT 1, access_code TEXT DEFAULT NULL, locked INTEGER DEFAULT 0, created TEXT)")

        # /account create
        @account_group.command(name="create", description="Create a Yogi account")
        async def command_create(ctx: discord.ApplicationContext):
            if account_exists:
                account_create(ctx.author.id)
                embed = discord.Embed(
                    title= "Account Creation Successful",
                    description= f"{ctx.author.mention}'s has been created successfully!",
                    color= discord.Color.brand_green()
                )

                await ctx.respond(embed= embed)
            else:
                embed = discord.Embed(
                    title= "Account Creation Failed",
                    description= "Your account already exists.",
                    color= discord.Color.brand_green()
                )
                await ctx.respond(embed= embed)

def setup(bot):
    bot.add_cog(account_ext(bot))
