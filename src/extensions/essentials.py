import discord
from discord.ext import commands

class essentials_ext(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        yogi_group = bot.create_group("yogi", "Yogi essential commands")

        # /yogi ping
        @yogi_group.command(name= "ping", description= "Ping the bot.")
        async def ping(ctx: discord.ApplicationContext):
            await ctx.respond(embed= 
                discord.Embed(
                    title= "Pong!",
                    description= f"Latency: {round(self.bot.latency * 1000)}ms",
                    color= discord.Color.brand_green()
                )
            )
        
        # /yogi reload {extension}
        @yogi_group.command(name="reload", description= "Reload an extension.")
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
        
        # /yogi load {extension}
        @yogi_group.command(name="load", description= "Load an extension.")
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

        # /yogi unload {extension}
        @yogi_group.command(name="unload", description= "Unload an extension.")
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
    bot.add_cog(essentials_ext(bot))