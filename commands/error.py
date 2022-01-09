import discord
from discord.ext import commands

class Errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass # Just let it slide, because it will be spammy

def setup(bot):
    bot.add_cog(Errors(bot))