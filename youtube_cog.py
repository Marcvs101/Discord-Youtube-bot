import discord
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


    @commands.command()
    async def play(self, ctx, url):
        voice_channel = ctx.author.voice.channel

        if voice_channel is None:
            await ctx.send("Connettiti a un canale vocale")
        else:
            song = self.search_yt(url)
            if type(song) == type(False):
                await ctx.send("URL non trovato")
            else:
                print(ctx.author.name)
                await ctx.send("Traccia aggiunta alla lista")
                self.youtube_queue.append([song,voice_channel])

                if self.is_playing == False:
                    await self.play_music()


    @commands.command()
    async def queue(self, ctx):
        retval = ""
        for i in range(len(self.youtube_queue)):
            retval += self.youtube_queue[i][0]["title"]+"\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("Coda vuota")


    @commands.command()
    async def skip(self, ctx):
        if self.vc != "":
            await ctx.send("Skippando")
            self.vc.stop()
            self.vc == ""
            await self.play_music()
