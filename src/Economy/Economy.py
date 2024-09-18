import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Bot
import json
from src.Utils import utils

import random

economyData = {}
def log(prefix, message):
    utils.log(prefix, "economy", message)


class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        economyData = open("economy.json", "r").read()
        if economyData == "":
            log("info", "no economy data found")
        else:
            economyData = json.loads(economyData)

    @nextcord.slash_command(description="give coins to other user")
    async def transact(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(economyData)
