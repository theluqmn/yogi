import os, json, discord
from dotenv import load_dotenv
from scripts.logging import log_event, log_initialise
os.system('cls' if os.name == 'nt' else 'clear')

load_dotenv()
TOKEN= os.getenv('DISCORD_TOKEN')
with open("./src/config.json", "r") as f: config= json.load(f)

if __name__ == "__main__":
    print(f"cwd: {os.getcwd()}")
    print("starting up Yogi...")
    bot= discord.Bot(intents= discord.Intents.all())
    log_initialise()

    for extension in config["extensions"]:
        try:
            bot.load_extension(f"extensions.{extension}")
            log_event(0, f"extension '{extension}' loaded successfully")
        except:
            log_event(1, f"extension '{extension}' failed to load")

    @bot.event
    async def on_ready():
        await bot.change_presence(status= discord.Status.do_not_disturb, activity= discord.Activity(name="cold cod"))
        log_event(0, "Yogi is now online")
    
    bot.run(TOKEN)