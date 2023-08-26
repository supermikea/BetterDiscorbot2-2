import asyncio

import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, tasks

import yt_dlp

test_servers = [1030579093659471913]

yt_dlp.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": False,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": True,
    "quiet": True,
    "no_warnings": False,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}
# ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10'}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=1):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")

    @classmethod
    async def play(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        # if "entries" in data:
        #    # take the entry given from the user TODO: BROKEN
        #    data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(nextcord.FFmpegPCMAudio(filename), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.queue: list = []

    # noinspection PyUnboundLocalVariable
    @nextcord.slash_command(description="play something", guild_ids=test_servers)
    async def play(self, interaction: nextcord.Interaction, url: str = SlashOption):
        voice_state = interaction.user.voice
        print("in play function")
        if not voice_state:
            await interaction.response.send_message("You are not connected to a voice channel!")
            return

        # handle (potential) exceptions when connecting to voice channel
        try:
            voice_client: nextcord.VoiceClient = await voice_state.channel.connect()
        except nextcord.ClientException:  # already in voice channel so it isn't a problem
            in_voice = True
        except asyncio.TimeoutError as e:
            await interaction.response.send_message(f"couldn't connect to the voice channel with exception: {e}")
            return
        finally:
            if not 'voice_client' in locals():  # check if voice_client is actually created
                voice_client: nextcord.VoiceClient = self.bot.voice_clients[0]

        if voice_client.is_playing():
            player = await YTDLSource.play(url, loop=self.bot.loop, stream=True)
            self.queue.append(player)
            # print(player.data["url"])
            if not self.queue_method.is_running():
                self.queue_method.start(channel=interaction.channel)
            await interaction.response.send_message(f"Added \"{player.data['title']}\" to the queue!")
            return

        player = await YTDLSource.play(url, loop=self.bot.loop, stream=True)
        voice_client.play(source=player, after=lambda e: print(f"Player error: {e}") if e else None)
        await interaction.response.send_message(f"Now Playing: {player.data['title']}")

    @nextcord.slash_command(description="display the queue", guild_ids=test_servers)
    async def queue(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(f"The Queue is:\n{[obj['title'] for obj in self.queue]}")

    @tasks.loop(seconds=1)
    async def queue_method(self, channel: nextcord.TextChannel):
        voice_client: nextcord.VoiceClient = self.bot.voice_clients[0]
        if not voice_client.is_playing() and self.queue != []:
            # print("not playing and queue not empty")
            player_data = self.queue.pop()
            voice_client.play(source=player_data['url'], after=lambda e: print(f"Player error: {e}") if e else None)
            await channel.send(f"Now playing: {player_data['title']}")
        if not voice_client.is_playing() and self.queue == []:
            self.queue_method.stop()
