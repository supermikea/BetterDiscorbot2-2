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
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10'}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=1):
        super().__init__(source, volume)

        self.data = data
        self.url = data.get("url")
        self.title = data.get("title")

    @classmethod
    async def play(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        # if "entries" in data:
        #    # take the entry given from the user TODO: BROKEN
        #    data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(nextcord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.queue: list[YTDLSource] = []

    # noinspection PyUnboundLocalVariable
    @nextcord.slash_command(description="play something", guild_ids=test_servers)
    async def play(self, interaction: nextcord.Interaction, url: str = SlashOption,
                   ask_priority: bool = SlashOption(name="priority_queue",
                                                    description="asks for priority from the call participants",
                                                    required=False,
                                                    default=False)):
        voice_state = interaction.user.voice
        # print("in play function")
        if not voice_state:
            await interaction.response.send_message("You are not connected to a voice channel!")
            return

        if ask_priority:
            title = ytdl.extract_info(url, download=False)["title"]
            partial_message: nextcord.PartialInteractionMessage = \
                await interaction.send(f"{interaction.user.display_name} asked to priority queue \"{title}\"")

            inter_message: nextcord.InteractionMessage = await partial_message.fetch()
            await inter_message.add_reaction("✅")
            await inter_message.add_reaction("❎")
            self.priority_method.start(inter_message, url)
            return

        # handle (potential) exceptions when connecting to voice channel
        try:
            voice_client: nextcord.VoiceClient = await voice_state.channel.connect()
            voice_state.self_deaf = True
        except nextcord.ClientException:  # already in voice channel so it isn't a problem
            in_voice = True
        except asyncio.TimeoutError as e:
            await interaction.response.send_message(f"couldn't connect to the voice channel with exception: {e}")
            return
        finally:
            if not 'voice_client' in locals():  # check if voice_client is actually created
                voice_client: nextcord.VoiceClient = self.bot.voice_clients[0]

        await interaction.response.defer()

        if voice_client.is_playing():
            player = await YTDLSource.play(url, loop=self.bot.loop, stream=True)
            self.queue.append(player)
            # print(player.data["url"])
            if not self.queue_method.is_running():
                self.queue_method.start(channel=interaction.channel)
            await interaction.send(f"Added \"{player.data['title']}\" to the queue!")
            return

        try:
            player = await YTDLSource.play(url, loop=self.bot.loop, stream=True)
        except yt_dlp.utils.DownloadError:
            if len(url) > 80:
                await interaction.send("Consider using a shorter link (;")
                return
            await interaction.send("Couldn't find your song! Consider finding a different link.")
            return
        try:
            voice_client.play(source=player, after=lambda e: print(f"Player error: {e}") if e else None)
        except nextcord.ClientException:  # already playing exception
            return
        await interaction.send(f"Now Playing: \"{player.data['title']}\"")

    @tasks.loop(seconds=1)
    async def priority_method(self, message: nextcord.InteractionMessage, url: str):
        await asyncio.sleep(29)
        voice_client: nextcord.VoiceClient = self.bot.voice_clients[0]
        members_connected: list[nextcord.Member] = voice_client.channel.members
        members_useful: list[nextcord.Member] = []
        for member in members_connected:
            if member.bot:
                continue
            # if member.voice.deaf or member.voice.self_deaf:
            #    continue
            members_useful.append(member)

        reactions: list[nextcord.Reaction] = message.reactions
        count = 0
        target = len(members_useful) / 2
        for reaction in reactions:
            print(reaction)
            async for user in reaction.users():
                print(user)
                if user in members_useful:
                    count += 1
        print(reactions)
        print(count)
        print(target)
        print(members_connected)
        print(members_useful)

        if count > target:
            player = await YTDLSource.play(url=url, loop=self.bot.loop, stream=True)
            self.queue.insert(0, player)
            await message.channel.send(f"Successfully voted to priority queue: \"{player.title}\"")
        else:
            player = await YTDLSource.play(url=url, loop=self.bot.loop, stream=True)
            await message.channel.send(f"Vote Failed to priority queue: \"{player.title}\"")

        self.priority_method.stop()

    @nextcord.slash_command(description="display the queue", guild_ids=test_servers)
    async def queue(self, interaction: nextcord.Interaction):
        titles = "\n".join([f"- {i.title}" for i in self.queue])
        await interaction.response.send_message(f"The Queue is:\n{titles}")

    @tasks.loop(seconds=1)
    async def queue_method(self, channel: nextcord.TextChannel):
        voice_client: nextcord.VoiceClient = self.bot.voice_clients[0]
        if not voice_client.is_playing() and self.queue != [] and not voice_client.is_paused():
            # print("not playing and queue not empty")
            player_data = self.queue.pop()
            # print(player_data.url)
            player = await YTDLSource.play(player_data.url, loop=self.bot.loop, stream=True)
            voice_client.play(source=player, after=lambda e: print(f"Player error: {e}") if e else None)

            await channel.send(f"Now playing: {player_data.title}")
        if not voice_client.is_playing() and self.queue == []:
            self.queue_method.stop()

    @nextcord.slash_command(description="toggle pause", guild_ids=test_servers)
    async def pause(self, interaction: nextcord.Interaction):
        voice_client: nextcord.VoiceClient = self.bot.voice_clients[0]
        if voice_client.is_paused():
            voice_client.resume()
            await interaction.send("Resumed!")
        else:
            voice_client.pause()
            await interaction.send("Paused!")

    @nextcord.slash_command(description="toggle pause", guild_ids=test_servers)
    async def stop(self, interaction: nextcord.Interaction):
        self.queue.clear()
        self.queue_method.stop()
        voice_client: nextcord.VoiceClient = self.bot.voice_clients[0]
        voice_client.stop()
        await voice_client.disconnect()
        await interaction.send("Stopped and disconnected from vc")

    @nextcord.slash_command(description="toggle pause", guild_ids=test_servers)
    async def skip(self, interaction: nextcord.Interaction):
        voice_client: nextcord.VoiceClient = self.bot.voice_clients[0]
        voice_client.stop()
        await interaction.send("Skipped the Song!")
