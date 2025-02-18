from nextcord.ext import commands
from bot import bot, intents
from dotenv import load_dotenv
import os
import nextcord
import config
import aiohttp

GUILDID = config.GUILDID
load_dotenv()
riottoken = os.getenv("riottoken")
headers = {
    'X-Riot-Token': riottoken
}

async def get_latest_version():
    url = 'https://ddragon.leagueoflegends.com/api/versions.json'
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                versions = await response.json()
                print(f"Version {version} received")
                return versions[0]  # The latest version is the first one in the list
            else:
                print(f"Error fetching latest version: {response.status}")
                return None

async def champSearch(champId, champions):
    for champion_key, champion_info in champions.items():
        if champion_info['key'] == str(champId):
            return champion_info['id']
    return None

#freechamps is a list of IDs
async def champConv(freechamps):
    version = get_latest_version
    champnames = []
    champions = []
    url = f'https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                champions = data['data']
            else: 
                return f"Error in ddragon API{response.status}"
    if champions:
        for champId in freechamps:
            champname = champSearch(champId, champions)
            if(champname):
                champnames.append(champname)
                print(f"{champname} added")
            else:
                return("Champ not found")
        

class league(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Checks the free champion rotation", guild_ids=[GUILDID])
    async def freechamps(self, interaction: nextcord.Interaction):
        url = "https://na1.api.riotgames.com/lol/platform/v3/champion-rotations"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                # Write the request into 
                if response.status == 200:
                    data = await response.json()
                    freechamps = data['freeChampionIds']
                    # Prepare the stat information to send
                    champnames = await champConv(freechamps)
                    await interaction.response.send_message(f"Free Champs are {champnames}")
                else:
                    await interaction.response.send_message(f"Error {response.status}")

def setup(bot):
    bot.add_cog(league(bot))
        
    @nextcord.slash_command(description="Checks a current player's rank: i.e. Test#1234", guild_ids=[GUILDID])
    async def rank(self, interaction: nextcord.Interaction, username = str):
        
        #Split the username to get the PUUID
        split_string = username.split("#")
        if len(split_string)< 0:
            await interaction.response.send_message(f"User not found")
            return
        print(split_string)

        #Extract PUUID from name and tag
        gameName = split_string[0]
        tagLine = split_string[1]
        url = f"https://na1.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # Write the request into 
                if response.status == 200:
                    data = await response.json()
                    print(f"data is {data}")
                    puuid = data['puuid']
                    # Prepare the stat information to send
                    await interaction.response.send_message(f"PUUID is {puuid}")
                else:
                    await interaction.response.send_message(f"Error {response.status}")
def setup(bot):
    bot.add_cog(league(bot))
