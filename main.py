import discord
from discord.ext import commands

from youtube_cog import youtube_cog


Bot = commands.Bot(command_prefix = "!")

Bot.add_cog(youtube_cog(Bot))


# Debug
@commands.command()
async def test(ctx):
    print("Test command!")
    print(ctx.author)
    print(ctx.channel)
    print(ctx.command)
    print(ctx.guild)
    print(ctx.me)
    print(ctx.prefix)
    channel = ctx.message.author.voice.channel 
    print(channel)


f = open("chiavi/discord.txt",mode="r",encoding="utf-8")
key = f.read().strip()
f.close()
Bot.run(key)