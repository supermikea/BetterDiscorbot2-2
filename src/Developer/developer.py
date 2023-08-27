import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Bot

test_servers = [1030579093659471913]


class Developer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

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
