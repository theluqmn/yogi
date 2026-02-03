import os, json, discord
from dotenv import load_dotenv
os.system('cls' if os.name == 'nt' else 'clear')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
with open("./src/config.json", "r") as f: config = json.load(f)

if __name__ == "__main__":
    print(f"pwd: {os.getcwd()}")
    print("Starting up Yogi...")
    bot = discord.Bot(intents=discord.Intents.all())

    for extension in config["extensions"]: bot.load_extension(f"extensions.{extension}")

    @bot.event
    async def on_ready():
        await bot.change_presence(status= discord.Status.do_not_disturb, activity= discord.Activity(name="cold cod"))
        print("Yogi is online.")
    
    bot.run(TOKEN)