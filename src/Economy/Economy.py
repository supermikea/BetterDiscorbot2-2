import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Bot
import json

import random

class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        economyData = open("economy.json", "r").read()
        if economyData == "":
            print("no data")



    @nextcord.slash_command(description="give coins to other user")
    async def transact(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("Pong!")
