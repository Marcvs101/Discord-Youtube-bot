from code import interact
import discord
from discord import app_commands
from discord.ext import commands

from cogs.youtube_cog import youtube_cog



class IlMale(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.members = True

        super().__init__(command_prefix = "!", intents = intents, help_command = None)

    async def setup_hook(self):
        await self.load_extension("cogs.youtube_cog")
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")

    async def on_ready(self):
        print("Bot is online")



bot = IlMale()


# Debug
@bot.tree.command(name="test")
async def test(interaction: discord.Interaction):
    print("Test command!")
    print(interaction.user)
    print(interaction.channel)
    print(interaction.command)
    print(interaction.guild)
    print(interaction.client)
    if interaction.user.voice is not None:
        channel = interaction.user.voice.channel 
    else:
        channel = "NO_CHANNEL"
    print(channel)
    await interaction.response.send_message(f"{interaction.user.mention}, bot is alive and well", ephemeral = True)


f = open("chiavi/discord.txt",mode="r",encoding="utf-8")
key = f.read().strip()
f.close()
bot.run(key)