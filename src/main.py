import sys
import time

import nextcord
from nextcord import SlashOption
from nextcord.ext import commands

# variables setup
start_time = time.time()

# initial bot setup

intents = nextcord.Intents.default()
intents.message_content = True
activity = nextcord.Activity(name="You", type=nextcord.ActivityType.watching, state="watching YOU")
bot = commands.Bot(command_prefix="~", intents=intents, activity=activity)


# signal that the bot is online
@bot.event
async def on_ready():
    print(f"[INFO] started successfully!")
    print(f"[INFO] Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"[INFO] Activity is: {bot.activity}")


@bot.slash_command(description="Replies with \"Pong!\"")
async def ping(interaction: nextcord.Interaction):
    await interaction.send("Pong!", ephemeral=True)


# repeats your message
@bot.slash_command(description="Repeats your message")
async def echo(interaction: nextcord.Interaction, arg: str = SlashOption(description="message")):
    await interaction.send(arg)


# prints the bot's uptime
@bot.slash_command(description="prints the uptime of the bot")
async def uptime(interaction: nextcord.Interaction):
    _uptime = round((time.time() - start_time) / 60 / 60, 2)
    await interaction.send(f"Uptime: {_uptime} hours")


# bot initiation code
def write_read_f(option, _token, location):  # write or read token from token file
    if option == "w":
        file = open(sys.path[0] + location, "w")
        file.write(_token)
        file.close()
        return 0
    # if option is not True then this is automatically executed
    file = open(sys.path[0] + location, "r")
    r_token = file.read()
    file.close()
    return r_token


token = write_read_f("r", 0, "/token")

from music.music import *
from developer.developer import *


bot.add_cog(Music(bot))
bot.add_cog(developer(bot))
bot.run(token)
