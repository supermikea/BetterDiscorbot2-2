import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Bot

import random

test_servers = [1030579093659471913]


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(description="Ping command", guild_ids=test_servers)
    async def ping(self, interaction: nextcord.Interaction):
        """Simple command that responds with Pong!"""
        await interaction.response.send_message("Pong!")

    @nextcord.slash_command(description="Repeats your message", guild_ids=test_servers)
    async def echo(self, interaction: nextcord.Interaction, arg: str = SlashOption(description="message")):
        await interaction.send(arg)

    @nextcord.slash_command(description="Rolls a number", guild_ids=test_servers)
    async def roll(self, interaction: nextcord.Interaction, limit: int = SlashOption(description="Limit of roll",
                                                                                     required=False, default=100)):
        await interaction.send(f"You rolled: {random.randint(0, limit)}\n - limit: {limit}")
