# account = discord_ID
# passcode = hashed and salted text code to toggle account lock, as well as validify major transactions
# tier = 1 (member), 2 (novice), 3 (executive), 4 (icon), 5 (elite)

import discord, datetime
from discord.ext import commands
from services import accounts

class account_ext(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
        account_group= bot.create_group("account", "Account-related commands.")
        accounts.initialise()

        # /account create
        @account_group.command(name= "create", description= "Create your Yogi account")
        async def command_create(ctx: discord.ApplicationContext):
            if accounts.if_exists(ctx.author.id) == False:
                accounts.create(ctx.author.id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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