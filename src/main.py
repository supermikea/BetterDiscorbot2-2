import sys

import nextcord
from nextcord.ext import commands

# import subcommands
from General.general import General
from Music.music import Music
from Developer.developer import Developer

intents = nextcord.Intents.all()
intents.typing = True
intents.presences = False
intents.message_content = True
intents.voice_states = True


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


if __name__ == "__main__":
    bot = commands.Bot(command_prefix='~', intents=intents, description="miauw")
    bot.add_cog(General(bot))
    bot.add_cog(Music(bot))
    bot.add_cog(Developer(bot))
    token = write_read_f('~', location="/token")
    bot.run(token)
