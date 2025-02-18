import nextcord
import os
from nextcord.ext import commands 
from config import *
from dotenv import load_dotenv

#Intents - all set to true for now via .all()
#intents = nextcord.Intents.all()

#Intents - set to default
intents = nextcord.Intents.all()
#intents.members = True 

# A bot instance is the connection to discord. 
bot = commands.Bot(intents=intents)

#Setting the discord key from the .env file
load_dotenv()
discordkey = os.getenv("dcode")
#print(discordkey)

COG_FOLDER = "cogs"

def load_cogs():
    for filename in os.listdir(COG_FOLDER):
        if filename.endswith(".py") and filename != "__init__.py":
            cog_name = f"{COG_FOLDER}.{filename[:-3]}"
            try:
                bot.load_extension(cog_name)
                print(f"Loaded cog: {cog_name}")
            except Exception as e:
                print(f"Failed to load cog {cog_name}: {e}")

#Async function - Is specifically called when the bot is finished logging in and setting up
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
load_cogs()
bot.run(discordkey)
                