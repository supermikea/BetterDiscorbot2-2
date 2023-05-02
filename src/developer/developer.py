import asyncio
import sys
import subprocess

import nextcord
from nextcord.ext import commands, tasks

# global vars
# sys.stdout = open('log.log', 'w')


class developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def restart(self, ctx):
        if str(ctx.author) == "supermikea#5051":
            await ctx.reply("Sure Mike!\n restarting...")
            subprocess.run("python3 \"/home/ubuntu/BetterDiscorbot2-2/src/main.py\"", capture_output=True)
            sys.exit()
        else:
            await ctx.reply("https://tenor.com/view/no-way-dude-no-oh-bugs-bunny-bugs-gif-22941840")
    
    @commands.command()
    async def update(self, ctx):
        if str(ctx.author) == "supermikea#5051":
            await ctx.reply("Sure Mike!\n updating...")
            output = subprocess.run("git pull", capture_output=True)
            await ctx.reply("Updated? here is the output:\n" + output)
        else:
            await ctx.reply("https://tenor.com/view/no-way-dude-no-oh-bugs-bunny-bugs-gif-22941840")
    

    @commands.command()
    async def live_update(self, ctx):
        if str(ctx.author) == "supermikea#5051":
            await ctx.reply("TODO: Not implemented!")
        else:
            await ctx.reply("https://tenor.com/view/no-way-dude-no-oh-bugs-bunny-bugs-gif-22941840")
    @commands.command()
    async def get_log(self, ctx):
        if str(ctx.author) == "supermikea#5051":
            await ctx.reply("it broken sooooooooooo no...")
            
            # await ctx.reply("Sure Mike!\n Uploading log...")
            # with open('log.log', 'rb') as f:
            #     log_file = nextcord.File(fp=f, filename="log.txt", description="your log mike")
            # await ctx.send(file=log_file)
            #sys.stdout = open('log.log', 'w')
        else:
            await ctx.reply("https://tenor.com/view/no-way-dude-no-oh-bugs-bunny-bugs-gif-22941840")

if __name__ == "__main__":
    os.system('python3 "../main.py"')