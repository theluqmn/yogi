import os, json, discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if __name__ == "__main__":
    print("Starting up Yogi...")
    bot = discord.Bot(intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        await bot.change_presence(status= discord.Status.do_not_disturb, activity= discord.Activity(name="cold cod"))
        print("Yogi is online.")
    
    bot.run(TOKEN)