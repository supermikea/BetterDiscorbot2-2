import sys
import subprocess
import time
import aiohttp

import nextcord
from nextcord.ext import commands
import mafic


# import subcommands
from General.general import General
from Music.music import Music
from Developer.developer import Developer
from Economy.economy import Economy

from Utils.utils import log

intents = nextcord.Intents.all()


def write_read_f(option, *_token, location):  # write or read token from token file
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


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # lavalink setup
        self.pool = mafic.NodePool(self)
        self.loop.create_task(self.add_nodes())

        self.command_prefix = "~"
        self.description = "miauw"
        self.log = log(loglevel=20, classname="main")

    async def add_nodes(self):
        try:
            await self.pool.create_node(
                host="127.0.0.1",
                port=2333,
                label="MAIN",
                password="mikeiscool",
            )
        except aiohttp.client_exceptions.ClientConnectorError as e:
            self.log("error", f"there will not be any music nor voice: error as -> {e}")
            


if __name__ == "__main__":
    #subprocess.Popen(["java", "-jar", "lavalink/Lavalink.jar"]) # TODO autostart bot cause thisd not workie workie???
    #time.sleep(5)  # give lavalink time to start
    bot = Bot(intents=intents)
    bot.add_cog(General(bot))
    bot.add_cog(Music(bot))
    bot.add_cog(Developer(bot))
    bot.add_cog(Economy(bot))
    token = write_read_f('~', location="/token")
    
    print("Starting bot...")
    bot.run(token)
