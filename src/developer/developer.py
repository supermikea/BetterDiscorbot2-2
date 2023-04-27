import asyncio
import os
import sys

import nextcord

from nextcord.ext import commands, tasks

class developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def restart(self, ctx):
        if str(ctx.author) == "supermikea#5051":
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        else:
            await ctx.send("https://tenor.com/view/no-way-dude-no-oh-bugs-bunny-bugs-gif-22941840")