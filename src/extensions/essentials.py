import discord
from discord.ext import commands

class essentials(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        yogi_group = bot.create_group("yogi", "Yogi essential commands")

        # /ping
        @yogi_group.command(name= "ping", description= "ping the bot")
        async def ping(ctx: discord.ApplicationContext):
            await ctx.respond(embed= 
                discord.Embed(
                    title= "Pong!",
                    description= f"Latency: {round(self.bot.latency * 1000)}ms",
                    color= discord.Color.brand_green()
                )
            )
        
        # /reload {extension}
        @yogi_group.command(name="reload", description= "reload an extension")
        @commands.is_owner()
        async def reload(ctx: discord.ApplicationContext, extension: str):
            try:
                bot.reload_extension(f"extensions.{extension}")
                await ctx.respond(embed=
                    discord.Embed(
                        title= f"Extension reload successful!",
                        description= f"The extension `{extension}` has been reloaded successfully.",
                        color= discord.Color.brand_green()
                    )
                )
            except Exception as exc:
                await ctx.respond(embed=
                    discord.Embed(
                        title= f"Extension reload failed!",
                        description= f"The extension `{extension}` has failed to reload. Error: `{exc}`",
                        color= discord.Color.brand_red()
                    )
                )
        
        # /load {extension}
        @yogi_group.command(name="load", description= "load an extension")
        @commands.is_owner()
        async def load(ctx: discord.ApplicationContext, extension: str):
            try:
                bot.load_extension(f"extensions.{extension}")
                await ctx.respond(embed=
                    discord.Embed(
                        title= f"Extension loading successful!",
                        description= f"The extension `{extension}` has been loaded successfully.",
                        color= discord.Color.brand_green()
                    )
                )
            except Exception as exc:
                await ctx.respond(embed=
                    discord.Embed(
                        title= f"Extension loading failed!",
                        description= f"The extension `{extension}` has failed to load. Error: `{exc}`",
                        color= discord.Color.brand_red()
                    )
                )

        # /unload {extension}
        @yogi_group.command(name="unload", description= "unload an extension")
        @commands.is_owner()
        async def unload(ctx: discord.ApplicationContext, extension: str):
            try:
                bot.load_extension(f"extensions.{extension}")
                await ctx.respond(embed=
                    discord.Embed(
                        title= f"Extension unloading successful!",
                        description= f"The extension `{extension}` has been unloaded successfully.",
                        color= discord.Color.brand_green()
                    )
                )
            except Exception as exc:
                await ctx.respond(embed=
                    discord.Embed(
                        title= f"Extension unloading failed!",
                        description= f"The extension `{extension}` has failed to unload. Error: `{exc}`",
                        color= discord.Color.brand_red()
                    )
                )

def setup(bot):
    bot.add_cog(essentials(bot))