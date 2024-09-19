import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Bot
import json
from src.Utils import utils

import random

economyData = {}

class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        global economyData
        economyData = open("Economy/economy.json", "r").read()
        if economyData == "":
            self.log("warning", "no economy data found")
            economyData = {}
        else:
            economyData = json.loads(economyData)

    def log(prefix, message):
        utils.log(prefix, "economy", message)

    #checks if user exists in economy data
    def check_user(self, username):
        if not economyData.__contains__(username):
            economyData[username] = {"money": 0}

    def add_money(self, username, amount):
        self.check_user(username)
        economyData[username]['money'] += amount

    @nextcord.slash_command(description="give coins to other user")
    async def transact(self, interaction: nextcord.Interaction):
        self.check_user(interaction.user.name)
        await interaction.response.send_message(str(economyData) + " | "+interaction.user.name)

    @nextcord.slash_command(description="try to find money")
    async def scrunge(self, interaction: nextcord.Interaction):
        amount = random.randint(0, 15)
        self.add_money(interaction.user.name, amount)
        await interaction.send(f"You found ${amount}!")



