import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Bot
import json
import time
import collections
import random

from Utils.utils import log

class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot, scavenge_cooldown=25, loglevel=20):
        self.bot = bot
        self.scavenge_cooldown = scavenge_cooldown
        self.log = log(loglevel=loglevel, classname="ecomony")

        # get the economy data
        self.economyData = {}
        try:  # open economy.json and account for all the errors
            economyData = open("economy.json", "r")
        except FileNotFoundError as e:
            self.log("warning", "economy.json not found, continuing with empty economyData")
            economyData = {}
        except Exception as e:
            self.self.log("warning", "error occured while opening economy.json, continuing with empty economyData")
            economyData = {}
        if economyData == "":  # load economy.json contents into dict
            self.log("warning", "economy.json empty, continuing with empty economyData")
            economyData = {}
        else:
            try:
                self.log("debug", "loading economyData.json")
                economyData = json.load(economyData)  # if everything goes well this should execute
            except Exception as e:
                self.log("warning", f"could not parse economyData, continuing with empty economyData:\n{e}")
                economyData = {}

        self.economyData = collections.defaultdict(int, economyData)  # turn economyData into defaultdict, so we don't get keyerror all the time
        #print(type(economyData))
        # --

    #boilerplate
    def check_user(self, id):  # checks if user exists in economy data
        if not str(id) in self.economyData:
            self.economyData[str(id)] = {"money": 0}
            self.update_economy_file()
        #if not "command-info" in self.economyData[str(id)]:
        #    self.economyData[str(id)]["command-info"] = {}
        #    self.economyData[str(id)]["command-info"]["scavenge"] = {}
        #    self.economyData[str(id)]["command-info"]["scavenge"]["last-used"] = 0

    def add_money(self, id, amount):  # adds money to specified account (this shouldn't need a comment)
        self.check_user(id)
        self.economyData[str(id)]['money'] += amount
        self.update_economy_file()

    def update_economy_file(self):  # write economyData to economy.json
        with open("economy.json", "w") as file:
            json.dump(self.economyData, file, indent=4)  # Using indent=4 for pretty printing

    def get_balance(self, id: str):
        self.check_user(id)
        return self.economyData[id]["money"]

    def get_used_time(self, id: str, command: str):
        self.check_user(id)
        return self.economyData[id]["command-info"][command]["last-used"]

    def set_used_time(self, id: str, command: str, time: float):
        self.check_user(id)
        self.economyData[id]["command-info"][command]["last-used"] = time

    # commands
    @nextcord.slash_command(description="give cookies to other user")
    async def transact(self, interaction: nextcord.Interaction, recipient: nextcord.User, amount: int):
        self.log("debug", str(self.economyData[str(interaction.user.id)]['money']) + " || " + str(type(interaction.user.id)))
        if amount < 0:
            await interaction.send(f"You can't transact negative amounts")
            return
        if not (self.economyData[str(interaction.user.id)]['money'] - amount) >= 0:
            await interaction.send(f"You don't have enough cookies for that!")
            return
        self.add_money(interaction.user.id, -amount)
        self.add_money(recipient.id, amount)
        await interaction.send(f"You gave {amount} cookies to {recipient.name}!")

    @nextcord.slash_command(description="try to find cookies")
    async def scavenge(self, interaction: nextcord.Interaction):
        if not time.time() - self.get_used_time(str(interaction.user.id), "scavenge") - self.scavenge_cooldown < time.time():
            await interaction.send(f"You have to wait another {time.time() - self.get_used_time(str(interaction.user.id), "scavenge") - self.scavenge_cooldown} seconds before using this")
        amount = random.randint(1, 40)
        self.add_money(interaction.user.id, amount)
        await interaction.send(f"You found {amount} cookies! ({time.time()})")
        self.set_used_time(str(interaction.user.id), "scavenge", time.time())

    @nextcord.slash_command(description="check how much money you have")
    async def balance(self, interaction: nextcord.Interaction):
        self.check_user(str(interaction.user.id))
        balance = self.get_balance(str(interaction.id))
        if balance >= 0:
            await interaction.send(f"You currently have {balance} cookies")
        else:
            await interaction.send(f"You are currently {-balance} cookies in debt to the cookie gods, ***you will hear from the tax collecter soon***")



