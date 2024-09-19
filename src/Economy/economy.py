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
            economyData = open("economy.json", "r")
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
                economyData = json.load(economyData)  # if everything goes well this should execute
            except Exception as e:
                log("warning", f"could not parse economyData, continuing with empty economyData:\n{e}")
                economyData = {}
        # --

    def check_user(self, id):  # checks if user exists in economy data
        if not str(id) in economyData:
            economyData[str(id)] = {"money": 0}
            self.update_economy_file()

    def add_money(self, id, amount):  # adds money to specified account (this shouldn't need a comment)
        self.check_user(id)
        economyData[str(id)]['money'] += amount
        self.update_economy_file()

    def update_economy_file(self):  # write economyData to economy.json
        with open("economy.json", "w") as file:
            json.dump(economyData, file, indent=4)  # Using indent=4 for pretty printing

    @nextcord.slash_command(description="give cookies to other user")
    async def transact(self, interaction: nextcord.Interaction, recipient: nextcord.User, amount: int):
        log("debug", str(economyData[str(interaction.user.id)]['money']) + "|| " + str(type(interaction.user.id)))
        if not (economyData[str(interaction.user.id)]['money'] - amount) >= 0:
            await interaction.send(f"You don't have enough cookies for that!")
            return
        self.add_money(interaction.user.id, -amount)
        self.add_money(recipient.id, amount)
        await interaction.send(f"You gave {amount} cookies to {recipient.name}!")

    @nextcord.slash_command(description="try to find cookies")
    async def scavenge(self, interaction: nextcord.Interaction):
        amount = random.randint(1, 40)
        self.add_money(interaction.user.id, amount)
        await interaction.send(f"You found {amount} cookies!")

    @nextcord.slash_command(description="check how much money you have")
    async def balance(self, interaction: nextcord.Interaction):
        self.check_user(interaction.user.id)
        await interaction.send(f"You currently have {economyData[str(interaction.user.id)]['money']} cookies")



