import asyncio
import time
import threading

import nextcord
import yt_dlp as youtube_dl
from nextcord.ext import commands, tasks

# global variables
playing = False
index = 0
context1 = None
queue = []
player = None
arg = None

# threads
t_counter = 0
b1 = None

# Suppress noise about console usage from errors
# youtube_dl.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": False,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.75):
        super().__init__(source, volume)

        self.data = data
        # print(f"[DEBUG] {data}")
        self.title = data.get("title")
        self.url = data.get("url")
        self.duration = data.get("duration_string")
        self.play_list_index = data.get("playlist_index")
        if "entries" in data:
            print("[DEBUG] Detected Playlist")
            self.play_list = True
            self.entries = data["entries"]

    @classmethod
    async def play(cls, url, *, loop=None, stream=True):
        global index
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        # print(data)

        if "entries" in data:
            # take first item from playlist
            data = data["entries"][index]

        else:
            index = 0

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(nextcord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: nextcord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, url):
        global player, queue
        """Streams from a URL (same as yt, but doesn't predownload)"""

        if ctx.voice_client.is_playing():
            queue.append(url)
            await ctx.send(f"added {url} to the queue")
            return

        async with ctx.typing():
            player = await YTDLSource.play(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(
                player, after=lambda e: print(f"Player error: {e}") if e else None
            )

        await ctx.send(f"Now playing: {player.title}\nDuration: {player.duration} seconds")

    @commands.command()
    async def queue(self, ctx):
        global queue
        await ctx.send(f"the queue is: {queue}")

    @commands.command()
    async def skip(self, ctx):
        ctx.voice_client.stop()
        await ctx.send("Skipped the song!")

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")

    @play.after_invoke
    async def after_voice(self, ctx):
        if not self.queue_method.is_running():
            self.queue_method.start(ctx)

    @tasks.loop(seconds=1)
    async def queue_method(self, ctx):
        if not ctx.voice_client.is_playing():
            try:
                await self.play(context=ctx, url=queue.pop(0))
            except IndexError:
                pass
