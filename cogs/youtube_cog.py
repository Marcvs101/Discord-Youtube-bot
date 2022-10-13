from pydoc import describe
import discord
from discord import app_commands
from discord.ext import commands

from youtube_dl import YoutubeDL

class youtube_cog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

        # Music states
        self.is_playing = False
        self.loop = False
        self.youtube_queue = []
        self.vc = ""

        # Config
        self.YDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True"}
        self.FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}


    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(item,download=False)
            except Exception:
                return False

        return {"source": info["formats"][0]["url"], "title": info["title"]}


    def play_next(self):
        if len(self.youtube_queue) > 0:
            self.is_playing = True

            url = self.youtube_queue[0][0]["source"]
            self.youtube_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
        else:
            self.is_playing = False


    async def play_music(self):
        if len(self.youtube_queue) > 0:
            self.is_playing = True

            # Connect to VC
            if (self.vc == "") or (not self.vc.is_connected()) or (type(self.vc) == type(None)) or (self.vc == None):
                self.vc = await self.youtube_queue[0][1].connect()
            else:
                self.vc = await self.vc.move_to(self.youtube_queue[0][1])

            url = self.youtube_queue[0][0]["source"]
            self.youtube_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
        else:
            self.is_playing = False



    @app_commands.command(name = "play", description = "play url")
    @app_commands.describe(youtube_url = "youtube url to play")
    async def play(self, interaction: discord.Interaction, youtube_url: str):
        print(f"{interaction.user.name} requested {youtube_url}")

        if interaction.user.voice is None:
            await interaction.response.send_message("Connettiti a un canale vocale")
        
        else:
            voice_channel = interaction.user.voice.channel
            song = self.search_yt(youtube_url)
            if type(song) == type(False):
                await interaction.response.send_message("URL non trovato")
            else:
                await interaction.response.send_message("Traccia aggiunta alla lista")
                self.youtube_queue.append([song,voice_channel])

                if self.is_playing == False:
                    await self.play_music()


    @app_commands.command(name = "queue", description = "show queue")
    async def queue(self, interaction: discord.Interaction):
        retval = ""
        for i in range(len(self.youtube_queue)):
            retval += self.youtube_queue[i][0]["title"]+"\n"

        if retval != "":
            await interaction.response.send_message(retval)
        else:
            await interaction.response.send_message("Coda vuota")


    @app_commands.command(name = "skip", description = "skip track")
    async def skip(self, interaction: discord.Interaction):
        if self.vc != "":
            await interaction.response.send_message("Skippando")
            self.vc.stop()
            self.vc == ""
            await self.play_music()
        else:
            await interaction.response.send_message("Qualcosa è andato storto, non sono in un canale vocale")



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(youtube_cog(bot))