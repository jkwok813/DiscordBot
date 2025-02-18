from nextcord.ext import commands
from bot import bot, intents
import nextcord
import config

#print(f"GUILDID from config: {getattr(config, 'GUILDID', None)}")
#print(f"intents.members are: {intents.members}")
GUILDID = config.GUILDID

class playtest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # print(f"playtest initialized")
    #Command to send a message in the welcome channel
    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        print(f"Member joined {member.name}")
        # Access the guild the member joined
        guild = member.guild
        print(f"{member.name} joined {guild.name}")
        
        # Example: Send a welcome message in a specific channel
        welcome_channel = nextcord.utils.get(guild.text_channels, name="welcome")
        if welcome_channel:
            await welcome_channel.send(f"Welcome to the server, {member.mention}!")

    @commands.Cog.listener()
    async def on_member_remove(self, member: nextcord.Member):
        print(f"Member left {member.name}")
        # Access the guild the member joined
        guild = member.guild
        print(f"{member.name} joined {guild.name}")
        
        # Example: Send a goodbye message in a specific channel
        welcome_channel = nextcord.utils.get(guild.text_channels, name="welcome")
        if welcome_channel:
            await welcome_channel.send(f"See you later, {member.mention}!")

    #Detects when a member is banned from the server
    @commands.Cog.listener()
    async def on_member_ban(self, guild: nextcord.Guild, user: nextcord.User):
        print(f"{user.name} was banned from the server.")
        # Example: Send a banned message in a server
        welcome_channel = nextcord.utils.get(guild.text.channels, name="welcome")
        if welcome_channel:
            await welcome_channel.send(f"Bozo banned: {user.name}")


    @commands.Cog.listener()
    async def on_member_unban(self, guild: nextcord.Guild, user: nextcord.User):
        print(f"{user.name} was unbanned from the server.")
        # Example: Send an unbanned message in a server
        welcome_channel = nextcord.utils.get(guild.text.channels, name="welcome")
        if welcome_channel:
            await welcome_channel.send(f"Bozo unbanned: {user.name}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:  # Ignore messages sent by the bot itself
            return
        stripped_content = message.content.strip()  # Remove leading/trailing whitespace
        print(f"Raw message: '{message.content}'")
        print(f"Stripped message: '{stripped_content}'")
        if not stripped_content:
            print("Received an empty or whitespace-only message.")
            return
        print(f"Received message: {message.content}")
        if message.content.startswith("!hello"):
            await message.channel.send(f"Hello, {message.author.name}!")

    @commands.Cog.listener()
    async def on_member_update(before, after):
        if before.nick != after.nick:
            print(f"{after.name} changed their nickname from {before.nick} to {after.nick}")

    # print(f"Listeners loaded")

    #Register a slash command - Takes in an Interaction object and uses interaction.send to send back "Hello!"
    @nextcord.slash_command(description="My first slash command", guild_ids=[GUILDID])
    async def hello(self, interaction: nextcord.Interaction):
        print(f'/hello command sent')
        await interaction.send("Hello! ttt4fefef")

    #Display Bot Permissions
    @nextcord.slash_command(name="permissions", description="Show the bot's permissions in this channel.", guild_ids=[GUILDID])
    async def permissions(self, interaction: nextcord.Interaction):
        # Get the bot's permissions in the channel where the command was invoked
        bot_permissions = interaction.channel.permissions_for(interaction.guild.me)
        
        # Format permissions into a human-readable list
        permissions_list = []
        for perm, has_perm in bot_permissions:
            permissions_list.append(f"{perm.replace('_', ' ').title()}: {'Yes' if has_perm else 'No'}")
        
        # Join all the permissions into a string
        permissions_str = "\n".join(permissions_list)
        
        # Send the permissions in a message
        await interaction.response.send_message(f"**Bot Permissions in this channel:**\n{permissions_str}")

    #Kick User
    @nextcord.slash_command(description="Kicks user", guild_ids=[GUILDID])
    async def kick(self, interaction:nextcord.Interaction, member: nextcord.Member, reason=None):
        bot_top_role = interaction.guild.me.top_role
        target_top_role = member.top_role
        if target_top_role >= bot_top_role:
            print(f"not kickable")
            await interaction.response.send_message("I cannot kick someone with a higher or equal role than my highest role.", ephemeral=True)
            return
        else:
            print(f"This user is very kickable")
        print(f"{interaction.user} is attempting to kick {member}")
        if interaction.user.guild_permissions.kick_members:
            await member.kick(reason=reason)
            await interaction.response.send_message("kicked")
        else:
            await interaction.response.send_message("No perms")

    #Ban User
    @nextcord.slash_command(description="Bans user", guild_ids=[GUILDID])
    async def ban(self, interaction:nextcord.Interaction, member: nextcord.Member, reason=None):
        bot_top_role = interaction.guild.me.top_role
        target_top_role = member.top_role
        if target_top_role >= bot_top_role:
            print(f"not kickable")
            await interaction.response.send_message("I cannot kick someone with a higher or equal role than my highest role.", ephemeral=True)
            return
        print(f"{interaction.user} is attempting to ban {member}")
        if interaction.user.guild_permissions.ban_members:
            await member.ban(reason=reason)
            await interaction.response.send_message("banned")
        else:
            await interaction.response.send_message("No perms")

def setup(bot):
    bot.add_cog(playtest(bot))