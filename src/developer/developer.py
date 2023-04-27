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
            await ctx.reply("Sure Mike!\n restarting...")
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        else:
            await ctx.reply("https://tenor.com/view/no-way-dude-no-oh-bugs-bunny-bugs-gif-22941840")
    
    @commands.command()
    async def update(self, ctx):
        if str(ctx.author) == "supermikea#5051":
            await ctx.reply("Sure Mike!\n updating...")
            output = os.system("git pull")
            await ctx.reply("Updated! here is the output:\n" + output)
        else:
            await ctx.reply("https://tenor.com/view/no-way-dude-no-oh-bugs-bunny-bugs-gif-22941840")