import discord
import datetime
import pytz
from discord.ext import commands

class ShowTime(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def time(self, ctx, *, timepoint): # change command here
        timezone = pytz.timezone(timepoint)
        time = datetime.datetime.now(tz=timezone)

        embedGo = discord.Embed(
            colour = 0x2F3136
        )

        embedGo.add_field(name='Time: ', value=time.strftime('%I:%M %p\n'), inline=False)
        embedGo.add_field(name='Date: ', value=time.strftime('%A, %d %B %Y'), inline=False)
        embedGo.set_footer(text=time.strftime('(GMT%z)'))

        await ctx.send(embed=embedGo)

def setup(bot):
    bot.add_cog(ShowTime(bot))