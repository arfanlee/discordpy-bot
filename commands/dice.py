import discord
import random
from discord.ext import commands

class Dice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['dice','rolldice','rd'])
    async def roll(self, ctx): # Change here
        dice = [1,2,3,4,5,6]
        diced = random.choice(dice)
        embed = discord.Embed(
                colour = discord.Colour.green()
            )
        embed.set_author(name=f'{ctx.message.author} rolled {diced}')

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Dice(bot))