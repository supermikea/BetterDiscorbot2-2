import sys
import time

import nextcord
from nextcord import SlashOption
from nextcord.ext import commands

# variables setup
start_time = time.time()

# initial bot setup

intents = nextcord.Intents.default()
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


@bot.slash_command(description="Repeats your message")
async def echo(interaction: nextcord.Interaction, arg: str = SlashOption(description="message")):
    await interaction.send(arg)


@bot.slash_command(description="prints the uptime of the bot")
async def uptime(interaction: nextcord.Interaction):
    await interaction.send(f"Uptime: {time.strftime('%H:%M:%S', time.time() - start_time)} seconds")


# bot initiation code
def write_read_f(option, token, location):  # write or read token from token file
    if option == "w":
        file = open(sys.path[0] + location, "w")
        file.write(token)
        file.close()
        return 0
    # if option is not True then this is automatically executed
    file = open(sys.path[0] + location, "r")
    r_token = file.read()
    file.close()
    return r_token


token = write_read_f("r", 0, "/token")

from music.music import *

bot.add_cog(Music(bot))
bot.run(token)
