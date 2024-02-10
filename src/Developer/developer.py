import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Bot

import os
import subprocess
import sys


class Developer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.check(commands.is_owner())
    @commands.command(hidden=True)
    async def restart(self, ctx):
        await ctx.reply("Sure Mike!\n restarting...")
        os.system("python3 \"/home/ubuntu/discor_bot/BetterDiscorbot2-2/src/restart.py\" &")
        sys.exit()


    @commands.check(commands.is_owner())
    @commands.command(hidden=True)
    async def update(self, ctx):
        await ctx.reply("Sure Mike!\n updating...")
        output = subprocess.run(["git", "pull"], capture_output=True).stdout
        await ctx.reply("Updated? here is the output:\n" + output.decode("utf-8"))


    @commands.check(commands.is_owner())
    @commands.command(hidden=True)
    async def load(self, ctx, module: str):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.reply('\N{PISTOL}')
            await ctx.reply('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.reply('\N{OK HAND SIGN}')

    @commands.check(commands.is_owner())
    @commands.command(hidden=True)
    async def unload(self, ctx, module: str):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.reply('\N{PISTOL}')
            await ctx.reply('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.reply('\N{OK HAND SIGN}')

    @commands.check(commands.is_owner())
    @commands.command(name='reload', hidden=True)
    async def _reload(self, ctx, module: str):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.reply('\N{PISTOL}')
            await ctx.reply('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.reply('\N{OK HAND SIGN}')
