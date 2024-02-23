import asyncio

import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, tasks

import mafic

test_servers = [1030579093659471913]


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.queue: list[mafic.Track] = []
        self.player = mafic.Player
        self.queue_loop.start()
        self.ensure_queue_loop.start()

    # noinspection PyUnboundLocalVariable
    @nextcord.slash_command(description="play something")
    async def play(self, inter: nextcord.Interaction, query: str):
        print("[DEBUG] play command called with arg: " + query)
        if not inter.guild.voice_client:
            self.player = await inter.user.voice.channel.connect(cls=mafic.Player)
        else:
            self.player = inter.guild.voice_client

        # could take a while
        await inter.response.defer()

        try:
            tracks = await self.player.fetch_tracks(query)
        except Exception as e:
            return await inter.send(f"Error while searching: {e}")

        if not tracks:
            return await inter.send("No tracks found.")

        # check for playlist
        if isinstance(tracks, mafic.Playlist):
            self.queue += tracks.tracks
            await inter.send(f"Added {len(tracks.tracks)} tracks to the queue.")
            playlist = True
        else:
            playlist = False
            track = tracks[0]

        # check if something is already playing
        if self.player.current and not playlist:
            await inter.send(f"Added {track.title} to the queue.")
            self.queue.append(track)
            return

        # playlist logic
        if playlist:
            if not self.player.current:
                await self.player.play(self.queue.pop(0))
            return

        await self.player.play(track)

        await inter.send(f"Playing {track.title}.")

    @nextcord.slash_command(description="display the queue")
    async def queue(self, inter: nextcord.Interaction):
        if not self.queue:
            return await inter.send("The queue is empty.")

        # format it correctly
        temp = ""
        count = 0
        for i in self.queue:
            count += 1
            temp += str(count) + ". " + i.title + "\n"

        await inter.send(f"Queue:\n{temp}")

    @nextcord.slash_command(description="Pause the current song")
    async def pause(self, inter: nextcord.Interaction):
        if not self.player.current:
            return await inter.send("Nothing is playing.")

        if self.player.paused:
            await self.player.resume()
            return await inter.send("Resumed.")
        else:
            await self.player.pause()
            return await inter.send("Paused.")

    @nextcord.slash_command(description="Stop the current song")
    async def stop(self, inter: nextcord.Interaction):
        if not self.player.current:
            return await inter.send("Nothing is playing.")

        await self.player.stop()
        self.queue.clear()
        return await inter.send("Stopped.")

    @nextcord.slash_command(description="ping_player")
    async def ping_player(self, inter: nextcord.Interaction):
        await inter.send("pong")
        await inter.send("voice_client latency: " + str(self.player.ping) + "ms")

    @nextcord.slash_command(description="skip the current song")
    async def skip(self, inter: nextcord.Interaction):
        if not self.player.current:
            return await inter.send("Nothing is playing.")

        await self.player.stop()
        return await inter.send("Skipped.")

    # give status info
    @nextcord.slash_command(description="give status info")
    async def status(self, inter: nextcord.Interaction):
        if not self.player.current:
            return await inter.send("Nothing is playing.")

        temp = "None"
        await inter.send(f"Currently playing: {self.player.current.title}\n"
                         f"by {self.player.current.author}\n"
                         f"at {self.player.position}/{self.player.current.length}.\n"
                         f"next up: {self.queue[0].title if self.queue is True else temp}.\n")

    # queue loop
    @tasks.loop(seconds=1)
    async def queue_loop(self):
        print("[DEBUG] queue loop")
        if not self.queue:
            print("[DEBUG] no tracks in queue")

        if not self.player.current and self.queue:
            print("[DEBUG] no current track")
            track = self.queue.pop(0)
            await self.player.play(track)

        print("[DEBUG] no condition met")

    @tasks.loop(seconds=1)
    async def ensure_queue_loop(self):
        if not self.queue_loop.is_running():
            self.queue_loop.start()
            print("[DEBUG] queue loop restarted")
