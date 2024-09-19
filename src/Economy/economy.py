import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Bot
import json
from src.Utils import utils

import random


def log(prefix, message):
    utils.log(prefix, "economy", message)


class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # get the economy data
        global economyData
        try:  # open economy.json and account for all the errors
            economyData = open("economy.json", "r").read()
        except FileNotFoundError as e:
            log("warning", "economy.json not found, continuing with empty economyData")
            economyData = {}
        except Exception as e:
            log("warning", "error occured while opening economy.json, continuing with empty economyData")
            economyData = {}

        if economyData == "":  # load economy.json contents into dict
            log("warning", "economy.json empty, continuing with empty economyData")
            economyData = {}
        else:
            try:
                log("debug", "loading economyData.json")
                economyData = dict(json.loads(economyData))  # if everything goes well this should execute
            except Exception as e:
                log("warning", f"could not parse economyData, continuing with empty economyData\n{e}")
                economyData = {}
        log("debug", type(economyData))
        # --

    def check_user(self, username):  # checks if user exists in economy data
        if not economyData.__contains__(username):
            economyData[username] = {"money": 0}

    def add_money(self, username, amount):  # adds money to specified account (this shouldn't need a comment)
        self.check_user(username)
        economyData[username]['money'] += amount
        open("economy.json", 'w').write(json.dumps(str(economyData)))

    @nextcord.slash_command(description="give coins to other user")
    async def transact(self, interaction: nextcord.Interaction):
        self.check_user(interaction.user.name)
        await interaction.response.send_message(str(economyData) + " | "+interaction.user.name)

    @nextcord.slash_command(description="try to find money")
    async def scrunge(self, interaction: nextcord.Interaction):
        amount = random.randint(0, 15)
        self.add_money(interaction.user.name, amount)
        await interaction.send(f"You found ${amount}!")

    @nextcord.slash_command(description="check how much money you have")
    async def check_money(self, interaction: nextcord.Interaction):
        money = economyData[interaction.user.name]['money']
        await interaction.send(f"You currently have ${money}")



