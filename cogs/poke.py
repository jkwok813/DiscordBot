from nextcord.ext import commands
from bot import bot, intents
import nextcord
import config
import requests
import aiohttp

GUILDID = config.GUILDID
pokehelp = config.pokehelp

#print(f"{pokehelp}")

#helper function to simplify pokemon to their default forms
def pokeCheck(pokemon):
        print(f"Helper method called on {pokemon}")
        if pokemon in pokehelp:
            pokemon = pokehelp[pokemon]
            print(f"Changed to {pokemon}")
        return pokemon

class poke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f"poke initialized")

    #Returns a Pokemon's BST
    @nextcord.slash_command(description="Returns a Pokemon's total bst", guild_ids=[GUILDID])
    async def bst(self, interaction: nextcord.Interaction, pokemon = str):
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # Write the request into 
                if response.status == 200:
                    data = await response.json()
                    stats = data['stats']
                    # Prepare the stat information to send
                    stat_details = [f"{stat['stat']['name'].upper()}: {stat['base_stat']}" for stat in stats]
                    stat_message = "\n".join(stat_details)
                    bst = sum(stat['base_stat'] for stat in stats)
                    await interaction.response.send_message(f"The BST of {pokemon} is **{bst}**. Here are the stats: \n{stat_message}")
                else:
                    await interaction.response.send_message(f"Error")

    #Returns a Pokemon's Shiny Sprite (Gen 9)
    @nextcord.slash_command(description="Returns a Pokemon's total shiny sprite", guild_ids=[GUILDID])
    async def shiny(self, interaction: nextcord.Interaction, pokemon = str):
        pokemon = pokeCheck(pokemon)
        print(f"Searching for {pokemon}'s shiny sprite")
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # Write the request into 
                if response.status == 200:
                    data = await response.json()
                    shiny_sprites = data['sprites']['versions']['generation-v']['black-white']['animated']['front_shiny']
                    dexno = data['id']
                    print(f"Searching for: {pokemon}")
                    if data is None:
                        await interaction.response.send_message(f"Could not find specified Pokemon")
                        return
                    if shiny_sprites:
                        # Prepare the stat information to send
                        await interaction.response.send_message(f"Displaying sprite for: {pokemon} \n {shiny_sprites}")
                    elif id:
                        shiny_sprites = data['sprites']['front_shiny']
                        await interaction.response.send_message(f"Displaying sprite for: {pokemon} \n {shiny_sprites}")
                    else:
                        await interaction.response.send_message("Could not find sprite")
                else:
                    await interaction.response.send_message(f"Error")

    #Checks if a Pokemon learns a specified move
    @nextcord.slash_command(description="Checks if a Pokemon can learn the specified move", guild_ids=[GUILDID])
    async def learncheck(self, interaction: nextcord.Interaction, pokemon = str, movesearch = str):
        pokemon = pokeCheck(pokemon)
        movesearch = movesearch.lower()
        print(f"Checking if {pokemon} can learn {movesearch}")
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    for move in data['moves']:
                        print(f"{move}")
                        if move['move']['name'] == movesearch:
                            method = move['version_group_details']['0']['move_learn_method']['name']
                            message = f"**{pokemon}** can learn **{movesearch}** via {method}"
                            if method == ['level_up']:
                                message = message + f" at level {move['version_group_details']['0']['level_learned_at:']}"
                            await interaction.response.send_message(message)
                            return
                    await interaction.response.send_message(f"**{pokemon} ** cannot learn **{movesearch}**")
                    
def setup(bot):
    bot.add_cog(poke(bot))