import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Bot

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
